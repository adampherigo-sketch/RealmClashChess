# Realm Clash Chess

Chess where every capture is an animated fight, in the spirit of classic battle-animation chess games.

- Full chess rules (castling, en passant, promotion, check, checkmate, stalemate)
- Four original themed realms, each with its own cast of animated characters drawn in code
- Black pawns use the supplied robot pup kit (`art/pup-black-pawn/`): idle, selected, moving, pounce, captured and promotion states
- Same-device play, plus two-device play by game code when hosted as a Claude artifact

`index.html` is the game; `kits.js` holds the supplied character kits (white pawn, knight, rook, queen, king)
and is generated from `art/` by `python3 tools/build_kits.py`. It is written as page content for a Claude artifact
(no `<html>`/`<body>` wrapper); browsers will still open it directly for same-device play.
