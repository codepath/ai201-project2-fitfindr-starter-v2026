# Capstone run — before

2026-11-16T00:02 · model `gemini-3.5-flash-lite` · temperature 0.9 · cache OFF · 3 trials · produced by `capstone_eval.py` through `serve.py::ask`

## Summary (counts per trial)

| Measurement | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|
| Numeric size parsed to the right value (S1–S5) | 5/5 | 5/5 | 5/5 |
| Size text removed from the description (S1–S5) | 5/5 | 5/5 | 5/5 |
| Every returned listing matches the numeric size (S1–S4, needs ≥1 result) | 4/4 | 4/4 | 4/4 |
| Numeric-size query ends in a fit card (S1–S4) | 4/4 | 4/4 | 3/4 |
| Unstocked size stops early AND the message names the size (S5) | 1/1 | 1/1 | 1/1 |
| Regression queries still parse and finish with a fit card (R1–R2) | 2/2 | 2/2 | 2/2 |
| Bad input gets a 400, not a 500 (F1–F2) | 2/2 | 2/2 | 2/2 |
| Model down: 200 + error naming the found listing, no crash (F3) | 1/1 | 1/1 | 1/1 |
| Every request left a log record (all) | 10/10 | 10/10 | 10/10 |
| Runs under 10 s end to end (S1–S4, R1–R2) | 6/6 | 5/6 | 5/6 |

## Trial 1

| ID | Query | Status | Parsed size | Size right | Size text left | Results | All match size | Fit card | Error names size | ms | Tokens | Logged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 6606.6 | 1621 | yes |
| S2 | `chelsea boots size 8.5` | 200 | US 8.5 | yes | **NO** | 1 | yes | yes | – | 3076.7 | 1235 | yes |
| S3 | `high-waisted denim shorts W27` | 200 | W27 | yes | **NO** | 1 | yes | yes | – | 3574.1 | 1494 | yes |
| S4 | `straight leg black jeans waist 28` | 200 | W28 | yes | **NO** | 2 | yes | yes | – | 3259.0 | 1306 | yes |
| S5 | `canvas sneakers size 12` | 200 | US 12 | yes | **NO** | 0 | – | **NO** | yes | 1408.4 | 0 | yes |
| R1 | `vintage graphic tee under $30, size M` | 200 | M | yes | **NO** | 10 | yes | yes | – | 2963.1 | 1394 | yes |
| R2 | `vintage jacket under $25` | 200 | – | yes | – | 10 | – | yes | – | 2652.8 | 1262 | yes |
| F1 | `{"query": "   "}` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F2 | `query=sneakers` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F3 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | **NO** | – | 865.8 | 0 | yes |

## Trial 2

| ID | Query | Status | Parsed size | Size right | Size text left | Results | All match size | Fit card | Error names size | ms | Tokens | Logged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 72686.9 | 1633 | yes |
| S2 | `chelsea boots size 8.5` | 200 | US 8.5 | yes | **NO** | 1 | yes | yes | – | 3647.5 | 1357 | yes |
| S3 | `high-waisted denim shorts W27` | 200 | W27 | yes | **NO** | 1 | yes | yes | – | 2655.9 | 1298 | yes |
| S4 | `straight leg black jeans waist 28` | 200 | W28 | yes | **NO** | 2 | yes | yes | – | 3445.9 | 1246 | yes |
| S5 | `canvas sneakers size 12` | 200 | US 12 | yes | **NO** | 0 | – | **NO** | yes | 867.2 | 0 | yes |
| R1 | `vintage graphic tee under $30, size M` | 200 | M | yes | **NO** | 10 | yes | yes | – | 2638.4 | 1252 | yes |
| R2 | `vintage jacket under $25` | 200 | – | yes | – | 10 | – | yes | – | 3130.5 | 1404 | yes |
| F1 | `{"query": "   "}` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F2 | `query=sneakers` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F3 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | **NO** | – | 1038.9 | 0 | yes |

## Trial 3

| ID | Query | Status | Parsed size | Size right | Size text left | Results | All match size | Fit card | Error names size | ms | Tokens | Logged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | yes | – | 2990.4 | 1268 | yes |
| S2 | `chelsea boots size 8.5` | 200 | US 8.5 | yes | **NO** | 1 | yes | yes | – | 3332.1 | 1277 | yes |
| S3 | `high-waisted denim shorts W27` | 200 | W27 | yes | **NO** | 1 | yes | **NO** | – | 36921.5 | 0 | yes |
| S4 | `straight leg black jeans waist 28` | 200 | W28 | yes | **NO** | 2 | yes | yes | – | 3010.3 | 1269 | yes |
| S5 | `canvas sneakers size 12` | 200 | US 12 | yes | **NO** | 0 | – | **NO** | yes | 964.0 | 0 | yes |
| R1 | `vintage graphic tee under $30, size M` | 200 | M | yes | **NO** | 10 | yes | yes | – | 2955.6 | 1534 | yes |
| R2 | `vintage jacket under $25` | 200 | – | yes | – | 10 | – | yes | – | 2495.3 | 1230 | yes |
| F1 | `{"query": "   "}` | 400 | – | – | – | 0 | – | **NO** | – | 0.1 | 0 | yes |
| F2 | `query=sneakers` | 400 | – | – | – | 0 | – | **NO** | – | 0.2 | 0 | yes |
| F3 | `platform sneakers size 8` | 200 | US 8 | yes | **NO** | 1 | yes | **NO** | – | 1033.1 | 0 | yes |

## Fit cards and errors (trial 1)

**S1 — shoe size, whole**

```
Level up your late 90s streetwear casual look with these Platform Sneakers — White Chunky Sole, currently listed on poshmark for $48. Paired with dark baggy denim and a fitted ribbed tank, they anchor the voluminous silhouette with effortless retro energy.
```

**S2 — shoe size, half**

```
Pairing a crisp white tank, wide-leg khaki trousers, and a black denim jacket creates the ultimate casual minimalist earth-tone vibe for everyday wear. These Suede Chelsea Boots — Tan pull the whole look together seamlessly and effortlessly. Grab them on Poshmark now for just $44.00!
```

**S3 — waist, W-form**

```
Channel an effortless grunge-meets-summer vibe by pairing these High-Waisted Denim Shorts — Cutoff with a vintage black jacket and chunky combat boots. This versatile staple is currently listed on poshmark for just $24.0, making it the ultimate piece for building easy, high-contrast warm-weather looks.
```

**S4 — waist, word form**

```
Score these Straight Leg Black Jeans — Faded for just $30.0 on thredUp! They are perfect for building a sleek, monochrome edge look with a black cropped zip hoodie and combat boots, or for keeping things casual and cozy with an oversized grey crewneck and white sneakers.
```

**S5 — numeric size nobody stocks**

```
No listings matched your search. Nothing is listed in size US 12, so try a different size or remove the size. Try changing the description, removing the size filter, or increasing the maximum price.
```

**R1 — letter size + price (unit 3 query)**

```
Embrace early 2000s nostalgia with this Y2K Baby Tee — Butterfly Print, listed on depop for just $18.0! It's perfect for styling into classic Y2K streetwear with baggy jeans and chunky sneakers, or mixing with black combat boots for an edgy, high-low look. Grab this sweet crop top to elevate your casual wardrobe today!
```

**R2 — no size at all**

```
Channel your inner 2000s icon with this Y2K Streetwear Casual look, featuring the **Y2K Baby Tee — Butterfly Print** paired with baggy dark-wash jeans, a cropped zip hoodie, and chunky sneakers. Grab this cute top for just $18.0 over on depop to complete your nostalgic wardrobe rotation.
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

## Log records from this run (`logs/runs.jsonl`, last 12)

```json
{"ts": "2026-11-16T05:01:18.259+00:00", "request_id": "19d3f6d1", "status": 400, "outcome": "rejected", "query": "query=sneakers", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:01:18.273+00:00", "request_id": "d0c791ca", "status": 200, "outcome": "agent_error", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 1037.8}, "error": "The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Injected for testing: the model API is unreachable. Best match meanwhile: Platform Sneakers — White Chunky Sole ($48.0, poshmark).", "duration_ms": 1038.9, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:01:19.320+00:00", "request_id": "c84f8db7", "status": 200, "outcome": "fit_card", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": "Channel major late-90s energy with these Platform Sneakers — White Chunky Sole, listed on poshmark for $48. Pair them with baggy dark-wash jeans, a ribbed tank, and a vintage black denim jacket for the ultimate Y2K streetwear casual vibe.", "timings_ms": {"parse": 0.0, "search_listings": 816.7, "suggest_outfit": 1458.7, "create_fit_card": 710.7}, "error": null, "duration_ms": 2990.4, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1006, "output_tokens": 262, "total_tokens": 1268}
{"ts": "2026-11-16T05:01:22.322+00:00", "request_id": "2f8882aa", "status": 200, "outcome": "fit_card", "query": "chelsea boots size 8.5", "parsed": {"description": "chelsea boots", "size": "US 8.5", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8.5"], "selected": {"id": "lst_028", "title": "Suede Chelsea Boots — Tan", "size": "US 8.5", "price": 44.0}, "fit_card": "Scored these gorgeous Suede Chelsea Boots — Tan for just $44.00 on poshmark! They are the ultimate addition to a casual minimalist earth-tone outfit, pairing effortlessly with wide-leg trousers and a white ribbed tank. It's such a clean, polished, yet relaxed look for everyday wear.", "timings_ms": {"parse": 0.1, "search_listings": 907.3, "suggest_outfit": 1163.7, "create_fit_card": 1253.8}, "error": null, "duration_ms": 3332.1, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1005, "output_tokens": 272, "total_tokens": 1277}
{"ts": "2026-11-16T05:01:25.668+00:00", "request_id": "26fb8f24", "status": 200, "outcome": "agent_error", "query": "high-waisted denim shorts W27", "parsed": {"description": "high-waisted denim shorts", "size": "W27", "max_price": null}, "size_kind": "waist", "n_results": 1, "result_sizes": ["W27"], "selected": {"id": "lst_016", "title": "High-Waisted Denim Shorts — Cutoff", "size": "W27", "price": 24.0}, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 877.3}, "error": "The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} Best match meanwhile: High-Waisted Denim Shorts — Cutoff ($24.0, poshmark).", "duration_ms": 36921.5, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:02:02.634+00:00", "request_id": "a0ea22f3", "status": 200, "outcome": "fit_card", "query": "straight leg black jeans waist 28", "parsed": {"description": "straight leg black jeans", "size": "W28", "max_price": null}, "size_kind": "waist", "n_results": 2, "result_sizes": ["W28", "W28"], "selected": {"id": "lst_037", "title": "Straight Leg Black Jeans — Faded", "size": "W28", "price": 30.0}, "fit_card": "I scored these Straight Leg Black Jeans — Faded on thredUp for just $30.0! They are the ultimate anchor for a casual streetwear and monochrome look, especially when layered with a slouchy grey crewneck and fresh chunky sneakers.", "timings_ms": {"parse": 0.0, "search_listings": 902.6, "suggest_outfit": 1173.2, "create_fit_card": 929.6}, "error": null, "duration_ms": 3010.3, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1009, "output_tokens": 260, "total_tokens": 1269}
{"ts": "2026-11-16T05:02:05.656+00:00", "request_id": "536c80d9", "status": 200, "outcome": "empty_search", "query": "canvas sneakers size 12", "parsed": {"description": "canvas sneakers", "size": "US 12", "max_price": null}, "size_kind": "shoe", "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 962.0}, "error": "No listings matched your search. Nothing is listed in size US 12, so try a different size or remove the size. Try changing the description, removing the size filter, or increasing the maximum price.", "duration_ms": 964.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:02:06.630+00:00", "request_id": "a2252a8f", "status": 200, "outcome": "fit_card", "query": "vintage graphic tee under $30, size M", "parsed": {"description": "vintage graphic tee", "size": "M", "max_price": 30.0}, "size_kind": "letter", "n_results": 10, "result_sizes": ["S/M", "S/M", "M", "One Size (adjustable)", "M", "M", "M", "M", "One Size", "M"], "selected": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "size": "S/M", "price": 18.0}, "fit_card": "Serve up early 2000s street style by pairing the Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans and chunky white sneakers for the ultimate casual look. It is listed on depop right now for just $18.0, giving you an effortless way to nail that fitted-top-and-baggy-bottom proportion contrast.", "timings_ms": {"parse": 0.0, "search_listings": 818.4, "suggest_outfit": 1438.1, "create_fit_card": 693.0}, "error": null, "duration_ms": 2955.6, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 1130, "output_tokens": 404, "total_tokens": 1534}
{"ts": "2026-11-16T05:02:09.598+00:00", "request_id": "d5e2ebc9", "status": 200, "outcome": "fit_card", "query": "vintage jacket under $25", "parsed": {"description": "vintage jacket", "size": null, "max_price": 25.0}, "size_kind": null, "n_results": 10, "result_sizes": ["S/M", "XL (oversized)", "L", "XL (fits oversized)", "One Size (adjustable)", "W27", "M", "M", "XL", "M"], "selected": {"id": "lst_002", "title": "Y2K Baby Tee — Butterfly Print", "size": "S/M", "price": 18.0}, "fit_card": "Channel authentic early 2000s proportions with a fitted Y2K Streetwear Casual look that pairs baggy dark-wash jeans with chunky white sneakers and a black crossbody bag. Grab the Y2K Baby Tee — Butterfly Print on depop for just 18.0 to nail that effortlessly practical everyday vibe!", "timings_ms": {"parse": 0.0, "search_listings": 953.6, "suggest_outfit": 971.1, "create_fit_card": 568.2}, "error": null, "duration_ms": 2495.3, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 983, "output_tokens": 247, "total_tokens": 1230}
{"ts": "2026-11-16T05:02:12.136+00:00", "request_id": "9deabdf7", "status": 400, "outcome": "rejected", "query": "   ", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:02:12.150+00:00", "request_id": "a4745c84", "status": 400, "outcome": "rejected", "query": "query=sneakers", "parsed": null, "size_kind": null, "n_results": 0, "result_sizes": [], "selected": null, "fit_card": null, "timings_ms": {}, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_ms": 0.2, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-16T05:02:12.164+00:00", "request_id": "a4dd316f", "status": 200, "outcome": "agent_error", "query": "platform sneakers size 8", "parsed": {"description": "platform sneakers", "size": "US 8", "max_price": null}, "size_kind": "shoe", "n_results": 1, "result_sizes": ["US 8"], "selected": {"id": "lst_019", "title": "Platform Sneakers — White Chunky Sole", "size": "US 8", "price": 48.0}, "fit_card": null, "timings_ms": {"parse": 0.0, "search_listings": 1030.7}, "error": "The search worked, but the outfit model couldn't be reached, so no outfit or fit card was made. Injected for testing: the model API is unreachable. Best match meanwhile: Platform Sneakers — White Chunky Sole ($48.0, poshmark).", "duration_ms": 1033.1, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
