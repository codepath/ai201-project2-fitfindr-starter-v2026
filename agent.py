"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""
import re
import time
import config
import trace
from tools import suggest_outfit, create_fit_card
from mcp_client import call_tool, MCPError
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
        "size_kind": None,           # capstone: "letter", "shoe", "waist" or None
        "timings_ms": {},            # capstone: how long each stage took
    }


# ── query parsing (capstone extension: numeric sizes) ───────────────────────

_LETTER_SIZE = re.compile(r"\b(?:size\s*)?(XXS|XS|S|M|L|XL|XXL)\b", re.IGNORECASE)

# Waist sizes: "W27", "w 30", "waist 28", "28 waist", "28in waist".
_WAIST_SIZE = [
    re.compile(r"\bW\s?(\d{2})\b", re.IGNORECASE),
    re.compile(r"\bwaist\s*(?:size\s*)?(\d{2})\b", re.IGNORECASE),
    re.compile(r"\b(\d{2})\s*(?:in(?:ch(?:es)?)?\s*|\"\s*)?waist\b", re.IGNORECASE),
]

# Shoe sizes: "size 8", "size 8.5", "US 9", "us size 7", "size 8 1/2".
_SHOE_SIZE = re.compile(
    r"\b(?:US\s*(?:size\s*)?|size\s*)(\d{1,2})(?:(\.5)|\s+1/2)?(?![\d.$])",
    re.IGNORECASE,
)


def _parse_size(query: str) -> tuple[str | None, str | None, str | None]:
    """
    Pull one size out of the query.

    Returns (size, kind, matched_text):
      size          the size in the same format the listings use
                    ("W27", "US 8.5", "M"), or None
      kind          "waist", "shoe", "letter", or None
      matched_text  the exact text that was matched, so it can be removed
                    from the description

    Numeric patterns run before the letter pattern, so "size 8" is never read
    as a missing letter size, and the 8 doesn't stay behind as a keyword.
    """
    for pattern in _WAIST_SIZE:
        m = pattern.search(query)
        if m:
            return f"W{m.group(1)}", "waist", m.group(0)

    m = _SHOE_SIZE.search(query)
    if m:
        half = ".5" if (m.group(2) or m.group(0).rstrip().endswith("1/2")) else ""
        return f"US {int(m.group(1))}{half}", "shoe", m.group(0)

    m = _LETTER_SIZE.search(query)
    if m:
        return m.group(1).upper(), "letter", m.group(0)

    return None, None, None


def _ms_since(t: float) -> float:
    return round((time.perf_counter() - t) * 1000, 1)


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    Steps, following the branch rule from Milestone 2:

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)

    t_start = time.perf_counter()

    # Parse the query into description / size / max_price.
    # Capstone extension: numeric sizes (shoe "size 8" / "US 8.5", waist
    # "W27" / "waist 28") are parsed first; letter sizes are the original rule.
    size, size_kind, size_text = _parse_size(query)

    # Parse optional maximum price, for example: "under $30"
    price_match = re.search(
        r"\b(?:under|below|max(?:imum)?(?:\s+price)?)\s*\$?\s*(\d+(?:\.\d+)?)",
        query,
        re.IGNORECASE,
    )
    max_price = float(price_match.group(1)) if price_match else None

    description = query
    if size_text:
        description = description.replace(size_text, " ")
    if price_match:
        description = description.replace(price_match.group(0), " ")

    description = re.sub(r"\s+", " ", description).strip(" ,")
    session["size_kind"] = size_kind

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    session["timings_ms"]["parse"] = _ms_since(t_start)

    trace.check_iterations(1)  # one pass: the loop never goes round again
    trace.step("parse_query", inputs=query, returned=str(session["parsed"]))

    try:
        t = time.perf_counter()
        session["search_results"] = call_tool("search_listings", session["parsed"])
        session["timings_ms"]["search_listings"] = _ms_since(t)
        trace.step("search_listings (via MCP)", inputs=str(session["parsed"]),
                   returned=session["search_results"])

        # The branch: stop immediately when no listing was found.
        if not session["search_results"]:
            size_note = (
                f" Nothing is listed in size {session['parsed']['size']}, so try a "
                f"different size or remove the size."
                if session["parsed"]["size"] else ""
            )
            session["error"] = (
                "No listings matched your search." + size_note + " Try changing the "
                "description, removing the size filter, or increasing the maximum price."
            )
            trace.step("branch", note="search empty, stopping before suggest_outfit")
            return session

        session["selected_item"] = session["search_results"][0]
        trace.step("select_item", returned=session["selected_item"],
                   note="first (best-scoring) result")

        t = time.perf_counter()
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"],
            session["wardrobe"],
        )
        session["timings_ms"]["suggest_outfit"] = _ms_since(t)
        trace.step("suggest_outfit",
                   inputs=f"new_item={session['selected_item']['title']!r}, "
                          f"wardrobe={len(session['wardrobe'].get('items', []))} items",
                   returned=session["outfit_suggestion"])

        t = time.perf_counter()
        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"],
            session["selected_item"],
        )
        session["timings_ms"]["create_fit_card"] = _ms_since(t)
        trace.step("create_fit_card",
                   inputs=f"outfit={len(session['outfit_suggestion'])} chars, "
                          f"new_item={session['selected_item']['title']!r}",
                   returned=session["fit_card"])

    except ModelUnavailable as exc:
        found = session["selected_item"]
        session["error"] = (
            f"The search worked, but the outfit model couldn't be reached, so no outfit "
            f"or fit card was made. {exc}"
            + (f" Best match meanwhile: {found['title']} (${found['price']}, {found['platform']})." if found else "")
        )
        trace.step("error", note=f"ModelUnavailable: {exc}")
    except MCPError as exc:
        session["error"] = (
            "The listing search service (MCP server) couldn't be reached, so nothing was searched. "
            "Run `python mcp_server.py` on its own to see why it won't start, then try again."
        )
        trace.step("error", note=f"MCPError: {str(exc).splitlines()[0]}")

    return session





# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    print("Search results:", len(session["search_results"]))
    print("Selected item:", session["selected_item"])
    print("Outfit suggestion:", session["outfit_suggestion"])
    print("Fit card:", session["fit_card"])
    print("Error:", session["error"])


if __name__ == "__main__":
    wardrobe = {
        "items": [
            "white sneakers",
            "straight-leg jeans",
            "black crossbody bag",
        ]
    }

    print("HAPPY PATH")
    _show(run_agent("vintage graphic tee under $30", wardrobe))

    print("\nEMPTY PATH")
    _show(run_agent("rare astronaut costume under $1", wardrobe))