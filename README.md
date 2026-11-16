# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> The three tools and the planning branch are implemented. The query above
> returns outfit suggestions and a fit card when the model is available.
>
> The first five sections document the Unit 3 build. The sections after the
> Unit 4 marker document the test: run logs, verdicts, trace, and the fix.

---

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr lets a user search thrift listings using a clothing description, size,
and optional maximum price. It selects the best matching listing and uses the
user's wardrobe to suggest an outfit. It then creates a fit card for the
selected item and outfit. If no listings match, the agent stops and explains
that the user should change the search conditions.

---

## Tool Inventory

### `search_listings`

- **What it does:** Searches listings by description keywords, optional size, and optional maximum price.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of listing dictionaries, sorted by keyword relevance, containing `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **Matching rules:** Case-insensitive keyword overlap across title, description, category, style tags, colors, and brand; common stopwords are ignored. Any positive overlap qualifies. Higher scores come first; ties preserve data order. Returns at most `config.SEARCH_RESULT_LIMIT` (10) items. Price is an inclusive ceiling. Sizes match complete slash-separated tokens (M matches S/M, L does not match XL); parenthetical notes are ignored, and one-size items match any requested size.
- **When it has nothing:** Returns an empty list `[]` when no listings match, including descriptions with no searchable keywords.
- **Over MCP (Unit 4):** Registered in `mcp_server.py`; `run_agent()` calls it through `mcp_client.call_tool`. Results are identical to the direct call, including `[]`.

### `suggest_outfit`

- **What it does:** Uses the selected clothing item and the user's wardrobe to suggest one or two outfits.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing outfit suggestions or general styling advice.
- **When it has nothing:** If the wardrobe has no items, returns general styling advice for the selected item.

### `create_fit_card`

- **What it does:** Creates a short social-media-style caption for the selected item and outfit.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A two-to-four sentence string mentioning the item, price, platform, and outfit vibe.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a descriptive message instead of raising an error.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` explaining what the user could change and stop. Otherwise, select the first result and pass it to `suggest_outfit`, then pass the outfit suggestion and selected item to `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regular expressions extract the size and maximum price. The remaining text becomes the description.

**What moves through the session:** The query is parsed into `parsed`; search results go into `search_results`; the first result goes into `selected_item`; the outfit result goes into `outfit_suggestion`; and the final caption goes into `fit_card`.

---

## Sample Run

Captured from terminal runs. Normal runs may reuse cached model responses; the
three-card variation check explicitly disables caching. These are build checks,
not the five-trial Unit 4 acceptance evaluation.

**Full query**

```text
$ python app.py ask 'vintage graphic tee under $30'
Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two practical, Y2K-inspired outfits using the new butterfly baby tee and pieces from your wardrobe:

### Outfit 1: Classic Y2K Streetwear
This look plays on the iconic early 2000s proportion play of a fitted top and baggy bottoms.
* **New Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces Used:**
  * **Baggy straight-leg jeans, dark wash** (w_001)
  * **Chunky white sneakers** (w_007)
  * **Black crossbody bag** (w_010)

### Outfit 2: Edgy Casual Contrast
This outfit tones down the sweetness of the butterfly tee by pairing it with earth tones and utilitarian outerwear, creating a balanced, everyday look.
* **New Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces Used:**
  * **Wide-leg khaki trousers** (w_002)
  * **Vintage black denim jacket** (w_006)
  * **Black combat boots** (w_008)

  Fit card: Channel that early 2000s streetwear energy by pairing this Y2K Baby Tee — Butterfly Print with dark wash baggy jeans and chunky white sneakers. For just $18.0 on depop, it's the ultimate fitted top to balance out relaxed proportions. Grab it now and complete the look with your favorite black crossbody bag!

0 model calls this session, 2 served from cache
```

**search_listings**

```text
$ python -c "from tools import search_listings; print(search_listings('graphic tee', size='M', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]
```

**suggest_outfit**

```text
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two practical, everyday outfits featuring the new Vintage Levi's 501 Jeans:

### Outfit 1: Casual & Cozy Everyday
A relaxed, effortless look that leans into vintage basics. The fitted tank balances the oversized sweater for an easy high-low silhouette.

* **New Item:** Vintage Levi's 501 Jeans — Medium Wash
* **Wardrobe Pieces Used:**
  * White ribbed tank top (`w_003`)
  * Oversized grey crewneck sweatshirt (`w_004`)
  * Chunky white sneakers (`w_007`)
  * Black crossbody bag (`w_010`)

---

### Outfit 2: Edgy Streetwear
A classic denim-and-hoodie combination with sharp contrasts. Layering the cropped hoodie over the vintage wash gives it a cool, urban edge.

* **New Item:** Vintage Levi's 501 Jeans — Medium Wash
* **Wardrobe Pieces Used:**
  * Black cropped zip hoodie (`w_005`)
  * Black combat boots (`w_008`)
  * Brown leather belt (`w_009`)
```

**create_fit_card**

```text
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these Vintage Levi's 501 Jeans in a gorgeous medium wash on depop for just $38! They give off that effortless, off-duty 90s model vibe when paired with a crisp oversized blazer and fresh white sneakers. It's the ultimate everyday look that feels both timeless and completely dialed-in.
```

**Empty search**

```text
$ python app.py ask 'rare astronaut costume under $1'
No listings matched your search. Try changing the description, removing the size filter, or increasing the maximum price.

0 model calls this session
```

**Empty wardrobe**

```text
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_empty_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_empty_wardrobe()))"
Here are two easy, versatile ways to style vintage medium-wash Levi's 501s:

**1. The Classic Casual Look**
* **Top:** A tucked-in, crisp white cotton t-shirt or a relaxed-fit grey crewneck sweatshirt.
* **Footwear:** Classic white canvas sneakers (like Converse or Vans) or retro runners.
* **Accessories:** A simple brown leather belt and a canvas tote bag.
* *Why it works:* It lets the vintage jeans take center stage with an effortless, timeless aesthetic.

**2. Elevated Denim-on-Denim**
* **Top:** A slightly darker or lighter button-down denim shirt worn open over a black baby tee, or fully buttoned and half-tucked.
* **Footwear:** Black leather loafers or ankle boots.
* **Accessories:** A structured black leather belt and minimalist silver jewelry.
* *Why it works:* Playing with different denim shades adds texture and a chic, intentionally styled edge to vintage staples.
```

**Three uncached fit cards**

```text
$ python -c "import config; config.CACHE_ENABLED = False; from tools import create_fit_card; from utils.data_loader import load_listings; cards = [create_fit_card('jeans and white sneakers', load_listings()[0]) for _ in range(3)]; [print(f'Run {i}: {card}') for i, card in enumerate(cards, 1)]; print(f'Unique outputs: {len(set(cards))}/3')"
Run 1: Scored these dreamy Vintage Levi's 501 Jeans in a classic medium wash on depop for just $38! They anchor the ultimate effortless off-duty look when paired with crisp white sneakers and an oversized vintage tee. It's giving cool, timeless everyday comfort that never goes out of style.
Run 2: Scored these Vintage Levi's 501 Jeans in a perfect medium wash on depop for just $38! They bring the ultimate effortlessly cool 90s indie-sleaze aesthetic to your everyday wardrobe. Just pair them with your favorite crisp white sneakers and an oversized vintage tee for a casual, coffee-run-ready vibe.
Run 3: Channeling total 90s off-duty model energy, these Vintage Levi's 501 Jeans—Medium Wash are an absolute must-have. Just style them with a classic baby tee and crisp white sneakers for that effortless weekend look. Snag this dreamy pair on depop right now for only $38.
Unique outputs: 3/3
```

**Local regression check (model calls mocked)**

```text
$ python test_agent.py
PASS: size and price filters, empty cases, session handoff, and early stop (mocked model).
```

---

## How I Used AI

The following two moments came from the final review with Codex.

**Moment 1 — checking the implementation**

- *What I asked for:* I asked Codex to check my completed milestones against the assignment before finishing the write-up.
- *What came back:* It found that `_size_tokens` used `p.strip().upper` instead of `p.strip().upper()`, so size filtering received method objects and could crash. It also checked the successful and empty-search branches and the session handoff.
- *What I changed:* With Codex's help, I added the missing parentheses and added `test_agent.py` to check size boundaries, price filtering, session handoff, and stopping before the model tools on an empty search. These local checks use mocked model outputs and do not claim to be the acceptance evaluation.

**Moment 2 — finishing the submission documentation**

- *What I asked for:* In the same request, I asked Codex to help finish the last milestone, the write-up and submission preparation.
- *What came back:* It identified a missing full-query transcript and abbreviated per-tool commands containing `...`. It ran the commands and also checked an empty wardrobe and three uncached captions for the same input; the three captions were different.
- *What I changed:* With Codex's help, I replaced the placeholders with runnable commands and captured text output, clarified the search rules, and recorded these actual uses of AI. My existing acceptance criteria were left unchanged.

**Moment 3: Unit 4 testing (Claude Code)**

- *What I asked for:* I asked Claude Code to work through the Unit 4 milestones with me: the MCP move, triggering the failure modes, running the evaluation, and the write-up.
- *What came back:* It registered `search_listings` in `mcp_server.py`, added the trace calls and a handler for MCP failures, and wrote `score_run.py`. That script applies my criteria, as written, to every `run_eval.py` try, including an identity check for criterion 3 that the run log alone can't show. It ran the before and after evaluations, diagnosed the criterion 4 miss as the model paraphrasing the title, and proposed a one-line prompt change.
- *What I changed / checked:* I kept the original targets in `criteria.md` unchanged, including the ones that turned out to be easy, and wrote that up as a finding instead of revising them. "Mentions the title" is scored literally, which is why the before run shows a miss.

**Repository for this unit and the next:** https://github.com/xiaogao0616/ai201-project2-fitfindr-starter-v2026

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════ -->

---

## Run Log — Before

Produced by `python score_run.py --label before`, which runs `run_eval.py::main`
(five tries per scenario, caching off, temperature 0.9) and applies each
criterion exactly as written in `criteria.md`. Full output:
`results/run_2026-10-11_2229_before.md`; per-try PASS/FAIL reasons:
`results/scores_before.json`.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item is the dict passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions item title and price | 4 of 5 | FAIL | PASS | FAIL | FAIL | PASS | MISSED (2/5) |
| 5. No returned listing over max_price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Scenarios (`scenarios.py`): c1 `vintage graphic tee under $30`; c2
`designer ballgown size XXS under $5`; c3 `90s track jacket in size M`; c4
`silk slip dress in midi length under $40` (same item all five tries); c5
`vintage jacket under $25`. A sixth, diagnostic scenario (`denim jacket under $50`
with the empty wardrobe) is not one of the five.

**Real output from one try per criterion**, pasted as text. All of it was
produced by `agent.py::run_agent` (tools in `tools.py`, search via
`mcp_server.py::search_listings`), run by `run_eval.py::run_once` and scored by
`score_run.py::score`.

Criterion 1, try 1 (`tools.py::create_fit_card`):

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10
Fit card:
Channel total early-2000s street style by pairing this cropped Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans and chunky white sneakers. Grab it on depop for just $18.0 to instantly nail that effortless, everyday proportion play.
```

Criterion 2, try 1 (the branch in `agent.py::run_agent`):

```
- stopped early: yes — No listings matched your search. Try changing the description, removing the size filter, or increasing the maximum price.
- selected_item: (none)
- search_results: 0
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    search empty, stopping before suggest_outfit
c2 try 1: PASS — suggest_outfit calls=0
```

Criterion 3, try 1 (session in `agent.py::run_agent`, checked by
`score_run.py` wrapping `agent.suggest_outfit` and comparing with `is`):

```
[3] select_item
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    first (best-scoring) result
[4] suggest_outfit
      in:  new_item='90s Track Jacket — Navy/White Stripe', wardrobe=10 items
c3 try 1: PASS — same object
```

Criterion 4, try 1, a FAIL (`tools.py::create_fit_card`):

```
- selected_item: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
Fit card:
Channel your inner 90s icon by pairing this floral silk slip dress with a distressed denim jacket and chunky combat boots. It's the ultimate grunge-meets-feminine contrast for effortless everyday styling. Find it listed on depop for just $30.0!
c4 try 1: FAIL — title=NO, price=yes
```

Criterion 5, try 1 (`mcp_server.py::search_listings` → `tools.py::search_listings`):

```
[1] parse_query
      in:  vintage jacket under $25
      out: {'description': 'vintage jacket', 'size': None, 'max_price': 25.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage jacket', 'size': None, 'max_price': 25.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Oversized Flannel Shirt — Plaid Red/Black, Graphic Tee — 2003 Tour Bootleg Style … +7 more
c5 try 1: PASS — 10 results, max $25.0, over ceiling: 0
```

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | PASS = no `session["error"]` and a non-empty `fit_card`. All five tries returned a card. |
| 2 | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | PASS = `error` set, `suggest_outfit` never called (counted by a wrapper, not read off the trace), and the message names what to change ("Try changing…"). |
| 3 | `selected_item` is the dict passed to `suggest_outfit` | 5 of 5 | MET (5/5) | PASS = `suggest_outfit` was called exactly once, and its `new_item` argument `is` `session["selected_item"]`: the same object, not merely one with an equal title. |
| 4 | Fit card mentions the item's title and price | 4 of 5 | MISSED (2/5) | PASS = the full listing title appears in the card (case-insensitive, dashes and commas ignored) AND the price appears as `$30` or `$30.0`. Paraphrases like "this floral silk slip dress" don't count as the title. 2 PASS is below the target of 4. |
| 5 | No returned listing over `max_price` | 5 of 5 | MET (5/5) | PASS = non-empty results and every `price <= max_price`, checked over all 10 results in the session, not just the 3 the trace shows. |

**Diagnoses**

*Criterion 4: missed, 2 of 5. Place: the model's output. Mechanism: the prompt in `tools.py::create_fit_card`.*
The price appeared in all five cards but the title in only two. In the other
three the model renamed the item: "this floral silk slip dress", "this floral
midi dress", "this floral midi slip dress". The prompt said "Mention the item
title… once" right next to "Do not write a product listing", so the model
treated the title as something to describe in its own words, not to quote.
The search, the session and the tool itself were all fine: the right item
reached the prompt every time (the criterion 3 check confirms it). The only
problem is what the prompt let the model do.

*Pattern.* It isn't specific to this item. The empty-wardrobe diagnostic runs
use a different item (`Denim Jacket — Light Wash, Cropped`), and only 2 of 5
of those cards used the exact title either ("this Light Wash Cropped Denim
Jacket", "this cropped light-wash Denim Jacket"). So it is one cause across
two items: the model paraphrases the title whenever the prompt allows it.

*On the four that were met.* Criteria 1, 2, 3 and 5 don't depend on how the
model words things. The branch, the session handoff and the price filter are
deterministic, so once they worked, 5/5 was close to guaranteed. My
criterion 1 target (4 of 5) was too low: I'd tighten it to 5 of 5 and run it
across several different queries, since the only thing that varies between
tries is the model, and the model never failed to return text. Criterion 5 is
also tested on only one query. A stronger version would check several price
ceilings, including one exactly equal to a listing's price.

*On how I read criterion 4.* "Mentions the title" could be read generously,
since "a floral slip dress" is arguably about the title. I scored the literal
reading, the listing's title text, because that is what makes the card point
to one specific listing. I didn't revise the criterion: it was measurable, and
I simply missed it.

---

## Loop Trace

Captured with `python app.py ask '...' --trace`. The search step goes through
MCP (`mcp_client.call_tool` → `mcp_server.py`) and is labelled `(via MCP)`.

**Happy path** (uncached, try 1 of the before run)

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    first (best-scoring) result
[4] suggest_outfit
      in:  new_item='Y2K Baby Tee — Butterfly Print', wardrobe=10 items
      out: Here is a practical, Y2K-inspired outfit using the new baby tee and pieces from your wardrobe:  **Y2K Streetwe…
[5] create_fit_card
      in:  outfit=646 chars, new_item='Y2K Baby Tee — Butterfly Print'
      out: Channel total early-2000s street style by pairing this cropped Y2K Baby Tee — Butterfly Print with baggy dark-…
```

**Empty search** (stops after step 3 and never reaches the model):

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    search empty, stopping before suggest_outfit

  No listings matched your search. Try changing the description, removing the size filter, or increasing the maximum price.

0 model calls this session
```

### Failure modes, triggered on purpose

**Empty search.** Handled since unit 3 (output above). The message names three things the user can change.

**Empty wardrobe.** `suggest_outfit` already had a prompt for an empty wardrobe. There was no crash and no empty string:

```
$ python app.py ask 'denim jacket under $50' --empty-wardrobe --trace
(running with an empty wardrobe)
...
[4] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped', wardrobe=0 items
      out: Here are two practical, everyday outfit ideas for this light-wash cropped denim jacket:  **1. The Off-Duty Cas…
[5] create_fit_card
      in:  outfit=992 chars, new_item='Denim Jacket — Light Wash, Cropped'
      out: Score this effortless Denim Jacket — Light Wash, Cropped for just $42 on Poshmark! It's the ultimate piece for…
```

**Model unavailable.** I ran it with one character of the key changed. The
bad key was set as an environment variable for that one command, so `.env` was
never edited, and the query wasn't in the cache:

```
$ python app.py ask 'black combat boots for winter'
...
[3] select_item
      out: Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
[4] error
      →    ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

  The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Best match meanwhile: Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp).
```

Before this unit the handler existed, but it said only "The model is
unavailable: …". I changed it to say what still worked and to show the best
match, so the user still gets the listing when the model is down.

**Extra: the MCP server won't start.** I forced this by renaming
`mcp_server.py` for one run. Before, it would have ended in an uncaught
`MCPError` stack trace. Now `run_agent` catches it:

```
  The listing search service (MCP server) couldn't be reached, so nothing was searched. Run `python mcp_server.py` on its own to see why it won't start, then try again.
```

**On the MCP move:** `search_listings` is registered in `mcp_server.py` with
typed inputs (`description: str`, `size: str | None`, `max_price: float | None`,
matching the Tool Inventory). Its description is written for an outside agent:
it states the units, the size-matching rule, the fields each result has, and
that it returns `[]` when nothing matches. In `agent.py::run_agent` the direct
call became `call_tool("search_listings", session["parsed"])`. Nothing behaved
differently: direct and MCP results were identical (`==`) on three queries,
including one that matched nothing, and `test_agent.py` still passes. Two things
did change. Each search now starts a server process, which is a little slower,
and there is a new way for the agent to fail (the server not starting), which
now has its own handler.

---

## The Improvement

**What I changed:** one line of the prompt in `tools.py::create_fit_card`.

```diff
-Mention the item title, its price, and its platform once each. Describe the
+Use the ITEM TITLE below word for word, exactly as written, once; do not
+paraphrase or shorten it. Mention its price and platform once each. Describe the
 outfit vibe specifically. Do not write a product listing or use bullet points.
```

**Which failure it was meant to fix:** criterion 4, where the model paraphrased
the title instead of using it (3 of the 5 tries failed before). Nothing else
changed: same scenarios, same temperature, same model, caching off.

### Run Log — After

`python score_run.py --label after` → `results/run_2026-10-11_2232_after.md`,
`results/scores_after.json`.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item is the dict passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions item title and price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. No returned listing over max_price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Criterion 4, try 2 after the change:

```
Channel your inner 90s grunge-chic aesthetic by layering this floral midi slip dress under a vintage black denim jacket and pairing it with combat boots. It's an effortlessly cool, sweet-meets-edgy look that is totally practical for everyday wear. Snag this 90s Silk Slip Dress — Floral, Midi Length for just $30.0 over on depop before it's gone!
```

**Did it help, and how do I know:** Yes. Criterion 4 went from 2/5 to 5/5, and
no other criterion changed. The empty-wardrobe diagnostic uses a different item
that the prompt wasn't tuned on, and its exact-title count also went from 2/5 to
5/5, so the result isn't a fluke of one listing. The caveat is sample size: ten
cards across two items is evidence, not proof.

---

## What's Still Broken

No criterion is missed after the fix, but that says as much about my targets as
about the agent:

- **Criterion 1's target was too easy.** It asked for 4 of 5 on a step that
  never failed. I'd tighten it to 5 of 5 across several different queries. I
  didn't change it now, because changing a target after seeing the result is
  exactly what this unit warns against. It belongs in the next set of criteria.
- **Prices read like Python floats.** Cards say "$30.0" and "$18.0" because the
  prompt passes `price` straight from the data. My criterion 4 rule accepts
  `$30.0`, so it isn't a miss, but it doesn't read like a real post. The fix is
  to format the price before it goes into the prompt. I didn't make it because
  the unit allows one improvement, and a second change would have muddied the
  before/after comparison.
- **The query parser only knows letter sizes.** `size 8` (shoes) and `W27`
  (denim) aren't extracted. So "platform sneakers size 8" searches with no size
  filter, and the 8 stays in the description. I'd add numeric and waist patterns
  to the regex in `agent.py::run_agent`. That's outside this unit's one change.
- **Each criterion is tested on only one query.** Criteria 3 and 5 especially
  would be stronger across several queries and price ceilings, including a
  price exactly at the ceiling.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

## Capstone

**What This Extends**

FitFindr (project 2): the agent that parses a shopping query, searches
secondhand listings over MCP, suggests an outfit and writes a fit card. What's
new: the query parser and the size filter now understand **numeric sizes**.
Shoe sizes (`size 8`, `size 8.5`, `size 8 1/2`, `US 9`) and waist sizes
(`W27`, `waist 28`, `28 waist`) are pulled out of the query, turned into the
format the listings use (`US 8`, `W28`), and used as a real filter in
`search_listings`. Before this, "platform sneakers size 8" searched with no
size filter at all and left the `8` in the description as a keyword (I listed
this under What's Still Broken in unit 4). When nobody stocks the size, the
empty-search message now names the size. Every request to the HTTP service
also writes a structured log record, and the run is timed per stage.

**The Shape**

Shape C, extend one capability: numeric size parsing and matching.
The capability is `agent.py::_parse_size` (new) plus the size matching in
`tools.py::_size_tokens` / `_size_matches` (changed so `US 8` never matches
`US 8.5`, `W30` matches `W30 L30`, and "One Size" no longer matches a shoe or
waist size). The run path and the log are carried alongside, as every shape
requires.

Out of scope, on purpose:
- I'm not converting between size systems (EU/UK shoe sizes, waist in cm, or
  "M ≈ W30"). Only the US/W forms that already exist in `listings.json`.
- I'm not changing keyword search, ranking, or which listing gets selected.
- I'm not touching the two model prompts (`suggest_outfit`, `create_fit_card`)
  or the price formatting ("$30.0") I noted in unit 4.
- I'm not deploying to a host (Path B only), and not adding a UI.

Stretch, declared before starting: **a latency breakdown** — every log record
carries `timings_ms` for parse, search_listings (MCP), suggest_outfit and
create_fit_card.

**Running It**

Path B, local with logs. One command starts the service: `python serve.py`.
Exact steps, environment and versions are in [RUNNING.md](RUNNING.md) under
"Capstone run path". The test run is `python capstone_eval.py --label before`,
which sends every request through the same `POST /ask` route, so every test
request is also a log record.

**Instrumentation**

Every request to `serve.py::ask` writes one JSON line to `logs/runs.jsonl`
(`runlog.py::write`), including rejected input (400), agent errors and crashes
(500). Fields: `ts`, `request_id`, `status`, `outcome`
(`fit_card` / `empty_search` / `agent_error` / `rejected` / `crash`), `query`
(what came in), `parsed` (description, size, max_price), `size_kind`
(`letter` / `shoe` / `waist`), `n_results`, `result_sizes`, `selected`,
`fit_card` (what went out), `error`, `duration_ms` (end to end), `timings_ms`
(per stage), `model_calls`, `cache_hits`, `prompt_tokens`, `output_tokens`,
`total_tokens` (from Gemini's `usage_metadata`, as a before/after difference of
`generate.token_counts()` around the run).

Read it back with `python runlog.py 12`.

Ten consecutive records from the before run (trial 1: S1–S5, R1–R2, F1–F3),
followed by the real failure from trial 3. Copied from `logs/runs.jsonl`
(committed); only `fit_card` is cut at 140 characters here to keep it readable.
Failed runs among them: two rejected inputs (status 400, `outcome: rejected`),
the injected model outage (`outcome: agent_error`), and the real 503.

Over the whole before session the log holds 40 records: 27 `fit_card`,
3 `empty_search`, 4 `agent_error`, 6 `rejected`, 0 `crash`.

```json
{"ts": "2026-11-16T04:59:24.441+00:00", "request_id": "f5aa848e", "status": 200, "outcome": "fit_card", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": "Level up your late 90s streetwear casual look with these Platform Sneakers — White Chunky Sole, currently listed on poshmark for $48. Paired…", "timings_ms": {"parse": 0.3, "search_listings": 2480.0, "suggest_outfit": 3346.8, "create_fit_card": 763.6}, "error": null, "duration_ms": 6606.6, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1184, "output_tokens": 437, "total_tokens": 1621}
{"ts": "2026-11-16T04:59:31.079+00:00", "request_id": "ba1fb3ea", "status": 200, "outcome": "fit_card", "query": "chelsea boots size 8.5", "parsed": {"description": "chelsea boots", "size": "US 8.5", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8.5"], "selected": {"id": "lst_028", "title": "Suede Chelsea Boots — Tan", "size": "US 8.5", "price": 44.0}, "fit_card": "Pairing a crisp white tank, wide-leg khaki trousers, and a black denim jacket creates the ultimate casual minimalist earth-tone vibe for eve…", "timings_ms": {"parse": 0.0, "search_listings": 1013.9, "suggest_outfit": 1240.4, "create_fit_card": 795.8}, "error": null, "duration_ms": 3076.7, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 985, "output_tokens": 250, "total_tokens": 1235}
{"ts": "2026-11-16T04:59:34.188+00:00", "request_id": "b8109d36", "status": 200, "outcome": "fit_card", "query": "high-waisted denim shorts W27", "parsed": {"description": "high-waisted denim shorts", "size": "W27", "max_price": null}, "size_kind": "waist", "n_results": 1, "result_sizes": ["W27"], "selected": {"id": "lst_016", "title": "High-Waisted Denim Shorts — Cutoff", "size": "W27", "price": 24.0}, "fit_card": "Channel an effortless grunge-meets-summer vibe by pairing these High-Waisted Denim Shorts — Cutoff with a vintage black jacket and chunky co…", "timings_ms": {"parse": 0.0, "search_listings": 960.9, "suggest_outfit": 1378.2, "create_fit_card": 1231.2}, "error": null, "duration_ms": 3574.1, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1116, "output_tokens": 378, "total_tokens": 1494}
{"ts": "2026-11-16T04:59:37.786+00:00", "request_id": "506e06fb", "status": 200, "outcome": "fit_card", "query": "straight leg black jeans waist 28", "parsed": {"description": "straight leg black jeans", "size": "W28", "max_price": null}, "size_kind": "waist", "n_results": 2, "result_sizes": ["W28", "W28"], "selected": {"id": "lst_037", "title": "Straight Leg Black Jeans — Faded", "size": "W28", "price": 30.0}, "fit_card": "Score these Straight Leg Black Jeans — Faded for just $30.0 on thredUp! They are perfect for building a sleek, monochrome edge look with a b…", "timings_ms": {"parse": 0.0, "search_listings": 1473.8, "suggest_outfit": 1048.7, "create_fit_card": 724.7}, "error": null, "duration_ms": 3259.0, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1023, "output_tokens": 283, "total_tokens": 1306}
{"ts": "2026-11-16T04:59:41.057+00:00", "request_id": "c56733d9", "status": 200, "outcome": "empty_search", "query": "canvas sneakers size 12", "parsed": {"description": "canvas sneakers", "size": "US 12", "max_price": null}, "size_kind": "shoe", "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 1405.9}, "error": "No listings matched your search. Nothing is listed in size US 12, so try a different size or remove the size. Try changing the description, removing the size filter, or increasing the maximum price.", "duration_ms": 1408.4, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T04:59:42.474+00:00", "request_id": "649099da", "status": 200, "outcome": "fit_card", "query": "vintage graphic tee under $30, size M", "parsed": {"description": "vintage graphic tee", "size": "M", "max_price": 30.0}, "size_kind": "letter", "n_results": 10, "result_sizes": ["S/M", "S/M", "M", "One Size (adjustable)", "M", "M", "M", "M", "One Size", "M"], "selected": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "size": "S/M", "price": 18.0}, "fit_card": "Embrace early 2000s nostalgia with this Y2K Baby Tee — Butterfly Print, listed on depop for just $18.0! It's perfect for styling into classi…", "timings_ms": {"parse": 0.0, "search_listings": 896.5, "suggest_outfit": 1187.6, "create_fit_card": 876.9}, "error": null, "duration_ms": 2963.1, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1058, "output_tokens": 336, "total_tokens": 1394}
{"ts": "2026-11-16T04:59:45.449+00:00", "request_id": "7b88cf28", "status": 200, "outcome": "fit_card", "query": "vintage jacket under $25", "parsed": {"description": "vintage jacket", "size": null, "max_price": 25.0}, "size_kind": null, "n_results": 10, "result_sizes": ["S/M", "XL (oversized)", "L", "XL (fits oversized)", "One Size (adjustable)", "W27", "M", "M", "XL", "M"], "selected": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "size": "S/M", "price": 18.0}, "fit_card": "Channel your inner 2000s icon with this Y2K Streetwear Casual look, featuring the **Y2K Baby Tee — Butterfly Print** paired with baggy dark-…", "timings_ms": {"parse": 0.0, "search_listings": 881.9, "suggest_outfit": 1051.2, "create_fit_card": 717.2}, "error": null, "duration_ms": 2652.8, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 996, "output_tokens": 266, "total_tokens": 1262}
{"ts": "2026-11-16T04:59:48.138+00:00", "request_id": "064187b2", "status": 400, "outcome": "rejected", "query": "   ", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T04:59:48.160+00:00", "request_id": "705a1162", "status": 400, "outcome": "rejected", "query": "query=sneakers", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T04:59:48.170+00:00", "request_id": "7ae40ea6", "status": 200, "outcome": "agent_error", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 863.9}, "error": "The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Injected for testing: the model API is unreachable. Best match meanwhile: Platform Sneakers — White Chunky Sole ($48.0, poshmark).", "duration_ms": 865.8, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:01:25.668+00:00", "request_id": "26fb8f24", "status": 200, "outcome": "agent_error", "query": "high-waisted denim shorts W27", "parsed": {"description": "high-waisted denim shorts", "size": "W27", "max_price": null}, "size_kind": "waist", "n_results": 1, "result_sizes": ["W27"], "selected": {"id": "lst_016", "title": "High-Waisted Denim Shorts — Cutoff", "size": "W27", "price": 24.0}, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 877.3}, "error": "The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} Best match meanwhile: High-Waisted Denim Shorts — Cutoff ($24.0, poshmark).", "duration_ms": 36921.5, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```

**What It Costs**

**Measured: 1,391.9 tokens per run on average (1,067.7 prompt + 324.2
output), 2 model requests per run, median 3.46 s end to end.** Range over the
ten runs: 1,183 to 1,693 tokens. All 10 runs succeeded.

Method: `python capstone_eval.py --cost 10` sent `platform sneakers size 8`
ten times through `POST /ask` (`serve.py::ask`) with the cache off. Each run's
tokens are the difference in `generate.token_counts()` before and after that
run, which is what the Gemini API reported in `usage_metadata` for the two
calls (`suggest_outfit` and `create_fit_card`), not a number from the pricing
page. Raw numbers per run: `results/capstone_cost_2026-11-16_0002.json`.

The mean duration was 7.19 s, but that mean is pulled up by one run (run 8,
38.8 s) that waited 35 s in `generate.py`'s own per-minute limiter
(15 requests/minute). The median, 3.46 s, is the honest "one run" number.

A hundred people a day, one query each:
1,391.9 tokens × 100 = **139,190 tokens/day**, and 2 requests × 100 =
**200 model requests/day**. On the free Gemini tier this course uses, that is
$0. The limit that bites first is not money but the per-minute cap: 100 people
spread over a day is far under 15 requests/minute, but 8 people arriving in the
same minute (16 requests) would already make someone wait.

**Latency breakdown (stretch)** — mean per stage over the same ten runs, from
`timings_ms` in each log record: parse 0.0 ms · search_listings (via MCP)
1,155 ms · suggest_outfit 1,437 ms · create_fit_card 4,592 ms. The
create_fit_card mean includes run 8's 35 s limiter wait; without it the two
model calls take about the same time. The surprise is search: matching 40
listings in Python takes almost nothing, so almost all of its 1.2 s must be starting
`mcp_server.py` as a new process for every call (`mcp_client.call_tool`).
**Which stage dominates:** the two model calls. Together they take
1,437 + 4,592 = 6,029 ms of the 7,184 ms summed across stages (84%), and even
with run 8's limiter wait taken out they are still most of every run. Parsing
is free, and search (~1.2 s) comes third.

**Run Log and Verdicts**

Criteria are in `criteria.md` under "Capstone criteria", committed before any
results (`add capstone criteria`, then `capstone first results (before)`).
Run with `python capstone_eval.py --label before`; every request went through
`serve.py::ask` and was logged by `runlog.py::write`. Full output:
`results/capstone_before_2026-11-15_2359.md` and `.json`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Numeric sizes parsed to the right value (S1–S5) | 5 of 5 each run | 5/5 | 5/5 | 5/5 | MET |
| 2. Every returned listing matches the numeric size (S1–S4) | 4 of 4 each run | 4/4 | 4/4 | 4/4 | MET |
| 3. Unstocked size stops early and names the size (S5) | 1 of 1 each run | 1/1 | 1/1 | 1/1 | MET |
| 4. Original queries still parse and end in a fit card (R1–R2) | at least 1 of 2 each run | 2/2 | 2/2 | 2/2 | MET |
| 5. Malformed requests get 400, not 500 (F1–F2) | 2 of 2 each run | 2/2 | 2/2 | 2/2 | MET |

Measured alongside (not criteria): numeric-size query ends in a fit card
4/4, 4/4, **3/4**; model-down request (F3) handled without a crash 1/1 in
every run; every request left a log record 10/10 in every run; runs under
10 s 6/6, **5/6**, **5/6**.

Real output, from run 1 (`capstone_eval.py` → `serve.py::ask` →
`agent.py::run_agent`, trace from `trace.py::step`):

*Criterion 1 and 2* — parse and search for S2 (`agent.py::_parse_size`,
`tools.py::search_listings` via MCP):
```
[6] parse_query
      in:  chelsea boots size 8.5
      out: {'description': 'chelsea boots', 'size': 'US 8.5', 'max_price': None}
[7] search_listings (via MCP)
      in:  {'description': 'chelsea boots', 'size': 'US 8.5', 'max_price': None}
      out: 1 items: Suede Chelsea Boots — Tan
```
and S4, where the word form "waist 28" becomes `W28` and both returned
listings are W28:
```
[16] parse_query
      in:  straight leg black jeans waist 28
      out: {'description': 'straight leg black jeans', 'size': 'W28', 'max_price': None}
[17] search_listings (via MCP)
      out: 2 items: Straight Leg Black Jeans — Faded, Corduroy Wide-Leg Pants — Rust
```

*Criterion 3* — S5 (`agent.py::run_agent`, the empty-search branch):
```
[21] parse_query
      in:  canvas sneakers size 12
      out: {'description': 'canvas sneakers', 'size': 'US 12', 'max_price': None}
[22] search_listings (via MCP)
      out: [] (empty)
[23] branch
      →    search empty, stopping before suggest_outfit
  S5 numeric size nobody stocks: status 200, size US 12, 0 results, card=False, 1408.4 ms
```

*Criterion 4* — R1, the unit 3 query, still parsed as a letter size and
finished with a fit card:
```
[24] parse_query
      in:  vintage graphic tee under $30, size M
      out: {'description': 'vintage graphic tee', 'size': 'M', 'max_price': 30.0}
[28] create_fit_card
      out: Embrace early 2000s nostalgia with this Y2K Baby Tee — Butterfly Print, listed on depop for just $18.0! It's p…
  R1 letter size + price (unit 3 query): status 200, size M, 10 results, card=True, 2963.1 ms
```

*Criterion 5* — F1 and F2 (`serve.py::ask`, rejected before the agent runs):
```
  F1 empty query: status 400, size None, 0 results, card=False, 0.1 ms
  F2 body is not JSON: status 400, size None, 0 results, card=False, 0.1 ms
```

**Diagnosis.** No criterion was missed, so there is no miss to diagnose. But
I have to be honest about why. Criteria 1, 2, 3 and 5 test plain code (a
regex, a set comparison, an `if not results`, a 400 check). Code like that
gives the same answer every time, so once it was right in trial 1 it was
always going to be right in trials 2 and 3. Three trials can't show variation
there, only whether the code is right. **Criterion 4's target was set too
low.** "At least 1 of 2" would have passed even if one of the two original
queries had been broken by my change. It came out 2/2 every time, so I would
tighten it to **2 of 2 in every run**, and add more original queries.

**The failure that did happen was outside my five criteria.** In run 3, S3
(`high-waisted denim shorts W27`) parsed and searched correctly but got no
fit card:
```
[87] select_item
      out: High-Waisted Denim Shorts — Cutoff ($24.0, poshmark)
  [rate limit] 15 requests used this minute. Waiting 35s. This is normal.
[88] error
      →    ModelUnavailable: Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}
  S3 waist, W-form: status 200, size W27, 1 results, card=False, 36921.5 ms
```
*Stage:* the model call in `generate.py::generate`. *Mechanism:* the retry
loop only retries when the error looks like a rate limit (429 / "resource
exhausted" / "rate limit"). A 503 "high demand" is just as temporary (the
message itself says "try again later"), but it fell into the
`if not rate_limited: raise ModelUnavailable` branch on the **first**
attempt. So one busy second at Google cost the user their fit card. The agent
handled it correctly (status 200, a message naming the listing, no crash),
but the run failed when it didn't need to.

The two slow runs have a separate cause: run 2 S1 (72.7 s) waited 9 s + 60 s
on two 429s from the service, and run 3 S3 (36.9 s) waited 35 s in our own
15-requests-per-minute limiter. Both are the rate limiter working as designed
when a test sends ~20 requests a minute.

**The Improvement**

*What I changed:* `generate.py::generate` now treats a 503 "UNAVAILABLE /
high demand" error as temporary and retries it with a short backoff (2 s,
4 s, 8 s, capped at 10 s, up to `MAX_RETRIES` = 5 attempts). Only when every
attempt fails does it raise `ModelUnavailable`. A bad key or any other error
still fails on the first attempt, as before.

*Why:* it follows the diagnosis above. The one run that failed in the before
set (run 3, S3) failed because a 503 was treated like a dead key.

*How I measured it:* a real 503 is random, so re-running the same five
criteria can't show whether the fix helped. Google just might not be busy.
So I added scenario **F4** to `capstone_eval.py`: the model API answers
`503 UNAVAILABLE ... high demand` on the first call and then behaves normally
(the client is wrapped in `run_scenario`; everything else is the real API).
F4 is new in the after run, so it has no before column. Without the fix it
would have ended exactly like the real S3 failure. The next step after the
503 is `raise ModelUnavailable`, and F3 shows that path in every run.

Run with `python capstone_eval.py --label after`. Full output:
`results/capstone_after_2026-11-16_0009.md` and `.json`.

After run log, in the same format as the before run log:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Numeric sizes parsed to the right value (S1–S5) | 5 of 5 each run | 5/5 | 5/5 | 5/5 | MET |
| 2. Every returned listing matches the numeric size (S1–S4) | 4 of 4 each run | 4/4 | 4/4 | 4/4 | MET |
| 3. Unstocked size stops early and names the size (S5) | 1 of 1 each run | 1/1 | 1/1 | 1/1 | MET |
| 4. Original queries still parse and end in a fit card (R1–R2) | at least 1 of 2 each run | 2/2 | 2/2 | 2/2 | MET |
| 5. Malformed requests get 400, not 500 (F1–F2) | 2 of 2 each run | 2/2 | 2/2 | 2/2 | MET |

Side by side with the before run, plus the measurements that aren't criteria:

| Criterion | Target | Before 1 | Before 2 | Before 3 | After 1 | After 2 | After 3 | Before → After |
|---|---|---|---|---|---|---|---|---|
| 1. Numeric sizes parsed right | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET → MET |
| 2. Returned listings match size | 4 of 4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | MET → MET |
| 3. Unstocked size stops, names it | 1 of 1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | MET → MET |
| 4. Original queries still work | ≥ 1 of 2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | MET → MET |
| 5. Malformed request → 400 | 2 of 2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | MET → MET |
| *F4. Model busy once → still a fit card* | 1 of 1 | — | — | — | 1/1 | 1/1 | 1/1 | new |
| *Numeric-size query ends in a fit card* | — | 4/4 | 4/4 | 3/4 | 4/4 | 4/4 | 4/4 | |
| *Every request logged* | — | 10/10 | 10/10 | 10/10 | 11/11 | 11/11 | 11/11 | |
| *Runs under 10 s (S1–S4, R1–R2)* | — | 6/6 | 5/6 | 5/6 | 6/6 | 6/6 | 6/6 | |

Real output from after run 1, F4 (`capstone_eval.py::run_scenario` →
`serve.py::ask` → `agent.py::run_agent` → `generate.py::generate`):
```
[40] select_item
      out: Platform Sneakers — White Chunky Sole ($48.0, poshmark)
  [busy] the model service is overloaded (503). Waiting 2s and trying again (attempt 1 of 5).
[41] suggest_outfit
      out: Here are two practical outfit ideas incorporating the new **Platform Sneakers** and pieces from your wardrobe:…
  [rate limit] service pushed back. Waiting 41s (attempt 1 of 5). This is the limiter doing its job, not a bug.
[42] create_fit_card
      out: Channel ultimate late '90s streetwear energy by styling these Platform Sneakers — White Chunky Sole with baggy…
  F4 model busy once (503 injected), then recovers: status 200, size US 8, 1 results, card=True, 46434.0 ms
```

*Did it help?* Yes, for the failure it was aimed at. A single 503 now costs
the user 2 seconds instead of their fit card: F4 is 1/1 in all three runs. The
five criteria didn't move because they were all already MET. The return of
"numeric-size query ends in a fit card" to 4/4 in every run is **not** proof
of the fix: no real 503 happened during the after run, so that row says only
that Google wasn't busy. F4 is the evidence. *The trade:* a request that would
have failed fast after a 503 now waits up to 2 + 4 + 8 + 10 = 24 s before
giving up. F4's own durations (38–46 s) are mostly the per-minute limiter,
not the retry: the 503 wait was 2 s each time.

**What's Still Broken**

No criterion is missed, so the honest part is which targets were too easy:
- **Criterion 4 was set too low.** "At least 1 of 2" would pass even if my
  change broke one of the two original queries. It was 2/2 in all six runs.
  I'd tighten it to **2 of 2 in every run**, across more original queries
  (the unit 3 and unit 4 scenarios too).
- **Criteria 1, 2, 3 and 5 test plain code**, so three trials only show the
  code is right, not that it holds up under variation. I'd make them harder,
  not stricter: more numeric forms (`sz 8`, `8.5 US`, `W 30 L 32`, `size 10W`,
  which I never tested), and a query with both a waist and an inseam.

Still broken in the system:
- **Running out of 429 retries still crashes.** When the service keeps saying
  "rate limited" for all 5 attempts, `generate.py` raises `RuntimeError`, not
  `ModelUnavailable`. The agent doesn't catch that, so `serve.py` returns a
  500. My fix made 503s safe, but the same gap is still there for 429s. I
  didn't fix it because the unit allows one improvement, and I couldn't
  trigger it in a test run without waiting out the real quota.
- **Search spends ~1.2 s starting a process.** `mcp_client.call_tool` starts
  `mcp_server.py` again for every call. Searching 40 listings takes almost
  nothing, so almost all of that second is startup.
- **No size conversion.** "W30" and "size M" don't know about each other, and
  EU/UK shoe sizes aren't parsed. That was out of scope on purpose.

*Why I stopped:* the unit asks for one improvement measured against the same
criteria, and a second change would have mixed up the before/after
comparison.

*The one thing I'd do first with another unit:* make running out of 429
retries end as `ModelUnavailable` instead of a 500, so every model failure
gets the same user-facing message. It is now the only path I know of where a
user gets a crash instead of a sentence, and it shows up exactly when the
service is under the most load.

**How I Used AI**

**Moment 1: Choosing the project**
- *What I asked:* I gave Claude the assignment and asked which project I should pick.
- *What it gave me:* It recommended FitFindr with numeric sizes.
- *What I changed:* Nothing. I agreed it was a good fit and went with it.

**Moment 2: Writing the acceptance criteria**
- *What I asked:* I asked Claude for help writing my criteria.
- *What it gave me:* Instead of writing them for me, it had me choose the metrics, set the targets, and explain my reasons myself, and then it helped me turn my notes into English.
- *What I changed:* For A2, I first thought the search didn't need to be right every time. Then I realized the size filter is a straight comparison against the listings data with no model involved, so each query has one clear correct answer, and even one wrong-size listing means showing the user something they can't wear. So I raised the target to 4 out of 4 in every trial.

**What Claude wrote and what I did**

To be clear about authorship: Claude wrote most of the code and most of this README. That includes the extension code (numeric size parsing and matching), the structured logging, `capstone_eval.py`, the improved 503 retry handling, and most of the Capstone section of this README.

My part was deciding what the system had to achieve and checking whether it did. I chose the metrics, targets, and reasoning for each criterion in `criteria.md`. I ran every test myself on my own computer, reviewed the results, and decided what to submit.
