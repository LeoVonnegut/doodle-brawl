# Game Playbook — lessons from Doodle Brawl

Copy this file into every new game repo as `AGENTS.md` (read by both Claude Code and Codex), make `CLAUDE.md` just the line `@AGENTS.md`, then add a section about the new game. Keep AGENTS.md under 24 KB (Codex reads only 32 KB); put long history in `docs/HISTORY.md`.

## How we work
- I'm not a programmer. Do the technical work, explain simply, keep it short.
- Save usage: plan first, small focused steps, no big vague rewrites. Ask before big changes.
- GitHub is the source of truth. Clone the repo directly; never search my whole computer.
- Keep this file updated as decisions are made. Commit and push after each finished step.
- Before claiming something works, prove it (run it in the browser, measure it). Don't guess.
- On hard problems, pick the smart method first (use what's already installed, use your own eyes on images) instead of brute-forcing or installing things.
- If I say something was sent, list exactly what arrived by name before arguing.

## Safety and backups (every game)
- Protect `main` on GitHub right after creating a repo (no force-push, no deletion): `gh api -X PUT repos/LeoVonnegut/<repo>/branches/main/protection` with allow_force_pushes=false, allow_deletions=false, enforce_admins=true.
- Keep a second copy on the Mac: `git clone --mirror` into `~/GameBackups/<repo>.git`, refresh after pushes with `git -C ~/GameBackups/<repo>.git remote update -p`.
- Never give the `gh` login the `delete_repo` scope. `~/.claude/settings.json` blocks destructive commands (rm -rf, force push, reset --hard, git clean, gh repo delete).
- Tag each playable version (v0.1, v0.2, …) as a restore point. Commit + push after every finished step.

## Setup that already works on my Mac
- `gh` (GitHub CLI) is installed and logged in as LeoVonnegut, so push with normal `git push`.
- If a push fails with "HTTP 400", retry with `git -c http.postBuffer=524288000 push`.
- Host on GitHub Pages from `main`. After each deploy, everyone does a hard refresh (Cmd+Shift+R).

## Tech defaults (browser first)
- One `index.html` plus an `assets/` folder (`img/`, `audio/`), hosted on GitHub Pages.
- Stay in the browser until it truly blocks us. Godot/Steam later; Electron + Steamworks is the cheap Steam route. Consoles are the only hard wall.
- Multiplayer with PeerJS (free, no accounts): a "Just play" button plus private room codes (recommend codes for friends, so strangers don't join). Each player sends their own state ~30x/sec; the shooter decides hits. It worked Tbilisi ↔ Dubai at 60-150ms.
- Show a version number and warn when players' versions differ. Bump it whenever gameplay changes.
- All tuning numbers (gravity, jump, weapon stats) in one table. Keep game logic separate from drawing.
- Every drawn asset has a code fallback, so a missing file never breaks the game.
- Each player needs their own device. Decide early whether we need phone/touch controls or local split-screen.
- Anything random that other players see or hear (like which taunt plays) must be sent over the network, so everyone gets the same one.

## Drawing assets (my hand-drawn art)
- Plan the full numbered list first: every character part, every weapon, every projectile, every effect frame, the UI words, and a font sheet **A–Z, 0–9 and punctuation**. Make sure every weapon has both a drawing and a sound, so none gets missed.
- Black marker on plain white paper, weapons facing right, draw black only (the game adds player colours). Separate body parts so they can be animated. Draw animation frames left to right, in order.
- Photograph with **iPhone Notes → Scan Documents**, which removes shadows. Otherwise shoot straight down in even light with no hand shadow.
- How Claude extracts the art: flatten the lighting (divide by a blurred copy of the page), look at each page and mark every item, crop each one, then check them all on one labelled overview sheet before using them. Tools: `assets/crops.py`, `font.py`, `font_build.py` in the doodle-brawl repo.
- The handwriting font works as a bitmap font inside the game canvas. For menus and buttons, turn the sheet into a real font file with Calligraphr.

## Sound assets (my voice)
- One Voice Memo per section, named by the section (`weapons`, `weapons 2` for a second take, and so on). Sounds go in the agreed list order inside each memo. Leave gaps between sounds; they don't need to be perfect.
- To send many files from my phone: in the Files app, select them all → ⋯ → **Compress**, then send the one zip. (Only about 5 separate files come through per message.)
- How Claude processes them: map each file by its **name → section**, then by **list order** within the file. Drop the tap noises at the start and end of recordings, even out the volume, and trim inside the audio filter (not with output seeking, which made silent clips once). **Check that every clip actually contains sound** before shipping.
- Play sounds through Web Audio, picking a random take each time. Rapid-fire sounds (minigun, burst rifle) hold instead of stacking up.

## Vision principles (carry over)
- Human-made everything: my drawings, my handwriting, my voice. Friends can add their own screams and taunts.
- Aim for clip-worthy chaos: 10-second moments anyone gets instantly.

## Working with two AI tools (Claude Code + Codex)
- Claude Code is the dev lead; Codex (bundled in the ChatGPT Mac app, logged in with ChatGPT) does most of the building, so both plans' usage gets used.
- Copy `tools/codex.sh` from farm-fighter: `tools/codex.sh <easy|normal|hard|max> <job-file> [read]` runs Codex on a job in the background (easy = gpt-6-luna, normal/hard/max = gpt-6-astra medium/high/xhigh). Its report lands in `codex-runs/` (git-ignored).
- Codex works in the repo with no internet: it can edit and commit, the lead pushes and refreshes the backup mirror.
- One tool edits the same files at a time. Small commits. Never put keys or tokens in files.
- Codex's personal rules live in `~/.codex/AGENTS.md` (already set up on this Mac).
