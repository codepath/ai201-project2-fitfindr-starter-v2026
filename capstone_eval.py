#!/usr/bin/env python3
"""
Capstone test run: three trials of every scenario, through the real HTTP route.

    python capstone_eval.py --label before          3 trials (default)
    python capstone_eval.py --label after           after the improvement
    python capstone_eval.py --cost 10               10 happy-path runs, average cost

Every request goes through serve.py's POST /ask (Flask's test client, so no
second terminal is needed), which means every request also lands in
logs/runs.jsonl exactly as it would on the running server.

Caching is turned OFF here, so every trial is a real model call and the token
counts are real.

What this does NOT do is decide MET or MISSED. It reports the measurements
per trial; the targets are in criteria.md and the verdicts are yours.

Output: results/capstone_<label>_<timestamp>.md  (+ .json with everything)
"""
import os

os.environ["AI201_CACHE"] = "0"  # before config is imported anywhere

import argparse
import datetime as dt
import json
import re
import statistics
import sys

import config  # noqa: E402
import runlog  # noqa: E402

# ── scenarios ────────────────────────────────────────────────────────────────
# expect_size: what the parser should produce. expect_listing_size: what every
# returned listing's size must match (None = filtering not checked).
SCENARIOS = [
    # The extension: numeric sizes
    {"id": "S1", "group": "extension", "name": "shoe size, whole",
     "query": "platform sneakers size 8", "expect_size": "US 8"},
    {"id": "S2", "group": "extension", "name": "shoe size, half",
     "query": "chelsea boots size 8.5", "expect_size": "US 8.5"},
    {"id": "S3", "group": "extension", "name": "waist, W-form",
     "query": "high-waisted denim shorts W27", "expect_size": "W27"},
    {"id": "S4", "group": "extension", "name": "waist, word form",
     "query": "straight leg black jeans waist 28", "expect_size": "W28"},
    {"id": "S5", "group": "extension", "name": "numeric size nobody stocks",
     "query": "canvas sneakers size 12", "expect_size": "US 12", "expect_empty": True},
    # Regression: what already worked must still work
    {"id": "R1", "group": "regression", "name": "letter size + price (unit 3 query)",
     "query": "vintage graphic tee under $30, size M", "expect_size": "M"},
    {"id": "R2", "group": "regression", "name": "no size at all",
     "query": "vintage jacket under $25", "expect_size": None},
    # Bad path
    {"id": "F1", "group": "failure", "name": "empty query", "body": {"query": "   "},
     "expect_status": 400},
    {"id": "F2", "group": "failure", "name": "body is not JSON", "raw": "query=sneakers",
     "expect_status": 400},
    {"id": "F3", "group": "failure", "name": "model unreachable (fault injected)",
     "query": "platform sneakers size 8", "expect_size": "US 8", "model_down": True},
]

COST_QUERY = "platform sneakers size 8"


# ── one request ──────────────────────────────────────────────────────────────

def _size_ok(wanted, listing_size):
    from tools import _size_matches
    return _size_matches(wanted, listing_size)


def run_scenario(client, sc):
    import tools
    from generate import ModelUnavailable

    original_generate = tools.generate
    if sc.get("model_down"):
        def _down(*a, **k):
            raise ModelUnavailable("Injected for testing: the model API is unreachable.")
        tools.generate = _down
    try:
        if "raw" in sc:
            resp = client.post("/ask", data=sc["raw"], content_type="text/plain")
        else:
            resp = client.post("/ask", json=sc.get("body") or {"query": sc["query"]})
    finally:
        tools.generate = original_generate

    body = resp.get_json(silent=True) or {}
    rec = runlog.read(1)[-1] if runlog.read(1) else {}
    request_id = body.get("request_id")
    logged = bool(rec) and (rec.get("request_id") == request_id or request_id is None
                            and rec.get("status") == resp.status_code)

    parsed = body.get("parsed") or {}
    results = body.get("search_results") or []
    desc = parsed.get("description") or ""
    m = {
        "id": sc["id"], "status": resp.status_code,
        "outcome": rec.get("outcome"),
        "parsed_size": parsed.get("size"),
        "size_kind": body.get("size_kind"),
        "description": desc,
        "size_parsed_right": (parsed.get("size") == sc.get("expect_size"))
                             if "expect_size" in sc else None,
        "size_text_left_in_description": bool(re.search(r"\b(size|waist|W\d{2}|US)\b|\d", desc,
                                                       re.IGNORECASE))
                                         if sc.get("expect_size") else None,
        "n_results": len(results),
        "all_results_match_size": (all(_size_ok(sc["expect_size"], r.get("size", ""))
                                       for r in results) if results else None)
                                  if sc.get("expect_size") else None,
        "result_sizes": [r.get("size") for r in results],
        "selected": (body.get("selected_item") or {}).get("title"),
        "fit_card_made": bool(body.get("fit_card")),
        "error": body.get("error"),
        "error_names_size": (sc["expect_size"] in (body.get("error") or ""))
                            if sc.get("expect_empty") else None,
        "duration_ms": rec.get("duration_ms"),
        "timings_ms": rec.get("timings_ms"),
        "total_tokens": rec.get("total_tokens"),
        "model_calls": rec.get("model_calls"),
        "logged": logged,
        "fit_card": body.get("fit_card"),
    }
    if "expect_status" in sc:
        m["status_as_expected"] = resp.status_code == sc["expect_status"]
    return m


# ── reporting ────────────────────────────────────────────────────────────────

def _fmt(v):
    if v is None:
        return "–"
    if v is True:
        return "yes"
    if v is False:
        return "**NO**"
    return str(v)


def trial_table(rows):
    head = ("| ID | Query | Status | Parsed size | Size right | Size text left | Results | "
            "All match size | Fit card | Error names size | ms | Tokens | Logged |")
    out = [head, "|" + "---|" * 13]
    for sc, m in rows:
        q = sc.get("query") or sc.get("raw") or json.dumps(sc.get("body"))
        out.append(
            f"| {sc['id']} | `{q}` | {m['status']} | {_fmt(m['parsed_size'])} | "
            f"{_fmt(m['size_parsed_right'])} | {_fmt(m['size_text_left_in_description'])} | "
            f"{m['n_results']} | {_fmt(m['all_results_match_size'])} | "
            f"{_fmt(m['fit_card_made'])} | {_fmt(m['error_names_size'])} | "
            f"{_fmt(m['duration_ms'])} | {_fmt(m['total_tokens'])} | {_fmt(m['logged'])} |"
        )
    return "\n".join(out)


def summary(all_trials):
    """Counts per trial that criteria can be scored against."""
    def count(trial, pred, filt):
        sel = [(sc, m) for sc, m in trial if filt(sc)]
        return f"{sum(1 for sc, m in sel if pred(sc, m))}/{len(sel)}"

    ext = lambda sc: sc["group"] == "extension" and not sc.get("expect_empty")  # noqa: E731
    lines = [
        ("Numeric size parsed to the right value (S1–S5)",
         lambda sc, m: m["size_parsed_right"], lambda sc: sc["group"] == "extension"),
        ("Size text removed from the description (S1–S5)",
         lambda sc, m: m["size_text_left_in_description"] is False,
         lambda sc: sc["group"] == "extension"),
        ("Every returned listing matches the numeric size (S1–S4, needs ≥1 result)",
         lambda sc, m: m["n_results"] > 0 and m["all_results_match_size"], ext),
        ("Numeric-size query ends in a fit card (S1–S4)",
         lambda sc, m: m["fit_card_made"], ext),
        ("Unstocked size stops early AND the message names the size (S5)",
         lambda sc, m: m["n_results"] == 0 and not m["fit_card_made"] and m["error_names_size"],
         lambda sc: sc.get("expect_empty")),
        ("Regression queries still parse and finish with a fit card (R1–R2)",
         lambda sc, m: m["size_parsed_right"] and m["fit_card_made"],
         lambda sc: sc["group"] == "regression"),
        ("Bad input gets a 400, not a 500 (F1–F2)",
         lambda sc, m: m.get("status_as_expected"), lambda sc: "expect_status" in sc),
        ("Model down: 200 + error naming the found listing, no crash (F3)",
         lambda sc, m: m["status"] == 200 and m["error"] and not m["fit_card_made"]
         and bool(m["selected"]) and m["selected"] in (m["error"] or ""),
         lambda sc: sc.get("model_down")),
        ("Every request left a log record (all)",
         lambda sc, m: m["logged"], lambda sc: True),
        ("Runs under 10 s end to end (S1–S4, R1–R2)",
         lambda sc, m: (m["duration_ms"] or 0) < 10_000,
         lambda sc: sc["group"] in ("extension", "regression") and not sc.get("expect_empty")),
    ]
    head = "| Measurement | " + " | ".join(f"Trial {i}" for i in range(1, len(all_trials) + 1)) + " |"
    out = [head, "|---|" + "---|" * len(all_trials)]
    for name, pred, filt in lines:
        cells = []
        for trial in all_trials:
            try:
                cells.append(count(trial, pred, filt))
            except Exception:  # noqa: BLE001
                cells.append("?")
        out.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def run_cost(client, n):
    rows = []
    for i in range(n):
        resp = client.post("/ask", json={"query": COST_QUERY})
        rec = runlog.read(1)[-1]
        rows.append(rec)
        print(f"  cost run {i + 1}/{n}: {rec['total_tokens']} tokens, "
              f"{rec['duration_ms']} ms, status {resp.status_code}", flush=True)
    ok = [r for r in rows if r["outcome"] == "fit_card"]
    tok = [r["total_tokens"] for r in ok]
    pt = [r["prompt_tokens"] for r in ok]
    ot = [r["output_tokens"] for r in ok]
    ms = [r["duration_ms"] for r in ok]
    stage = {}
    for r in ok:
        for k, v in (r.get("timings_ms") or {}).items():
            stage.setdefault(k, []).append(v)
    return {
        "query": COST_QUERY, "runs": n, "successful": len(ok),
        "mean_total_tokens": round(statistics.mean(tok), 1) if tok else None,
        "mean_prompt_tokens": round(statistics.mean(pt), 1) if pt else None,
        "mean_output_tokens": round(statistics.mean(ot), 1) if ot else None,
        "min_total_tokens": min(tok) if tok else None,
        "max_total_tokens": max(tok) if tok else None,
        "mean_duration_ms": round(statistics.mean(ms), 1) if ms else None,
        "median_duration_ms": round(statistics.median(ms), 1) if ms else None,
        "mean_stage_ms": {k: round(statistics.mean(v), 1) for k, v in stage.items()},
        "model_calls_per_run": sorted({r["model_calls"] for r in ok}),
        "records": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="before")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--cost", type=int, default=0,
                    help="instead of the scenarios, run the happy path N times and average")
    args = ap.parse_args()

    from serve import app
    client = app.test_client()
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    (config.ROOT / "results").mkdir(exist_ok=True)

    if args.cost:
        print(f"Cost run: {args.cost} × {COST_QUERY!r}, cache off.")
        res = run_cost(client, args.cost)
        out = config.ROOT / "results" / f"capstone_cost_{stamp}.json"
        out.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({k: v for k, v in res.items() if k != "records"}, indent=2))
        print(f"\nWrote {out.relative_to(config.ROOT)}")
        return

    all_trials = []
    for t in range(1, args.trials + 1):
        print(f"\nTrial {t}/{args.trials}")
        trial = []
        for sc in SCENARIOS:
            m = run_scenario(client, sc)
            print(f"  {sc['id']} {sc['name']}: status {m['status']}, size {m['parsed_size']}, "
                  f"{m['n_results']} results, card={m['fit_card_made']}, {m['duration_ms']} ms",
                  flush=True)
            trial.append((sc, m))
        all_trials.append(trial)

    md = [f"# Capstone run — {args.label}", "",
          f"{dt.datetime.now().isoformat(timespec='minutes')} · model `{config.MODEL}` · "
          f"temperature {config.TEMPERATURE} · cache OFF · {args.trials} trials · "
          f"produced by `capstone_eval.py` through `serve.py::ask`", "",
          "## Summary (counts per trial)", "", summary(all_trials), ""]
    for i, trial in enumerate(all_trials, 1):
        md += [f"## Trial {i}", "", trial_table(trial), ""]
    md += ["## Fit cards and errors (trial 1)", ""]
    for sc, m in all_trials[0]:
        md += [f"**{sc['id']} — {sc['name']}**", "",
               "```", (m["fit_card"] or m["error"] or "(none)").strip(), "```", ""]
    n_req = len(SCENARIOS) * args.trials
    md += ["## Log records from this run (`logs/runs.jsonl`, last 12)", "", "```json"]
    md += [json.dumps(r, ensure_ascii=False) for r in runlog.read(min(12, n_req))]
    md += ["```", ""]

    out = config.ROOT / "results" / f"capstone_{args.label}_{stamp}.md"
    out.write_text("\n".join(md), encoding="utf-8")
    raw = [[{"scenario": sc, "measured": m} for sc, m in trial] for trial in all_trials]
    out.with_suffix(".json").write_text(json.dumps(raw, indent=2, ensure_ascii=False),
                                        encoding="utf-8")
    print("\n" + summary(all_trials))
    print(f"\nWrote {out.relative_to(config.ROOT)} (and .json)")


if __name__ == "__main__":
    sys.exit(main())
