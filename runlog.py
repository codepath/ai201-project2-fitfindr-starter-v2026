"""
Structured run log for FitFindr. ← CAPSTONE

Every request to serve.py writes one JSON record (one line) to
logs/runs.jsonl — successful runs, runs that ended on the empty-search
branch, runs where the model or MCP failed, rejected input (400) and crashes
(500). A failure leaves a record, not an absence.

Fields in every record:
    ts             UTC timestamp, ISO 8601
    request_id     short random id for this request
    status         HTTP status returned (200 / 400 / 500)
    outcome        "fit_card", "empty_search", "agent_error", "rejected", "crash"
    query          what came in (raw text)
    parsed         description / size / max_price the parser pulled out
    size_kind      "letter", "shoe", "waist" or null       (the extension)
    n_results      how many listings search_listings returned
    result_sizes   the size field of every returned listing (to check filtering)
    selected       id / title / size / price of the chosen listing, or null
    fit_card       what went out (the fit card text), or null
    error          the error message shown to the user, or null
    duration_ms    end-to-end time for the request, in milliseconds
    timings_ms     per-stage time: parse, search_listings, suggest_outfit,
                   create_fit_card
    model_calls    model requests this run made (cache hits not counted)
    cache_hits     answers served from the local cache this run
    prompt_tokens / output_tokens / total_tokens
                   tokens this run used, as reported by the Gemini API
                   (usage_metadata) — this is the cost measurement

Read it back with:
    python runlog.py            prints the last 12 records
    python runlog.py 20         prints the last 20
"""
import datetime as dt
import json
import sys
import uuid

import config

LOG_DIR = config.ROOT / "logs"
RUN_LOG = LOG_DIR / "runs.jsonl"


def new_request_id() -> str:
    return uuid.uuid4().hex[:8]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def write(record: dict) -> None:
    """Append one record. Never raises: logging must not take a request down."""
    try:
        LOG_DIR.mkdir(exist_ok=True)
        with RUN_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"  [runlog] could not write log record: {exc}", file=sys.stderr)


def read(last: int = 12) -> list[dict]:
    if not RUN_LOG.exists():
        return []
    lines = RUN_LOG.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines[-last:] if line.strip()]


def record_from_session(session: dict | None) -> dict:
    """The session-derived part of a record."""
    if not session:
        return {"parsed": None, "size_kind": None, "n_results": 0,
                "result_sizes": [], "selected": None, "fit_card": None,
                "timings_ms": {}}
    item = session.get("selected_item")
    return {
        "parsed": session.get("parsed"),
        "size_kind": session.get("size_kind"),
        "n_results": len(session.get("search_results") or []),
        "result_sizes": [r.get("size") for r in (session.get("search_results") or [])],
        "selected": (
            {k: item.get(k) for k in ("id", "title", "size", "price")} if item else None
        ),
        "fit_card": session.get("fit_card"),
        "timings_ms": session.get("timings_ms") or {},
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for rec in read(n):
        print(json.dumps(rec, ensure_ascii=False))
