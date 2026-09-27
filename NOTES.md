# Doodle Brawl notes

## How to work with me
- Not a programmer. Do the technical work, explain simply, keep it short.
- Care a lot about saving usage/tokens: plan first, small focused steps, no big vague rewrites.
- Ask before big changes. Don't touch anything outside this project folder.
- Play with friends in other countries (me in Tbilisi on a Mac, a friend in Dubai on Windows).
- Hate moving files around. GitHub is the source of truth.
- Start a new chat per feature/batch; batch fixes after play sessions.

## Current state (v1.1)
- Live at https://leovonnegut.github.io/doodle-brawl/ (GitHub Pages from main, file index.html).
- Single HTML file. Stick figures, notebook paper, googly eyes all drawn in code; sounds synthesized in code.
- Multiplayer via PeerJS: "Just play" (no code, first to click hosts, host relays) or private 5-letter code, with automatic reconnect if host leaves. Each player sends own state ~30x/sec; shooter decides hits, victim applies damage. Ping between Tbilisi/Dubai ~60-150ms, worked fine.
- Rounds (first to 5 bonks), leader crown, 1.5s spawn protection, kill feed, T taunt, random hats, squash and stretch, screen wraparound, moving platform, controller support, unique player colors, version check/mismatch warning.
- Guns now: Pea Shooter, Shotty, Brrrt-o-matic (minigun), Boomstick (rocket), Banana Bomb, Honk Cannon. Built for 4 players (6 max).

## History
1. First version used claude.ai's built-in multiplayer — failed for friend (needs a Claude Team account).
2. Switched to PeerJS (free, no accounts) — worked between Tbilisi and Dubai.
3. Added "Just play" + private room codes + auto-reconnect.
4. Big 4-player upgrade: rounds, crown, spawn protection, kill feed, taunts, hats, squash/stretch, Banana Bomb, Honk Cannon, moving platform, wraparound, controller support, colors.
5. Added version check (v1.1).
6. Hosted on GitHub Pages (LeoVonnegut/doodle-brawl, index.html).

## Vision
- Stick Fight / Duck Game style party brawler on notebook paper, drawn entirely by me.
- Maximum human-made assets: my drawings (traced from photos), my handwriting as the font, my voice for all sounds. Friends may record their own screams/taunts.
- Goal: clip-worthy chaos moments (10-second, instantly-get-it clips) to record with friends and post online.
- Signature twist ideas (the notebook fights back) — pick one to prototype: pencil draws platforms mid-match, eraser wipes floors, coffee spill, tearing pages, page flip to change maps.
- Later: killcam replay and a "save last 15 seconds" clip button.

## Long-term platform decisions
- Stay in HTML/browser for a long time; the only hard wall is consoles. Godot/Steam later, only when browser truly blocks us.
- Feel can transfer to Godot if: tuning numbers live in one place, movement code is custom (or same physics engine e.g. Rapier used in both), test runs recorded as numbers.
- Cheaper Steam path: wrap the HTML game in Electron with Steamworks.
- Browser physics (Matter.js/Rapier) is feasible; online physics sync is hard everywhere, not just browser.
- Models: Sonnet for most work, Opus for hard problems, Haiku for tiny chores.
- Real game-dev references (Sakurai's YouTube, Vlambeer's "Art of Screenshake", Duck Game, Stick Fight) are study references only, never role-played.

## Next version (build ONLY when I say go)
- Clean up fonts/text; fix scoreboard overlap ("first to 5" line collides with names).
- Remove "mind the gaps" background text.
- Fix falling at screen edges: floors must continue seamlessly through the wraparound.
- New gun lineup:
  - Pea Shooter (starting gun)
  - Rocket launcher (keep as is, same fire rate)
  - Shotgun
  - Minigun
  - Assault rifle (NEW) — open question: fast bursts, or randomly fires on its own sometimes?
  - Sniper rifle (NEW) — shots pass through platforms
  - Banana gun (keep, but must look nothing like the rocket launcher)
  - Honk Cannon — not mentioned in new lineup; decide whether to keep it.
- Replace all code-drawn art and synthesized sounds with hand-drawn and recorded assets, animated where needed.

## Drawings needed (black marker, plain white paper, numbered, 5-10 per page, photographed from straight above, good light, no shadows)
Characters (separate parts for animation, black only, game adds player color):
1 head, 2 face normal, 3 face hurt, 4 face dead (x x), 5 face taunting, 6 arm, 7 leg, 8 torso, 9 party hat, 10 propeller hat, 11 top hat, 12 beanie, 13 crown (extra hats welcome).
Weapons (facing right): 14 pea shooter, 15 shotgun, 16 minigun, 17 assault rifle, 18 sniper, 19 rocket launcher, 20 banana gun.
Projectiles: 21 pea, 22 pellet, 23 bullet, 24 rocket, 25 banana.
World: 26 thick floor block, 27 thin platform, 28 moving platform (ruler or pencil), 29 "?" crate.
Effects (frames left to right): 30 explosion x4, 31 muzzle flash x2, 32 hit splat x3, 33 dust puff x3, 34 respawn poof x3, 35 confetti x5-6 shapes.
Text/UI: 36 "BONK!", 37 "KABOOM", 38 "WINS!", 39 logo, 40 crosshair, 41 skull icon, 42 kill icon.
Font: A-Z, 0-9, ! ? . , ' - : ( ) in capitals, one per grid box.

## Audio needed (iPhone Voice Memos, one memo per section, list order, ~2s silence between sounds, 2-3 takes each, don't say names aloud)
Weapons: pea shooter, shotgun, minigun burst, assault rifle, sniper, rocket launch, banana throw.
Explosions: rocket boom, banana boom.
Hits/deaths: 3 bonk/oof hits, 5 death screams, 1 long falling "aaaa".
Moving: jump, double jump, landing thud.
Items: crate pickup, out of ammo.
Taunts: 6-10 short lines.
Rounds: "Fight!", winner fanfare, player joined.
Optional: 15-20s hummed/beatboxed music loop.

## How to send assets
- Drawings: attach photos in chat, e.g. "drawings 1-15."
- Audio: Voice Memos → ⋯ → Save to Files → attach in chat, e.g. "audio: weapons."
- Claude traces exact lines into game graphics, slices audio by silences, reports anything to redo.

## Principles (for a future Godot/Steam port)
- All tuning numbers (gravity, jump, knockback, weapon stats) in one place.
- Game logic separate from drawing.
- Decide netcode style early: simple host-based vs rollback.
- Move to Godot only when the browser truly blocks us; only hard wall is consoles.
