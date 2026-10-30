# H4H practice run — lessons (2026-10-30, 12:00–12:30 ACDT)

Practice slice: "Reservoir Watch" (W1 SA Water reservoir volumes → Streamlit chart + one Gemma call per question).
Throwaway — tonight's project must be built at the event.

## Gemma / Gemini API
- `gemma-4-26b-a4b-it` with `thinking_level="minimal"`: ~1–2.5 s, 6/6 calls OK. **Use this one.**
- `gemma-4-31b-it`: 9–23 s and one 500 in three calls. The first two smoke-test calls (around noon) got a 500 then a 503 "high demand". **Expect API flakiness at 7 pm, when every team is demoing on the same free tier.**
- Fallback built: `gemma.py` tries the API, then local Ollama `gemma4:e4b` on the 4090. The UI caption shows which backend answered. Keep that honest. Judges check "uses Gemma through the Gemini API", so the API should be the main path and Ollama only the safety net.
- I tested the fallback by forcing the API to fail with a bogus model name. It works, but: the **first call took 50 s** because the 6.6 GB model has to load, and later calls took about 6 s. The first answer also **got a fact wrong** ("85% is the same as August 2023"), where the 26B API model made no such errors. Before the demo, warm the model up with one call (or run `ollama run gemma4:e4b ""`). Treat local answers as a degraded mode.
- **Gemma refuses when the facts don't cover the question, and that's good.** "Is this unusual for this time of year?" got "the facts don't say" until I added same-month history from earlier years. Then it answered properly ("85%, higher than previous Augusts at 27–82%"). Lesson: work out ahead of time which facts each question needs, then pass them in. Gemma explains the numbers; pandas does the maths.

## Data
- **The data loader was the time sink, not the app.** W1 has 95 monthly CSVs with at least 3 header schemes (duplicate "Reservoir Name" columns, `Volume_today__ML_`, BOM-prefixed headers), plus junk rows ("Adelaide's consumption today is…"). Fix: pick columns by keyword, `encoding="utf-8-sig"`, `format="mixed"` dates, and filter to the real entities.
- Expect the same mess in the other themes' XLSX files (multi-row headers, notes rows). Budget 30–45 min for the data, and have Claude/CoCo write the loader while you write the pitch.
- Credit lines are in `data/README.md` → "Credit the source". Paste them into the app footer and README from the start.

## Environment (this container)
- Python env: `uv venv` + `google-genai python-dotenv streamlit pandas plotly openpyxl`. Took under 1 min.
- Key loading: `load_dotenv("/workspace/.secrets/.env.gemini")`, then project `.env`. **Don't copy the key into the project folder.**
- Cortex CLI is installed (`~/.local/bin/cortex`, v1.2.24) but not yet connected. Browser OAuth won't work in the container, so use a PAT.
- Ollama: installing it needed `zstd` first. The server was started by hand (`ollama serve`). It won't survive a container restart.
- Streamlit 1.5x: `use_container_width` is deprecated, so use `width="stretch"`.
- Headless test that actually clicks the button and makes a live Gemma call: `streamlit.testing.v1.AppTest`. It took 10 s, and it's how I check the app works without a browser.

## Git / submission (biggest open risk)
- No git identity in the container. Set it per repo: `git config user.name/email`.
- `gh` is not logged in. `GH_TOKEN_TOBYLIGHTHEART` exists, but a fine-grained PAT probably doesn't cover a **brand-new** repo.
  → **Tonight:** Toby creates the public repo in the GitHub web UI with the MIT licence ticked, in the first 15 minutes. Then we either add it to the token's scope or push another way. **Decide this before 3:45.**
- The repo must be public, MIT, and the README must name the model (Gemma 4 via the Gemini API + Apache 2.0 link) and the data credits. The challenge checks are done before demos.

## Time budget for tonight (3:45 build → 6:50 submit = 3 h 05)
| Block | Min |
|---|---|
| Problem pick + repo + README skeleton | 15 |
| Data loader + facts function | 45 |
| App + Gemma call + chart | 45 |
| Polish, honest fallback, README, credits | 30 |
| 60-second backup screen recording + demo rehearsal | 20 |
| Buffer | 30 |

## Snowflake (Track 3)
- (pending: trial signup, `AI_COMPLETE` check, PAT → cortex connection, Marketplace listing)
