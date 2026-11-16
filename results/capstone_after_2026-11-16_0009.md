# Capstone run — after

2026-11-16T00:13 · model `gemini-3.5-flash-lite` · temperature 0.9 · cache OFF · 3 trials · produced by `capstone_eval.py` through `serve.py::ask`

## Summary (counts per trial)

| Measurement | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|
| Numeric size parsed to the right value (S1–S5) | 5/5 | 5/5 | 5/5 |
| Size text removed from the description (S1–S5) | 5/5 | 5/5 | 5/5 |
| Every returned listing matches the numeric size (S1–S4, needs ≥1 result) | 4/4 | 4/4 | 4/4 |
| Numeric-size query ends in a fit card (S1–S4) | 4/4 | 4/4 | 4/4 |
| Unstocked size stops early AND the message names the size (S5) | 1/1 | 1/1 | 1/1 |
| Regression queries still parse and finish with a fit card (R1–R2) | 2/2 | 2/2 | 2/2 |
| Bad input gets a 400, not a 500 (F1–F2) | 2/2 | 2/2 | 2/2 |
| Model down: 200 + error naming the found listing, no crash (F3) | 1/1 | 1/1 | 1/1 |
| Model busy once (503): still ends in a fit card (F4, after run only) | 1/1 | 1/1 | 1/1 |
| Every request left a log record (all) | 11/11 | 11/11 | 11/11 |
| Runs under 10 s end to end (S1–S4, R1–R2) | 6/6 | 6/6 | 6/6 |

## Trial 1

| ID | Query | Status | Parsed size | Size right | Size text left | Results | All match size | Fit card | Error names size | ms | Tokens | Logged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 5149.6 | 1271 | yes |
| S2 | `chelsea boots size 8.5` | 200 | US 8.5 | yes | **NO** | 1 | yes | yes | – | 3645.2 | 1351 | yes |
| S3 | `high-waisted denim shorts W27` | 200 | W27 | yes | **NO** | 1 | yes | yes | – | 2649.0 | 1247 | yes |
| S4 | `straight leg black jeans waist 28` | 200 | W28 | yes | **NO** | 2 | yes | yes | – | 4104.9 | 1514 | yes |
| S5 | `canvas sneakers size 12` | 200 | US 12 | yes | **NO** | 0 | – | **NO** | yes | 880.6 | 0 | yes |
| R1 | `vintage graphic tee under $30, size M` | 200 | M | yes | **NO** | 10 | yes | yes | – | 2611.3 | 1259 | yes |
| R2 | `vintage jacket under $25` | 200 | – | yes | – | 10 | – | yes | – | 2912.0 | 1249 | yes |
| F1 | `{"query": "   "}` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F2 | `query=sneakers` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F3 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | **NO** | – | 749.6 | 0 | yes |
| F4 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 46434.0 | 1639 | yes |

## Trial 2

| ID | Query | Status | Parsed size | Size right | Size text left | Results | All match size | Fit card | Error names size | ms | Tokens | Logged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 2878.9 | 1581 | yes |
| S2 | `chelsea boots size 8.5` | 200 | US 8.5 | yes | **NO** | 1 | yes | yes | – | 3513.7 | 1593 | yes |
| S3 | `high-waisted denim shorts W27` | 200 | W27 | yes | **NO** | 1 | yes | yes | – | 3255.2 | 1286 | yes |
| S4 | `straight leg black jeans waist 28` | 200 | W28 | yes | **NO** | 2 | yes | yes | – | 3343.0 | 1525 | yes |
| S5 | `canvas sneakers size 12` | 200 | US 12 | yes | **NO** | 0 | – | **NO** | yes | 768.6 | 0 | yes |
| R1 | `vintage graphic tee under $30, size M` | 200 | M | yes | **NO** | 10 | yes | yes | – | 2907.2 | 1177 | yes |
| R2 | `vintage jacket under $25` | 200 | – | yes | – | 10 | – | yes | – | 2331.5 | 1216 | yes |
| F1 | `{"query": "   "}` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F2 | `query=sneakers` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F3 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | **NO** | – | 737.0 | 0 | yes |
| F4 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 39968.7 | 1399 | yes |

## Trial 3

| ID | Query | Status | Parsed size | Size right | Size text left | Results | All match size | Fit card | Error names size | ms | Tokens | Logged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 3180.7 | 1350 | yes |
| S2 | `chelsea boots size 8.5` | 200 | US 8.5 | yes | **NO** | 1 | yes | yes | – | 2691.0 | 1273 | yes |
| S3 | `high-waisted denim shorts W27` | 200 | W27 | yes | **NO** | 1 | yes | yes | – | 3793.9 | 1230 | yes |
| S4 | `straight leg black jeans waist 28` | 200 | W28 | yes | **NO** | 2 | yes | yes | – | 3434.7 | 1499 | yes |
| S5 | `canvas sneakers size 12` | 200 | US 12 | yes | **NO** | 0 | – | **NO** | yes | 825.0 | 0 | yes |
| R1 | `vintage graphic tee under $30, size M` | 200 | M | yes | **NO** | 10 | yes | yes | – | 3653.3 | 1178 | yes |
| R2 | `vintage jacket under $25` | 200 | – | yes | – | 10 | – | yes | – | 3438.4 | 1409 | yes |
| F1 | `{"query": "   "}` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F2 | `query=sneakers` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F3 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | **NO** | – | 821.4 | 0 | yes |
| F4 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 38171.5 | 1389 | yes |

## Fit cards and errors (trial 1)

**S1 — shoe size, whole**

```
Serve up some late-90s energy with these Platform Sneakers — White Chunky Sole, available now on poshmark for $48. Pair them with a baggy dark wash denim and a black cropped zip hoodie for the ultimate Y2K streetwear casual look. It's an effortlessly cool, everyday outfit formula you'll reach for on repeat!
```

**S2 — shoe size, half**

```
Snag these Suede Chelsea Boots — Tan on Poshmark for just $44 to instantly elevate your wardrobe. They are the star of this effortless casual minimalist earth-tone look, paired with wide-leg khakis, a crisp white tank, and a vintage black denim jacket. It's a relaxed, cohesive outfit with a cool structural edge that's perfect for everyday errands or casual meetups.
```

**S3 — waist, W-form**

```
Channel that effortless casual streetwear summer energy by pairing your new High-Waisted Denim Shorts — Cutoff with a tucked-in ribbed tank and chunky sneakers. You can easily score these on poshmark for just 24.0, making them a total warm-weather staple. Toss on an oversized grey crewneck and a black crossbody bag to complete the ultimate comfy, proportion-play look for breezy days.
```

**S4 — waist, word form**

```
Score these Straight Leg Black Jeans — Faded for just $30.0 on thredUp to nail that cozy streetwear aesthetic. I love styling them with an oversized grey crewneck and chunky white sneakers for the ultimate relaxed, everyday vibe.
```

**S5 — numeric size nobody stocks**

```
No listings matched your search. Nothing is listed in size US 12, so try a different size or remove the size. Try changing the description, removing the size filter, or increasing the maximum price.
```

**R1 — letter size + price (unit 3 query)**

```
Channel ultimate early 2000s proportion play by pairing the Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans and chunky white sneakers for a nostalgic streetwear fit. Grab this fitted cropped tee right now on depop for just $18.0 to complete your effortless everyday look.
```

**R2 — no size at all**

```
Channel your inner early-2000s icon by pairing this Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans and chunky white sneakers for an effortless everyday streetwear vibe. It's listed on depop right now for just $18.0!
```

**F1 — empty query**

```
Send JSON with a 'query' field, e.g. {"query": "vintage graphic tee under $30"}
```

**F2 — body is not JSON**

```
Send JSON with a 'query' field, e.g. {"query": "vintage graphic tee under $30"}
```

**F3 — model unreachable (fault injected)**

```
The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Injected for testing: the model API is unreachable. Best match meanwhile: Platform Sneakers — White Chunky Sole ($48.0, poshmark).
```

**F4 — model busy once (503 injected), then recovers**

```
Channel ultimate late '90s streetwear energy by styling these Platform Sneakers — White Chunky Sole with baggy dark-wash jeans, a ribbed tank, and a cropped zip hoodie. I just listed this chunky white pair on Poshmark for $48, and they are ready to elevate your everyday casual rotation.
```

## Log records from this run (`logs/runs.jsonl`, last 12)

```json
{"ts": "2026-11-16T05:11:22.026+00:00", "request_id": "8f6e2007", "status": 200, "outcome": "fit_card", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": "Channel ultimate Y2K streetwear energy or cozy minimal vibes with these sweet Platform Sneakers — White Chunky Sole. Grab them over on poshmark for just $48.0 to easily elevate your everyday baggy denim and oversized hoodie looks!", "timings_ms": {"parse": 0.0, "search_listings": 700.0, "suggest_outfit": 3133.9, "create_fit_card": 36131.3}, "error": null, "duration_ms": 39968.7, "model_calls": 3, "cache_hits": 0, "prompt_tokens": 1076, "output_tokens": 323, "total_tokens": 1399}
{"ts": "2026-11-16T05:12:02.054+00:00", "request_id": "505e0c38", "status": 200, "outcome": "fit_card", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": "Grab these Platform Sneakers — White Chunky Sole on Poshmark for just $48 to instantly nail a late '90s Y2K streetwear vibe. They look amazing peeking out beneath baggy dark-wash jeans and a cropped zip hoodie for an effortless, on-the-go everyday fit.", "timings_ms": {"parse": 0.0, "search_listings": 746.6, "suggest_outfit": 1351.5, "create_fit_card": 1069.5}, "error": null, "duration_ms": 3180.7, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1044, "output_tokens": 306, "total_tokens": 1350}
{"ts": "2026-11-16T05:12:05.256+00:00", "request_id": "09248d7e", "status": 200, "outcome": "fit_card", "query": "chelsea boots size 8.5", "parsed": {"description": "chelsea boots", "size": "US 8.5", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8.5"], "selected": {"id": "lst_028", "title": "Suede Chelsea Boots — Tan", "size": "US 8.5", "price": 44.0}, "fit_card": "Scored these gorgeous Suede Chelsea Boots — Tan on Poshmark for just $44! They are the ultimate anchor for a casual minimalist earth-tone vibe, especially when paired with wide-leg khaki trousers and a structured vintage black denim jacket.", "timings_ms": {"parse": 0.0, "search_listings": 713.0, "suggest_outfit": 1353.8, "create_fit_card": 614.2}, "error": null, "duration_ms": 2691.0, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1010, "output_tokens": 263, "total_tokens": 1273}
{"ts": "2026-11-16T05:12:07.966+00:00", "request_id": "12d06978", "status": 200, "outcome": "fit_card", "query": "high-waisted denim shorts W27", "parsed": {"description": "high-waisted denim shorts", "size": "W27", "max_price": null}, "size_kind": "waist", "n_results": 1, "result_sizes": ["W27"], "selected": {"id": "lst_016", "title": "High-Waisted Denim Shorts — Cutoff", "size": "W27", "price": 24.0}, "fit_card": "Channel that casual streetwear summer vibe by pairing your new High-Waisted Denim Shorts — Cutoff with a ribbed white tank, a cropped zip hoodie, and fresh chunky sneakers. This effortless, sporty look is currently listed on poshmark for just $24.0, making it the ultimate warm-weather staple for your everyday wardrobe.", "timings_ms": {"parse": 0.0, "search_listings": 795.8, "suggest_outfit": 1743.4, "create_fit_card": 1251.8}, "error": null, "duration_ms": 3793.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 983, "output_tokens": 247, "total_tokens": 1230}
{"ts": "2026-11-16T05:12:11.778+00:00", "request_id": "29a61c38", "status": 200, "outcome": "fit_card", "query": "straight leg black jeans waist 28", "parsed": {"description": "straight leg black jeans", "size": "W28", "max_price": null}, "size_kind": "waist", "n_results": 2, "result_sizes": ["W28", "W28"], "selected": {"id": "lst_037", "title": "Straight Leg Black Jeans — Faded", "size": "W28", "price": 30.0}, "fit_card": "Score these Straight Leg Black Jeans — Faded for just $30.0 on thredUp to nail that laid-back streetwear aesthetic. They’re super easy to style with an oversized grey crewneck and chunky white sneakers for a cozy, everyday monochromatic fit.", "timings_ms": {"parse": 0.0, "search_listings": 798.7, "suggest_outfit": 1717.4, "create_fit_card": 912.5}, "error": null, "duration_ms": 3434.7, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1122, "output_tokens": 377, "total_tokens": 1499}
{"ts": "2026-11-16T05:12:15.232+00:00", "request_id": "0cc416f3", "status": 200, "outcome": "empty_search", "query": "canvas sneakers size 12", "parsed": {"description": "canvas sneakers", "size": "US 12", "max_price": null}, "size_kind": "shoe", "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 818.4}, "error": "No listings matched your search. Nothing is listed in size US 12, so try a different size or remove the size. Try changing the description, removing the size filter, or increasing the maximum price.", "duration_ms": 825.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:12:16.073+00:00", "request_id": "e53be81f", "status": 200, "outcome": "fit_card", "query": "vintage graphic tee under $30, size M", "parsed": {"description": "vintage graphic tee", "size": "M", "max_price": 30.0}, "size_kind": "letter", "n_results": 10, "result_sizes": ["S/M", "S/M", "M", "One Size (adjustable)", "M", "M", "M", "M", "One Size", "M"], "selected": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "size": "S/M", "price": 18.0}, "fit_card": "Nostalgic early 2000s proportions come alive in this effortless Y2K Streetwear Casual look, blending fitted silhouettes with voluminous dark wash denim and chunky white sneakers. Grab this Y2K Baby Tee — Butterfly Print on depop for just $18.0 to easily nail that laid-back, everyday aesthetic.", "timings_ms": {"parse": 0.0, "search_listings": 812.9, "suggest_outfit": 1157.4, "create_fit_card": 1675.9}, "error": null, "duration_ms": 3653.3, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 955, "output_tokens": 223, "total_tokens": 1178}
{"ts": "2026-11-16T05:12:19.754+00:00", "request_id": "b8e0d2d6", "status": 200, "outcome": "fit_card", "query": "vintage jacket under $25", "parsed": {"description": "vintage jacket", "size": null, "max_price": 25.0}, "size_kind": null, "n_results": 10, "result_sizes": ["S/M", "XL (oversized)", "L", "XL (fits oversized)", "One Size (adjustable)", "W27", "M", "M", "XL", "M"], "selected": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "size": "S/M", "price": 18.0}, "fit_card": "Channel early 2000s streetwear by pairing the Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans and chunky sneakers for the ultimate nostalgic proportion play. This playful, girly pastel graphic is now available on depop for just $18.0!", "timings_ms": {"parse": 0.0, "search_listings": 937.2, "suggest_outfit": 1183.4, "create_fit_card": 1306.1}, "error": null, "duration_ms": 3438.4, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1077, "output_tokens": 332, "total_tokens": 1409}
{"ts": "2026-11-16T05:12:23.202+00:00", "request_id": "3d976301", "status": 400, "outcome": "rejected", "query": "   ", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:12:23.211+00:00", "request_id": "e329ff06", "status": 400, "outcome": "rejected", "query": "query=sneakers", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:12:23.220+00:00", "request_id": "4b78486c", "status": 200, "outcome": "agent_error", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 820.5}, "error": "The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Injected for testing: the model API is unreachable. Best match meanwhile: Platform Sneakers — White Chunky Sole ($48.0, poshmark).", "duration_ms": 821.4, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:12:24.050+00:00", "request_id": "fff3be19", "status": 200, "outcome": "fit_card", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": "Channel total late-90s streetwear energy with these retro-vibe kicks paired with baggy dark denim and a cropped zip hoodie. You can snag the Platform Sneakers — White Chunky Sole on poshmark right now for just 48.0 to complete your effortless Y2K rotation.", "timings_ms": {"parse": 0.0, "search_listings": 719.3, "suggest_outfit": 3292.3, "create_fit_card": 34154.4}, "error": null, "duration_ms": 38171.5, "model_calls": 3, "cache_hits": 0, "prompt_tokens": 1065, "output_tokens": 324, "total_tokens": 1389}
```
