# Doodle Brawl notes

## Current state (v1.1)
- Live at https://leovonnegut.github.io/doodle-brawl/ (GitHub Pages from main, file index.html).
- Single HTML file. Stick figures, notebook paper, googly eyes all drawn in code; sounds synthesized in code.
- Multiplayer via PeerJS: "Just play" (no code, first to click hosts, host relays) or private 5-letter code. Each player sends own state ~30x/sec; shooter decides hits, victim applies damage.
- Rounds (first to 5 bonks), leader crown, 1.5s spawn protection, kill feed, T taunt, random hats, screen wraparound, moving platform, controller support, version check.
- Guns now: Pea Shooter, Shotty, Brrrt-o-matic (minigun), Boomstick (rocket), Banana Bomb, Honk Cannon. Built for 4 players (6 max).

## Vision
- Stick Fight / Duck Game style party brawler on notebook paper, drawn entirely by me.
- Maximum human-made assets: my drawings (traced from photos), my handwriting as the font, my voice for all sounds. Friends may record their own screams/taunts.
- Goal: clip-worthy chaos moments to record with friends and post online.
- Twist ideas (notebook fights back): pencil draws platforms mid-match, eraser wipes floors, coffee spill, tearing pages, page flip to change maps.
- Later: killcam replay and a "save last 15 seconds" clip button.

## Next version (build ONLY when I say go)
- Clean up fonts/text; fix scoreboard overlap ("first to 5" line collides with names).
- Remove "mind the gaps" background text.
- Fix falling at screen edges: floors must continue seamlessly through the wraparound.
- Guns: Pea Shooter (start), Rocket launcher (keep as is), Shotgun, Minigun, NEW Assault rifle (open question: fast bursts or randomly fires on its own?), NEW Sniper (shots pass through platforms), Banana gun (keep but make it look nothing like the rocket). Honk Cannon: undecided.
- Replace all code art and synth sounds with my hand-drawn and recorded assets, animated where needed.

## Assets I'll provide
Drawings (black marker, plain white paper, numbered, photographed from above, 5-10 per page):
1 head, 2-5 faces (normal, hurt, dead x x, taunting), 6 arm, 7 leg, 8 torso, 9-13 hats (party, propeller, top hat, beanie, crown); 14-20 weapons facing right (pea shooter, shotgun, minigun, assault rifle, sniper, rocket launcher, banana gun); 21-25 projectiles (pea, pellet, bullet, rocket, banana); 26 thick floor, 27 thin platform, 28 moving platform, 29 "?" crate; 30 explosion x4 frames, 31 muzzle flash x2, 32 hit splat x3, 33 dust puff x3, 34 respawn poof x3, 35 confetti shapes; 36 "BONK!", 37 "KABOOM", 38 "WINS!", 39 logo, 40 crosshair, 41 skull icon, 42 kill icon; font sheet A-Z 0-9 ! ? . , ' - : ( ).
Audio (iPhone Voice Memos, one memo per section, list order, ~2s silence between sounds, 2-3 takes each, names not spoken):
weapons (pea, shotgun, minigun burst, assault rifle, sniper, rocket launch, banana throw); explosions (rocket, banana); hits/deaths (3 hits, 5 death screams, 1 long fall "aaaa"); moving (jump, double jump, land); items (pickup, out of ammo); 6-10 taunts; rounds ("Fight!", winner fanfare, player joined); optional 15-20s hummed music loop.
Workflow: I'll drop photos and memos into an inbox folder; you trace drawings into game graphics, slice audio by silences, and report anything to redo.

## Principles
- All tuning numbers in one place; game logic separate from drawing.
- Decide netcode style early (host-based vs rollback).
- Stay in the browser until it truly blocks us; Godot/Steam later.
- Keep requests small to save usage; plan before building.
