#!/usr/bin/env python3
"""Draw the realm pawn kits (Armada, Dungeon, Arcane; white and black) into art/.

Each character is assembled from parts (legs, torso, head, arms, weapon) and written
once per state: idle, selected, moving, attack, captured, promotion, icon, plus the
move / capture hint markers. Same canvas as the supplied kits (viewBox 135 20 410 430,
feet on y~432, facing right). Run from the repo root, then run tools/build_kits.py:
    python3 tools/make_realm_pawns.py && python3 tools/build_kits.py
"""
import os

INK = '#15131a'
OL = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"'
OLT = f'stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"'
SH_L, SH_F = (296, 236), (386, 236)          # shoulders (back, front)
HAND_B, HAND_F = (272, 302), (422, 292)      # hands
LEG_L, LEG_R = 314, 366                      # leg centres


def limb(x1, y1, x2, y2, col, w=22):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="{w+10}" stroke-linecap="round"/>'
            f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


def hand(p, col, r=13):
    return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{col}" {OL}/>'


def star(cx, cy, r, fill, cls='', extra=''):
    pts = []
    import math
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        pts.append(f'{cx + rr * math.cos(a):.1f} {cy + rr * math.sin(a):.1f}')
    c = f' class="{cls}"' if cls else ''
    return f'<path{c} d="M{" L".join(pts)}Z" fill="{fill}" {extra}/>'


def boot_leg(cx, pants, boot):
    return (f'<rect x="{cx-14}" y="334" width="28" height="74" rx="12" fill="{pants}" {OL}/>'
            f'<path d="M{cx-18} 398 L{cx+12} 398 Q{cx+30} 404 {cx+30} 420 L{cx+30} 430 L{cx-18} 430 Z" fill="{boot}" {OL}/>')


def bone_leg(cx, bone):
    return (limb(cx, 338, cx, 414, bone, 12) +
            f'<ellipse cx="{cx+8}" cy="424" rx="22" ry="9" fill="{bone}" {OL}/>')


def eyes_human(st, x1=334, x2=376, y=162, col='#1b1626'):
    if st == 'captured':
        return ''.join(f'<path d="M{x-8} {y-8} L{x+8} {y+8} M{x+8} {y-8} L{x-8} {y+8}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>' for x in (x1, x2))
    return ''.join(f'<g class="ey"><ellipse cx="{x}" cy="{y}" rx="8" ry="11" fill="{col}"/><circle cx="{x+3}" cy="{y-4}" r="3" fill="#fff"/></g>' for x in (x1, x2))


def mouth(st, x=362, y=192, col='#5a2a1a'):
    if st == 'captured':
        return f'<ellipse cx="{x}" cy="{y+2}" rx="7" ry="8" fill="{col}"/>'
    if st in ('attack', 'selected'):
        return f'<path d="M{x-12} {y-2} L{x+12} {y-4}" stroke="{col}" stroke-width="4.5" stroke-linecap="round"/>'
    return f'<path d="M{x-10} {y} Q{x} {y+7} {x+10} {y-1}" stroke="{col}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'


def blush():
    return ('<ellipse cx="318" cy="186" rx="9" ry="5" fill="#ff7a7a" opacity=".35"/>'
            '<ellipse cx="394" cy="184" rx="8" ry="5" fill="#ff7a7a" opacity=".35"/>')


# ───────────────────────── characters ─────────────────────────

def concord(st):
    skin, blue, white, navy, glow = '#e8b98f', '#2c6fd6', '#eef3fb', '#1b2c4a', '#4fb3ff'
    legs = (f'<g class="lL">{boot_leg(LEG_L, navy, white)}</g>', f'<g class="lR">{boot_leg(LEG_R, navy, white)}</g>')
    armb = limb(*SH_L, *HAND_B, blue) + hand(HAND_B, white)
    torso = (f'<path d="M288 222 Q280 290 290 346 L390 346 Q400 290 392 222 Q340 206 288 222Z" fill="{blue}" {OL}/>'
             f'<path d="M296 226 Q290 290 298 340 L310 340 Q304 290 310 222Z" fill="#245cb2"/>'
             f'<path d="M312 218 L340 246 L368 218" fill="none" stroke="{white}" stroke-width="9" stroke-linejoin="round"/>'
             f'<path d="M368 258 L381 284 L355 284Z" fill="#ff9d3c" {OLT}/>'
             f'<rect x="288" y="320" width="104" height="18" rx="5" fill="{navy}" {OLT}/>'
             f'<rect class="wg2" x="330" y="323" width="20" height="12" rx="3" fill="{glow}"/>'
             f'<ellipse cx="298" cy="230" rx="26" ry="15" fill="{white}" {OL}/>')
    head = (f'<circle cx="340" cy="152" r="64" fill="{skin}" {OL}/>' + blush() +
            eyes_human(st) + mouth(st) +
            f'<path d="M274 152 Q270 80 340 78 Q410 80 406 152 Q402 130 380 124 L300 124 Q278 130 274 152Z" fill="{white}" {OL}/>'
            f'<path d="M300 98 Q340 80 382 98" stroke="{blue}" stroke-width="13" fill="none" stroke-linecap="round"/>'
            f'<path d="M296 112 Q304 100 318 96" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/>'
            f'<circle cx="286" cy="164" r="16" fill="#c9d2e2" {OL}/><circle class="wg2" cx="286" cy="164" r="6" fill="{glow}"/>'
            f'<path d="M286 148 L262 112" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle class="wg2" cx="260" cy="108" r="6" fill="{glow}"/>')
    wpn = (f'<rect x="404" y="270" width="62" height="24" rx="8" fill="{white}" {OL}/>'
           f'<rect x="414" y="276" width="40" height="6" rx="3" fill="{blue}"/>'
           f'<rect x="462" y="275" width="22" height="14" rx="4" fill="#39435a" {OL}/>'
           f'<rect x="410" y="290" width="16" height="24" rx="5" fill="#39435a" {OL}/>')
    armf = limb(*SH_F, *HAND_F, blue) + f'<ellipse cx="384" cy="230" rx="26" ry="15" fill="{white}" {OL}/>'
    return dict(legs=legs, armb=armb, torso=torso, head=head, armf=armf, wpn=wpn, handf=hand(HAND_F, white),
                tip=(492, 282), glow=glow, glow2='#cfeeff', kind='shoot')


def kragh(st):
    skin, red, gold, metal, glow = '#6fbf6a', '#7a1f1f', '#d9a441', '#2c2f38', '#3dff6e'
    legs = (f'<g class="lL">{boot_leg(LEG_L, metal, red)}</g>', f'<g class="lR">{boot_leg(LEG_R, metal, red)}</g>')
    armb = limb(*SH_L, *HAND_B, metal) + hand(HAND_B, skin)
    spikes = lambda x: f'<path d="M{x-18} 224 L{x-12} 198 L{x-4} 220 L{x+4} 194 L{x+12} 220 L{x+18} 202 L{x+22} 226Z" fill="#4a4e58" {OLT}/>'
    torso = (f'<path d="M286 222 Q278 290 290 346 L390 346 Q402 290 394 222 Q340 204 286 222Z" fill="{red}" {OL}/>'
             f'<path d="M306 232 L340 300 L374 232" fill="none" stroke="{gold}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M298 230 Q292 290 300 340 L312 340 Q306 290 312 226Z" fill="#5e1616"/>'
             f'<rect x="286" y="320" width="108" height="20" rx="5" fill="{metal}" {OLT}/>'
             f'<path class="wg2" d="M340 322 L350 330 L340 338 L330 330Z" fill="{glow}"/>'
             + spikes(298) + f'<ellipse cx="298" cy="230" rx="28" ry="16" fill="{metal}" {OL}/>')
    if st == 'captured':
        eyes = ''.join(f'<path d="M{x-8} 152 L{x+8} 166 M{x+8} 152 L{x-8} 166" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>' for x in (334, 378))
    else:
        eyes = ''.join(f'<g class="ey"><ellipse cx="{x}" cy="159" rx="10" ry="8" fill="#d6ff6a" {OLT}/><rect x="{x-1.8}" y="152" width="3.6" height="14" rx="1.8" fill="{INK}"/></g>' for x in (334, 378))
    head = (f'<ellipse cx="340" cy="156" rx="68" ry="60" fill="{skin}" {OL}/>'
            f'<path d="M290 190 Q340 226 398 186 Q392 214 340 218 Q300 214 290 190Z" fill="#58a055"/>'
            + eyes +
            f'<path d="M308 140 Q342 152 398 134 L400 146 Q352 164 308 152Z" fill="#4f8f4c" {OLT}/>'
            f'<path d="M336 196 Q362 204 388 192" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M342 198 L346 182 L352 198Z" fill="#f4efe0" {OLT}/><path d="M378 195 L384 180 L388 194Z" fill="#f4efe0" {OLT}/>'
            f'<path d="M276 146 Q274 80 340 76 Q406 80 406 146 Q340 116 276 146Z" fill="{red}" {OL}/>'
            f'<path d="M300 90 Q332 30 394 80 Q352 66 300 90Z" fill="{gold}" {OL}/>'
            f'<path d="M282 132 Q340 108 402 132" stroke="{gold}" stroke-width="6" fill="none"/>')
    wpn = (f'<path d="M394 264 L478 264 Q490 266 492 276 L494 292 L394 298 Z" fill="{metal}" {OL}/>'
           f'<rect x="402" y="292" width="18" height="28" rx="5" fill="{red}" {OL}/>'
           + ''.join(f'<rect class="wg2" x="{x}" y="270" width="8" height="18" rx="3" fill="{glow}"/>' for x in (428, 444, 460)) +
           f'<path d="M492 272 L514 277 L514 289 L492 292Z" fill="{gold}" {OL}/>')
    armf = limb(*SH_F, *HAND_F, metal) + spikes(384) + f'<ellipse cx="384" cy="230" rx="28" ry="16" fill="{metal}" {OL}/>'
    return dict(legs=legs, armb=armb, torso=torso, head=head, armf=armf, wpn=wpn, handf=hand(HAND_F, skin),
                tip=(518, 283), glow=glow, glow2='#c8ffd5', kind='shoot')


def militia(st):
    skin, red, gold, steel, brown = '#eac39a', '#b33a2e', '#e0a93b', '#c3cad3', '#6a4320'
    legs = (f'<g class="lL">{boot_leg(LEG_L, brown, "#3a2508")}</g>', f'<g class="lR">{boot_leg(LEG_R, brown, "#3a2508")}</g>')
    armb = limb(*SH_L, *HAND_B, '#8d949e') + hand(HAND_B, skin)
    mail = ''.join(f'<path d="M{x} {y} q6 6 12 0" stroke="#6f7680" stroke-width="2.5" fill="none"/>' for y in (240, 262, 284, 306) for x in range(296, 384, 14))
    torso = (f'<path d="M288 222 Q280 290 290 346 L390 346 Q400 290 392 222 Q340 206 288 222Z" fill="#8d949e" {OL}/>' + mail +
             f'<path d="M314 218 L366 218 L374 352 L306 352Z" fill="{red}" {OL}/>'
             f'<path d="M340 246 L354 270 L340 294 L326 270Z" fill="{gold}" {OLT}/>'
             f'<rect x="288" y="318" width="104" height="16" rx="4" fill="#5a3818" {OLT}/>'
             f'<rect x="332" y="316" width="18" height="20" rx="3" fill="{gold}" {OLT}/>')
    shield = (f'<circle cx="262" cy="300" r="46" fill="#8b5a2b" {OL}/>'
              f'<path d="M232 270 L232 330 M262 254 L262 346 M292 270 L292 330" stroke="#6a4320" stroke-width="3"/>'
              f'<circle cx="262" cy="300" r="40" fill="none" stroke="{gold}" stroke-width="7"/>'
              f'<circle cx="262" cy="300" r="13" fill="{steel}" {OL}/><circle cx="258" cy="296" r="4" fill="#fff" opacity=".8"/>')
    head = (f'<circle cx="340" cy="156" r="62" fill="{skin}" {OL}/>' + blush() +
            f'<path d="M282 130 Q276 168 290 178 Q292 150 300 134Z" fill="{brown}"/>'
            + eyes_human(st, y=166) + mouth(st, y=196) +
            f'<path d="M322 146 L344 150 M366 150 L388 144" stroke="{brown}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M284 120 Q286 62 340 60 Q394 62 396 120Z" fill="{steel}" {OL}/>'
            f'<ellipse cx="340" cy="120" rx="90" ry="17" fill="#aab2bd" {OL}/>'
            f'<path d="M304 82 Q316 70 334 68" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85"/>'
            + ''.join(f'<circle cx="{x}" cy="120" r="3.5" fill="#6f7680"/>' for x in (276, 308, 340, 372, 404)))
    wpn = (f'<path d="M408 412 L444 100" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
           f'<path d="M408 412 L444 100" stroke="#8b5a2b" stroke-width="8" stroke-linecap="round"/>'
           f'<path d="M444 108 Q432 124 438 140 M446 110 Q456 126 448 142" stroke="{red}" stroke-width="6" fill="none" stroke-linecap="round"/>'
           f'<path d="M451 36 L462 86 L445 106 L432 82Z" fill="{steel}" {OL}/>'
           f'<path d="M449 50 L448 90" stroke="#fff" stroke-width="3" opacity=".8"/>')
    armf = limb(*SH_F, *HAND_F, '#8d949e')
    return dict(legs=legs, armb=armb, torso=torso, front_b=f'<g class="ab">{shield}</g>', head=head, armf=armf, wpn=wpn,
                handf=hand(HAND_F, skin), tip=(451, 40), glow='#ffd27a', glow2='#fff3c8', kind='thrust')


def skeleton(st):
    bone, purple, iron, glow = '#e9e4d0', '#3a2a3f', '#5b5560', '#7dff6a'
    legs = (f'<g class="lL">{bone_leg(LEG_L, bone)}</g>', f'<g class="lR">{bone_leg(LEG_R, bone)}</g>')
    armb = limb(*SH_L, *HAND_B, bone, 12) + hand(HAND_B, bone, 11)
    ribs = ''.join(f'<path d="M{316+i*2} {252+i*16} Q344 {262+i*16} {372-i*2} {252+i*16}" stroke="{bone}" stroke-width="6" fill="none" stroke-linecap="round"/>' for i in range(4))
    torso = (f'<path d="M290 222 Q282 290 292 336 L300 352 L312 338 L326 356 L340 340 L354 356 L368 338 L380 352 L388 336 Q398 290 390 222 Q340 206 290 222Z" fill="{purple}" {OL}/>'
             f'<ellipse cx="344" cy="282" rx="36" ry="46" fill="#140e18"/>' + ribs +
             f'<path d="M344 236 L344 328" stroke="{bone}" stroke-width="7" stroke-linecap="round"/>'
             f'<path d="M290 328 Q340 340 390 326" stroke="#7d6a4a" stroke-width="6" fill="none"/>')
    if st == 'captured':
        eyes = ''.join(f'<ellipse cx="{x}" cy="152" rx="15" ry="17" fill="#1b1420"/>' for x in (330, 378))
    else:
        eyes = ''.join(f'<ellipse cx="{x}" cy="152" rx="15" ry="17" fill="#1b1420"/><g class="ey"><circle cx="{x+2}" cy="154" r="10" fill="{glow}" opacity=".35"/><circle cx="{x+2}" cy="154" r="5.5" fill="{glow}"/></g>' for x in (330, 378))
    jaw_open = st in ('attack', 'captured')
    jaw = (f'<path d="M312 {196 if not jaw_open else 204} Q344 {228 if not jaw_open else 238} 386 {194 if not jaw_open else 202} L382 {184 if not jaw_open else 192} Q344 {206 if not jaw_open else 214} 316 {186 if not jaw_open else 194}Z" fill="{bone}" {OL}/>')
    head = (jaw + f'<path d="M282 150 Q282 88 340 86 Q402 88 402 150 Q402 192 378 196 L310 196 Q282 192 282 150Z" fill="{bone}" {OL}/>'
            + eyes +
            f'<path d="M356 168 L364 182 L348 182Z" fill="#1b1420"/>'
            + ''.join(f'<path d="M{x} 184 L{x} 198" stroke="{INK}" stroke-width="3"/>' for x in (322, 336, 350, 364, 378)) +
            f'<path d="M300 116 L312 128 L306 138" stroke="#a89f86" stroke-width="3" fill="none"/>'
            f'<path d="M290 104 Q240 92 238 40 Q262 76 300 88Z" fill="#d8cfb0" {OL}/>'
            f'<path d="M390 100 Q440 88 446 36 Q418 72 380 84Z" fill="#d8cfb0" {OL}/>'
            f'<path d="M280 128 Q282 74 340 72 Q398 74 400 128 Q340 106 280 128Z" fill="{iron}" {OL}/>'
            f'<path d="M298 92 Q314 80 332 78" stroke="#8a8491" stroke-width="5" fill="none" stroke-linecap="round"/>')
    wpn = (f'<path d="M418 268 L436 278 L482 150 L472 124 L458 146 Z" fill="#9aa08a" {OL}/>'
           f'<path d="M446 232 l10 4 l-6 8 Z M466 178 l9 3 l-6 7Z" fill="#7d6a4a"/>'
           f'<path class="wg2" d="M440 248 L462 186" stroke="{glow}" stroke-width="3" stroke-linecap="round" stroke-dasharray="8 10"/>'
           f'<path d="M404 266 L450 286" stroke="{INK}" stroke-width="13" stroke-linecap="round"/><path d="M404 266 L450 286" stroke="{iron}" stroke-width="7" stroke-linecap="round"/>'
           f'<circle cx="414" cy="316" r="8" fill="{iron}" {OLT}/>')
    armf = limb(*SH_F, *HAND_F, bone, 12)
    return dict(legs=legs, armb=armb, torso=torso, head=head, armf=armf, wpn=wpn, handf=hand(HAND_F, bone, 11),
                tip=(474, 132), glow=glow, glow2='#d4ffcc', kind='slash')


def hood(fill, trim, face, tail):
    return (f'<path d="M304 96 Q238 104 {tail}Z" fill="{fill}" {OL}/>'
            f'<path d="M340 70 C406 70 420 128 416 198 Q414 220 394 228 L286 228 Q266 220 264 198 C260 128 274 70 340 70Z" fill="{fill}" {OL}/>'
            f'<ellipse cx="352" cy="166" rx="47" ry="51" fill="{face}"/>'
            f'<ellipse cx="352" cy="166" rx="47" ry="51" fill="none" stroke="{trim}" stroke-width="7"/>')


def dawn(st):
    skin, cream, gold, glow = '#e6bd95', '#f4ecd0', '#d9b45a', '#ffd24a'
    legs = (f'<g class="lL"><ellipse cx="{LEG_L}" cy="428" rx="22" ry="11" fill="#8a5a2a" {OL}/></g>',
            f'<g class="lR"><ellipse cx="{LEG_R+6}" cy="430" rx="22" ry="11" fill="#8a5a2a" {OL}/></g>')
    armb = limb(*SH_L, *HAND_B, cream, 26) + hand(HAND_B, skin)
    rays = ''.join(f'<path d="M346 {270-24} L346 {270-17}" stroke="{gold}" stroke-width="4" stroke-linecap="round" transform="rotate({a} 346 270)"/>' for a in range(0, 360, 45))
    torso = (f'<g class="rb"><path d="M292 218 Q272 320 248 424 Q340 444 432 424 Q408 320 388 218Z" fill="{cream}" {OL}/>'
             f'<path d="M252 408 Q340 428 428 408" stroke="{gold}" stroke-width="8" fill="none"/>'
             f'<path d="M300 300 Q290 360 276 410 M384 300 Q394 360 408 410" stroke="#d8cba4" stroke-width="4" fill="none"/></g>'
             f'<path d="M298 236 L384 312" stroke="{gold}" stroke-width="10" stroke-linecap="round"/>'
             f'<circle cx="346" cy="270" r="13" fill="{gold}" {OLT}/>' + rays)
    face_bits = eyes_human(st, 340, 374, 172) + mouth(st, 360, 198)
    head = (hood(cream, gold, skin, '236 178 Q258 140 302 134') + f'<path d="M306 150 Q352 100 398 150 Q352 126 306 150Z" fill="#d8cba4"/>'
            + face_bits + '<ellipse cx="326" cy="194" rx="8" ry="5" fill="#ff7a7a" opacity=".35"/><ellipse cx="390" cy="192" rx="7" ry="5" fill="#ff7a7a" opacity=".35"/>')
    wpn = (limb(*HAND_F, 458, 232, '#b8902f', 8) +
           f'<circle class="wg" cx="462" cy="226" r="26" fill="{glow}" opacity=".45"/>' + star(462, 226, 18, '#ffe08a', '', OLT))
    armf = limb(*SH_F, *HAND_F, cream, 26)
    return dict(legs=legs, armb=armb, torso=torso, head=head, armf=armf, wpn=wpn, handf=hand(HAND_F, skin),
                tip=(462, 226), glow=glow, glow2='#fff6c8', kind='cast')


def dusk(st):
    robe, trim, glow, pale = '#2a1c44', '#b060ff', '#b060ff', '#d7b0ff'
    wisps = ''.join(f'<path class="ws" style="animation-delay:{d}s" d="M{x} 418 Q{x-10} 440 {x+4} 456" stroke="{glow}" stroke-width="7" fill="none" stroke-linecap="round" opacity=".6"/>' for x, d in ((290, 0), (340, .3), (392, .6)))
    legs = ('', '')
    armb = limb(*SH_L, *HAND_B, robe, 26) + hand(HAND_B, '#3b2d55')
    torso = (f'<g class="rb">{wisps}'
             f'<path d="M292 218 Q270 316 250 406 L266 428 L284 410 L302 432 L320 412 L340 434 L360 412 L378 432 L396 410 L414 428 L430 406 Q410 316 388 218Z" fill="{robe}" {OL}/>'
             f'<path d="M262 398 L284 404 L302 422 M378 422 L396 402 L418 398" stroke="{trim}" stroke-width="5" fill="none" stroke-linejoin="round"/>'
             f'<path d="M304 300 Q292 350 280 396 M380 300 Q392 350 402 396" stroke="#3d2a60" stroke-width="4" fill="none"/></g>'
             f'<path d="M298 236 L384 312" stroke="{trim}" stroke-width="8" stroke-linecap="round"/>'
             f'<path d="M354 254 A18 18 0 1 0 354 290 A13 13 0 1 1 354 254Z" fill="{pale}" {OLT}/>')
    if st == 'captured':
        eyes = ''.join(f'<path d="M{x-9} 160 L{x+9} 174 M{x+9} 160 L{x-9} 174" stroke="#6d5290" stroke-width="5" stroke-linecap="round"/>' for x in (338, 376))
    else:
        eyes = ''.join(f'<g class="ey"><ellipse cx="{x}" cy="167" rx="16" ry="11" fill="{glow}" opacity=".35"/><path d="M{x-11} 168 Q{x} 156 {x+11} 166 Q{x} 176 {x-11} 168Z" fill="{pale}"/></g>' for x in (338, 376))
    head = hood(robe, trim, '#0d0716', '232 186 L250 168 L246 150 Q262 136 302 134') + eyes
    wpn = (limb(*HAND_F, 456, 232, '#6d5290', 8) +
           f'<circle class="wg" cx="460" cy="222" r="26" fill="{glow}" opacity=".45"/>'
           f'<path d="M460 194 L474 222 L460 252 L446 222Z" fill="{pale}" {OLT}/><path d="M460 202 L466 222 L460 240" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/>')
    armf = limb(*SH_F, *HAND_F, robe, 26)
    return dict(legs=legs, armb=armb, torso=torso, head=head, armf=armf, wpn=wpn, handf=hand(HAND_F, '#3b2d55'),
                tip=(460, 222), glow=glow, glow2='#efe0ff', kind='cast', float=1)


CHARS = {  # folder -> (file prefix, title, draw)
    'armada-white-pawn': ('aw-ensign-', 'Concord Fleet ensign', concord),
    'armada-black-pawn': ('ab-trooper-', 'Kragh Dominion trooper', kragh),
    'dungeon-white-pawn': ('dw-militia-', 'Adventurers militia spearman', militia),
    'dungeon-black-pawn': ('db-skeleton-', 'Dungeon Horde skeleton', skeleton),
    'arcane-white-pawn': ('cw-apprentice-', 'Dawn Circle apprentice', dawn),
    'arcane-black-pawn': ('cb-shade-', 'Dusk Circle shade', dusk),
}

# Arm pose (degrees about the front shoulder) per state and attack kind.
POSE = {'selected': {'shoot': -12, 'thrust': -8, 'slash': -14, 'cast': -20},
        'captured': {'shoot': 48, 'thrust': 34, 'slash': 55, 'cast': 50},
        'promotion': {'shoot': -70, 'thrust': -14, 'slash': -18, 'cast': -48}}

BASE_CSS = '''
.bd{transform-origin:340px 432px}
.lL{transform-origin:314px 340px}.lR{transform-origin:366px 340px}
.ab{transform-origin:296px 236px}.af{transform-origin:386px 236px}
.lean{transform-origin:340px 432px}
.ey{transform-box:fill-box;transform-origin:center}
.wg,.fl,.rg,.st,.up{transform-box:fill-box;transform-origin:center}
.rb{transform-origin:340px 230px}
@keyframes br{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes bl{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
@keyframes gw{0%,100%{opacity:.35;transform:scale(.8)}50%{opacity:.75;transform:scale(1.15)}}
@keyframes g2{0%,100%{opacity:1}50%{opacity:.45}}
@keyframes sw{0%,100%{transform:rotate(0)}50%{transform:rotate(5deg)}}
@keyframes sf{0%,100%{transform:rotate(0)}50%{transform:rotate(-4deg)}}
@keyframes rs{0%,100%{transform:skewX(0)}50%{transform:skewX(-3deg)}}
@keyframes ws{0%,100%{opacity:.25;transform:translateY(0)}50%{opacity:.75;transform:translateY(6px)}}
'''
LIVE_CSS = '''
.ey{animation:bl 3.6s infinite}.wg{animation:gw 1.6s ease-in-out infinite}.wg2{animation:g2 1.4s ease-in-out infinite}
.ws{animation:ws 1.2s ease-in-out infinite}
'''
STATE_CSS = {
    'idle': '''.bd{animation:br 2.4s ease-in-out infinite}.ab{animation:sw 2.4s ease-in-out infinite}.af{animation:sf 2.4s ease-in-out infinite}
.rb{animation:rs 2.4s ease-in-out infinite}''',
    'selected': '''.bd{animation:hp .9s ease-in-out infinite}.af{animation:sf .9s ease-in-out infinite}
@keyframes hp{0%,100%{transform:translateY(0)}35%{transform:translateY(-18px)}60%{transform:translateY(-3px)}}
.rg{animation:rg 1.1s ease-out infinite}@keyframes rg{0%{opacity:1;transform:scale(.75)}100%{opacity:0;transform:scale(1.3)}}
.au{animation:au 1.1s ease-in-out infinite}@keyframes au{0%,100%{opacity:.55}50%{opacity:1}}
.wg{animation-duration:.6s}.st{animation:tw 1.1s ease-in-out infinite}.st.s2{animation-delay:.55s}
@keyframes tw{0%,100%{opacity:0;transform:scale(.3) rotate(0)}50%{opacity:1;transform:scale(1) rotate(45deg)}}''',
    'moving': '''.bd{animation:bo .5s ease-in-out infinite}.lL{animation:stA .5s linear infinite}.lR{animation:stB .5s linear infinite}
.ab{animation:stB .5s linear infinite}.af{animation:sw .5s ease-in-out infinite}.rb{animation:rw .5s ease-in-out infinite}
@keyframes bo{0%,50%,100%{transform:translateY(0)}25%,75%{transform:translateY(-10px)}}
@keyframes stA{0%,100%{transform:rotate(22deg)}50%{transform:rotate(-22deg)}}
@keyframes stB{0%,100%{transform:rotate(-22deg)}50%{transform:rotate(22deg)}}
@keyframes rw{0%,100%{transform:skewX(6deg)}50%{transform:skewX(-6deg)}}
.ds{animation:ds .5s linear infinite}.ds.s2{animation-delay:.25s}
@keyframes ds{0%{opacity:.8;transform:translate(0,0) scale(.6)}100%{opacity:0;transform:translate(-60px,-10px) scale(1.4)}}
.ds{transform-box:fill-box;transform-origin:center}''',
    'captured': '''.bd{animation:wb 1.2s ease-in-out infinite}@keyframes wb{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
.st{animation:sp 1.2s linear infinite}.st.s2{animation-delay:-.4s}.st.s3{animation-delay:-.8s}
@keyframes sp{0%{transform:rotate(0) scale(.7);opacity:.4}50%{transform:rotate(180deg) scale(1.1);opacity:1}100%{transform:rotate(360deg) scale(.7);opacity:.4}}''',
    'promotion': '''.bd{animation:fl2 1.8s ease-in-out infinite}@keyframes fl2{0%,100%{transform:translateY(0)}50%{transform:translateY(-16px)}}
.au{animation:au 1.8s ease-in-out infinite}@keyframes au{0%,100%{opacity:.6}50%{opacity:1}}
.up{animation:up 1.8s ease-out infinite}@keyframes up{0%{transform:translateY(0) scale(1);opacity:0}15%{opacity:1}100%{transform:translateY(-300px) scale(.4);opacity:0}}
.wg{animation:gw .5s ease-in-out infinite}.cv{animation:cv 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes cv{0%,100%{transform:translateY(0) scale(.9);opacity:.7}50%{transform:translateY(-10px) scale(1.1);opacity:1}}
.rg{animation:rg 1.8s ease-out infinite}@keyframes rg{0%{opacity:1;transform:scale(.7)}100%{opacity:0;transform:scale(1.4)}}''',
}
ATTACK_CSS = {  # every attack loop: hit lands at ~55% (KCFG atk.hit in index.html)
    'shoot': '''.af{animation:aim 1.3s cubic-bezier(.4,0,.2,1) infinite}
@keyframes aim{0%,100%{transform:rotate(0)}30%,50%{transform:rotate(-8deg)}56%{transform:translateX(-14px) rotate(-22deg)}72%{transform:rotate(-6deg)}}
.lean{animation:kick 1.3s infinite}@keyframes kick{0%,50%,100%{transform:none}57%{transform:translateX(-8px) rotate(-3deg)}75%{transform:none}}
.wg{animation:chg 1.3s infinite}@keyframes chg{0%{opacity:.2;transform:scale(.4)}50%{opacity:1;transform:scale(1.7)}56%,100%{opacity:.2;transform:scale(.5)}}
.fl{opacity:0;animation:fl 1.3s infinite}@keyframes fl{0%,53%{opacity:0;transform:scale(.3)}57%{opacity:1;transform:scale(1)}72%,100%{opacity:0;transform:scale(1.7)}}''',
    'thrust': '''.af{animation:th 1.3s cubic-bezier(.5,0,.2,1) infinite}
@keyframes th{0%,100%{transform:rotate(0)}32%{transform:translateX(-30px) rotate(52deg)}50%{transform:translateX(-34px) rotate(72deg)}58%,70%{transform:translateX(44px) rotate(72deg)}}
.lean{animation:ln 1.3s infinite}@keyframes ln{0%,32%,100%{transform:none}48%{transform:rotate(-4deg)}58%,70%{transform:translateX(10px) rotate(5deg)}}
.fl{opacity:0;animation:fl 1.3s infinite}@keyframes fl{0%,55%{opacity:0;transform:scale(.3)}59%{opacity:1;transform:scale(1)}74%,100%{opacity:0;transform:scale(1.7)}}''',
    'slash': '''.af{animation:sl 1.3s cubic-bezier(.5,0,.2,1) infinite}
@keyframes sl{0%,100%{transform:rotate(0)}35%,44%{transform:rotate(-28deg)}56%,70%{transform:rotate(92deg)}}
.lean{animation:ln 1.3s infinite}@keyframes ln{0%,30%,100%{transform:none}42%{transform:rotate(-4deg)}56%,70%{transform:translateX(8px) rotate(5deg)}}
.tr{opacity:0;animation:tr 1.3s infinite}@keyframes tr{0%,48%{opacity:0}55%{opacity:.95}68%,100%{opacity:0}}
.fl{opacity:0;animation:fl 1.3s infinite}@keyframes fl{0%,54%{opacity:0;transform:scale(.3)}58%{opacity:1;transform:scale(1)}72%,100%{opacity:0;transform:scale(1.7)}}''',
    'cast': '''.af{animation:cs 1.4s cubic-bezier(.5,0,.2,1) infinite}
@keyframes cs{0%,100%{transform:rotate(0)}35%,44%{transform:rotate(30deg)}56%,72%{transform:rotate(-16deg)}}
.lean{animation:ln 1.4s infinite}@keyframes ln{0%,30%,100%{transform:none}42%{transform:rotate(-3deg)}56%,72%{transform:translateX(6px) rotate(3deg)}}
.wg{animation:chg 1.4s infinite}@keyframes chg{0%{opacity:.3;transform:scale(.6)}44%{opacity:1;transform:scale(1.3)}56%,100%{opacity:.3;transform:scale(.6)}}
.rn{opacity:0;transform-box:fill-box;transform-origin:center;animation:rn 1.4s linear infinite}
@keyframes rn{0%,50%{opacity:0;transform:rotate(0) scale(.4)}58%{opacity:1;transform:rotate(60deg) scale(1)}80%,100%{opacity:0;transform:rotate(160deg) scale(1.3)}}
.fl{opacity:0;animation:fl 1.4s infinite}@keyframes fl{0%,54%{opacity:0;transform:scale(.3)}58%{opacity:1;transform:scale(1)}74%,100%{opacity:0;transform:scale(1.7)}}''',
}
REDUCE = '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'


def figure(c, st):
    kind, g, g2 = c['kind'], c['glow'], c['glow2']
    pose = POSE.get(st, {}).get(kind, 0)
    tx, ty = c['tip']
    pre, post, defs = [], [], ''
    flash = ''
    if st in ('selected', 'promotion'):
        defs = (f'<defs><radialGradient id="ag"><stop offset="0" stop-color="{g}" stop-opacity=".55"/>'
                f'<stop offset="1" stop-color="{g}" stop-opacity="0"/></radialGradient>'
                f'<linearGradient id="bm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{g}" stop-opacity=".7"/>'
                f'<stop offset="1" stop-color="{g}" stop-opacity="0"/></linearGradient></defs>')
        if st == 'promotion':
            pre.append('<path class="au" d="M262 434 L284 20 L396 20 L418 434Z" fill="url(#bm)"/>')
        pre.append('<circle class="au" cx="340" cy="260" r="165" fill="url(#ag)"/>')
        pre.append(f'<ellipse class="rg" cx="340" cy="432" rx="120" ry="20" fill="none" stroke="{g}" stroke-width="6"/>')
        pre.append(f'<ellipse cx="340" cy="432" rx="112" ry="17" fill="none" stroke="{g}" stroke-width="4" opacity=".55"/>')
    if st == 'selected':
        post.append(star(258, 140, 14, g2, 'st', OLT) + star(430, 96, 11, g2, 'st s2', OLT))
    if st == 'moving' and not c.get('float'):
        post.append(''.join(f'<ellipse class="ds{" s2" if i else ""}" cx="{300+i*20}" cy="426" rx="14" ry="9" fill="#d8d2c4" opacity=".7"/>' for i in range(2)))
    if st == 'captured':
        post.append(star(282, 54, 14, '#ffe27a', 'st', OLT) + star(340, 34, 14, '#ffe27a', 'st s2', OLT) + star(400, 54, 14, '#ffe27a', 'st s3', OLT))
    if st == 'promotion':
        for i, (x, d) in enumerate(((270, 0), (318, .5), (366, .25), (410, .9), (294, 1.2), (388, 1.5))):
            post.append(f'<path class="up" style="animation-delay:{d}s" d="M{x} {400-i*8} l8 12 l-8 12 l-8 -12Z" fill="{g2}"/>')
        post.append(f'<path class="cv" d="M312 44 L340 18 L368 44 L356 44 L340 30 L324 44Z" fill="{g}" {OLT}/>')
    if st == 'attack':
        if kind == 'shoot':
            flash = (f'<g class="fl"><circle cx="{tx+16}" cy="{ty}" r="30" fill="{g}" opacity=".6"/>'
                     + star(tx + 16, ty, 26, g2) + '</g>')
        elif kind == 'thrust':
            flash = f'<g class="fl">{star(tx, ty - 10, 34, g2)}<circle cx="{tx}" cy="{ty-10}" r="12" fill="#fff"/></g>'
        elif kind == 'slash':
            flash = f'<g class="fl">{star(tx, ty, 30, g2)}</g>'
            post.append(f'<path class="tr" d="M420 120 Q540 170 500 330 Q500 210 420 120Z" fill="{g}" opacity=".8"/>')
        else:
            flash = f'<g class="fl">{star(tx, ty, 34, g2)}</g>'
            post.append(f'<g class="rn"><circle cx="505" cy="220" r="44" fill="none" stroke="{g}" stroke-width="5" stroke-dasharray="14 8"/>'
                        f'<circle cx="505" cy="220" r="28" fill="none" stroke="{g2}" stroke-width="3"/>{star(505, 220, 16, g2)}</g>')
    legs = ''.join(c['legs'])
    armf = (f'<g class="af"><g transform="rotate({pose} 386 236)">{c["wpn"]}{c["armf"]}{c["handf"]}{flash}</g></g>')
    if kind == 'thrust':  # spear shaft sits in front of the arm, hand wraps it
        armf = (f'<g class="af"><g transform="rotate({pose} 386 236)">{c["armf"]}{c["wpn"]}{c["handf"]}{flash}</g></g>')
    lean = {'captured': 'rotate(-12 340 432)', 'moving': 'rotate(5 340 432)'}.get(st, '')
    fy = 'translate(0 -16)' if c.get('float') else ''
    shadow = f'<ellipse cx="340" cy="436" rx="{96 if c.get("float") else 112}" ry="10" fill="#000" opacity=".2"/>'
    body = (f'<g class="ab">{c["armb"]}</g>{legs}{c["torso"]}{c.get("front_b", "")}'
            f'<g class="hd">{c["head"]}</g>{armf}')
    return defs + ''.join(pre) + shadow + (
        f'<g class="lean"><g transform="{lean}"><g class="bd"><g transform="{fy}">{body}</g></g></g></g>') + ''.join(post)


def hint(kind, c, emblem):
    g, g2 = c['glow'], c['glow2']
    css = ('.h{transform-box:fill-box;transform-origin:center;animation:hp 1.4s ease-in-out infinite}'
           '@keyframes hp{0%,100%{transform:scale(.85);opacity:.7}50%{transform:scale(1.1);opacity:1}}')
    if kind == 'move':
        body = f'<circle class="h" cx="340" cy="240" r="40" fill="{g}" opacity=".85"/><circle cx="340" cy="240" r="17" fill="{g2}"/>'
    else:
        br = ''.join(f'<path d="M{x} {y+dy*46} L{x} {y} L{x+dx*46} {y}" stroke="{g}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                     for x, y, dx, dy in ((160, 60, 1, 1), (520, 60, -1, 1), (160, 420, 1, -1), (520, 420, -1, -1)))
        body = br + f'<g class="h">{emblem}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="140 40 400 400" width="400" height="400" role="img">'
            f'<title>{"Legal move" if kind == "move" else "Capture"} marker</title><style>{css}{REDUCE}</style>{body}</svg>')


EMBLEM = {
    'armada-white-pawn': lambda g, g2: f'<circle cx="340" cy="240" r="58" fill="none" stroke="{g}" stroke-width="10"/><path d="M340 168 L340 312 M268 240 L412 240" stroke="{g2}" stroke-width="8"/>',
    'armada-black-pawn': lambda g, g2: f'<path d="M340 176 L398 240 L340 304 L282 240Z" fill="none" stroke="{g}" stroke-width="10"/><circle cx="340" cy="240" r="14" fill="{g2}"/>',
    'dungeon-white-pawn': lambda g, g2: f'<path d="M282 182 L398 298 M398 182 L282 298" stroke="{g}" stroke-width="14" stroke-linecap="round"/><path d="M270 206 L306 170 M374 170 L410 206" stroke="{g2}" stroke-width="10" stroke-linecap="round"/>',
    'dungeon-black-pawn': lambda g, g2: f'<path d="M300 236 Q300 186 340 186 Q380 186 380 236 Q380 262 366 266 L366 286 L314 286 L314 266 Q300 262 300 236Z" fill="none" stroke="{g}" stroke-width="9"/><circle cx="324" cy="236" r="10" fill="{g2}"/><circle cx="356" cy="236" r="10" fill="{g2}"/>',
    'arcane-white-pawn': lambda g, g2: star(340, 240, 60, 'none', '', f'stroke="{g}" stroke-width="9" stroke-linejoin="round"') + f'<circle cx="340" cy="240" r="12" fill="{g2}"/>',
    'arcane-black-pawn': lambda g, g2: f'<path d="M352 182 A60 60 0 1 0 352 298 A44 44 0 1 1 352 182Z" fill="none" stroke="{g}" stroke-width="9" stroke-linejoin="round"/><circle cx="380" cy="214" r="8" fill="{g2}"/>',
}


def main():
    for folder, (pfx, title, draw) in CHARS.items():
        d = os.path.join('art', folder)
        os.makedirs(d, exist_ok=True)
        for st in ('idle', 'selected', 'moving', 'attack', 'captured', 'promotion', 'icon'):
            c = draw(st if st != 'icon' else 'idle')
            if st == 'icon':
                css = BASE_CSS
            else:
                css = BASE_CSS + (LIVE_CSS if st != 'captured' else '') + (ATTACK_CSS[c['kind']] if st == 'attack' else STATE_CSS[st])
                if st == 'captured':
                    css += '.wg,.wg2{opacity:.25}'
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="135 20 410 430" width="410" height="430" role="img">'
                   f'<title>{title} {st}</title><style>{css.strip()}\n{REDUCE}</style>{figure(c, "idle" if st == "icon" else st)}</svg>\n')
            open(os.path.join(d, f'{pfx}{st}.svg'), 'w').write(svg)
        c = draw('idle')
        short = pfx.split('-')[0]
        open(os.path.join(d, f'{short}-hint-move.svg'), 'w').write(hint('move', c, '') + '\n')
        open(os.path.join(d, f'{short}-hint-capture.svg'), 'w').write(hint('capture', c, EMBLEM[folder](c['glow'], c['glow2'])) + '\n')
        print('wrote', d)


if __name__ == '__main__':
    main()
