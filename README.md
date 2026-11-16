# Realm Clash Chess

Chess where every capture is an animated fight, in the spirit of classic battle-animation chess games.

- Full chess rules (castling, en passant, promotion, check, checkmate, stalemate)
- Four original themed realms, each with its own cast of animated characters drawn in code
- Pawns are styled per realm, each with idle, selected, moving, attack, captured and promotion drawings plus its own move/capture markers:
  - Temporal Wardens: the supplied P-1 robot pawn (white) and robot pup (black, `art/pup-black-pawn/`)
  - Frontier Armada: Concord ensign with a blaster vs Kragh trooper with a disruptor rifle
  - Dungeon Delve: militia spearman with a shield vs horned skeleton with a rusty sword
  - Arcane Duel: Dawn apprentice with a star wand vs floating Dusk shade with a crystal wand
- Same-device play, plus two-device play by game code when hosted as a Claude artifact

`index.html` is the game; `kits.js` holds the supplied character kits (white pawn, knight, rook, queen, king)
and is generated from `art/` by `python3 tools/build_kits.py`. The realm pawns in `art/<realm>-<side>-pawn/` are drawn by
`python3 tools/make_realm_pawns.py` (re-run it, then `build_kits.py`, after changing a character). It is written as page content for a Claude artifact
(no `<html>`/`<body>` wrapper); browsers will still open it directly for same-device play.

## Testing

`node tools/test_game.js` runs a headless sweep (needs Playwright and Chromium): move-generation counts against known
reference positions, random full games with and without battles in every realm, castling, en passant, promotion,
checkmate, repetition, undo, drag-to-move, the character sheets, and two-device play against a simulated shared store.
