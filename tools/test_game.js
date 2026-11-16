// Headless test sweep. Run: node tools/test_game.js   (needs playwright + chromium)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const root=path.resolve(__dirname,'..');
const wrap=()=>{fs.writeFileSync(path.join(root,'_t.html'),'<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">'+fs.readFileSync(path.join(root,'index.html'),'utf8')+'</body></html>');return 'file://'+path.join(root,'_t.html');};
let fails=0;const ok=(c,msg)=>{console.log((c?'PASS ':'FAIL ')+msg);if(!c)fails++;};
(async()=>{const url=wrap();const b=await chromium.launch();
const mk=async(init)=>{const ctx=await b.newContext({viewport:{width:1100,height:900}});const p=await ctx.newPage();p.errs=[];p.on('pageerror',e=>p.errs.push(e.message));p.on('console',m=>{if(m.type()==='error')p.errs.push(m.text())});if(init)await init(p);await p.goto(url);await p.waitForTimeout(500);return p;};
// ---------- 1. rules ----------
let p=await mk();
const perft=await p.evaluate(()=>{
  const fen=f=>{const [rows,turn,cs,ep]=f.split(' ');const b=Array(64).fill(null);rows.split('/').forEach((row,r)=>{let x=0;for(const ch of row){if(/\d/.test(ch))x+=+ch;else{b[r*8+x]=(ch===ch.toUpperCase()?'w':'b')+ch.toLowerCase();x++;}}});
    return {b,turn,castle:{wK:+cs.includes('K'),wQ:+cs.includes('Q'),bK:+cs.includes('k'),bQ:+cs.includes('q')},ep:ep==='-'?-1:('abcdefgh'.indexOf(ep[0])+(8-+ep[1])*8),half:0};};
  const pf=(s,d)=>{if(!d)return 1;let n=0;for(const m of legal(s))n+=pf(applyMove(s,m),d-1);return n;};
  return [['start',pf(initial(),4),197281],
   ['kiwipete',pf(fen('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -'),3),97862],
   ['pos3',pf(fen('8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -'),4),43238],
   ['pos4',pf(fen('r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq -'),3),9467],
   ['pos5',pf(fen('rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ -'),3),62379]];});
for(const [n,got,want] of perft)ok(got===want,`perft ${n}: ${got} (want ${want})`);
// ---------- 2. random playouts, battles off ----------
const consistent=()=>p.evaluate(()=>{const n=state.b.filter(Boolean).length,d=document.querySelectorAll('#pieces .piece').length;return busy===0&&n===d&&!document.querySelector('.reticle');});
const playout=async(n,pref)=>p.evaluate(async({n,pref})=>{let c=0;for(let i=0;i<n&&!result;i++){const ms=legal(state);const caps=ms.filter(m=>m.cap>=0||m.promo||m.castle);const m=(pref&&caps.length&&Math.random()<pref)?caps[Math.random()*caps.length|0]:ms[Math.random()*ms.length|0];await enqueue(()=>play(m,false));c++;}return [c,result&&result.type];},{n,pref});
await p.click('[data-speed=off]');
for(let g=0;g<6;g++){await p.evaluate(()=>rebuild([]));const r=await playout(400,.5);ok(await consistent(),`fast playout ${g}: ${r[0]} moves, result ${r[1]}`);}
ok(p.errs.length===0,'no page errors in fast playouts '+p.errs.slice(0,3).join(' | '));
// ---------- 3. playouts with battles, each realm, incl. flipped ----------
await p.click('[data-speed=quick]');
for(const [k,flip] of [['temporal',0],['armada',1],['dungeon',0],['arcane',1]]){await p.click(`[data-k=${k}]`);await p.evaluate(f=>{rebuild([]);flipped=!!f;render();},flip);const r=await playout(36,.85);ok(await consistent(),`battle playout ${k}${flip?' flipped':''}: ${r[0]} moves`);}
ok(p.errs.length===0,'no page errors in battle playouts '+p.errs.slice(0,3).join(' | '));
// ---------- 4. special moves through the real click path ----------
const click=async(pg,sq)=>{const r=await pg.$eval('#board',e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.width]});const fl=await pg.evaluate(()=>flipped);let f='abcdefgh'.indexOf(sq[0]),rk=8-+sq[1];if(fl){f=7-f;rk=7-rk;}await pg.mouse.click(r[0]+(f+.5)*r[2]/8,r[1]+(rk+.5)*r[2]/8);};
const idle=pg=>pg.waitForFunction(()=>busy===0,{timeout:30000});
const mv=async(pg,a,c,promo)=>{await click(pg,a);await click(pg,c);if(promo!==undefined){await pg.waitForSelector('.promo button');await pg.click(`.promo button[data-p=${promo}]`);}await pg.waitForTimeout(60);await idle(pg);};
await p.click('[data-k=temporal]');await p.click('[data-speed=full]');await p.evaluate(()=>{flipped=false;rebuild(['e2e4','a7a6','e4e5','d7d5']);});
await mv(p,'e5','d6');ok(await p.evaluate(()=>sans.at(-1)==='exd6'&&!state.b[27]),'en passant by click removes the pawn');
await p.evaluate(()=>rebuild(['e2e4','e7e5','g1f3','g8f6','f1c4','f8c5']));
await mv(p,'e1','g1');ok(await p.evaluate(()=>sans.at(-1)==='O-O'&&state.b[61]==='wr'&&state.b[62]==='wk'),'white castles kingside by click');
await mv(p,'e8','g8');ok(await p.evaluate(()=>sans.at(-1)==='O-O'&&state.b[5]==='br'),'black castles kingside by click');
await p.evaluate(()=>rebuild(['a2a4','b7b5','a4b5','a7a6','b5a6','h7h6','a6a7','h6h5']));
await mv(p,'a7','b8','n');ok(await p.evaluate(()=>state.b[1]==='wn'&&sans.at(-1)==='axb8=N'),'white underpromotion to knight');
await p.evaluate(()=>rebuild(['f2f3','e7e5','g2g4']));await mv(p,'d8','h4');
ok(await p.evaluate(()=>result&&result.type==='mate'&&result.winner==='b'&&!!document.querySelector('.overlay.end')),'fool\'s mate ends the game with overlay');
await click(p,'e2');ok(await p.evaluate(()=>sel===-1),'no selection after game over');
await p.click('.overlay.end button');await p.waitForTimeout(200);ok(await p.evaluate(()=>moves.length===0&&!result&&!document.querySelector('.overlay.end')),'Play again resets');
// repetition
await p.click('[data-speed=off]');await p.evaluate(()=>rebuild([]));
for(const [a,c] of [['g1','f3'],['g8','f6'],['f3','g1'],['f6','g8'],['g1','f3'],['g8','f6'],['f3','g1'],['f6','g8']])await mv(p,a,c);
ok(await p.evaluate(()=>result&&result.type==='draw'),'threefold repetition is a draw');
// undo, drag, character sheets
await p.evaluate(()=>rebuild(['e2e4','d7d5']));await mv(p,'e4','d5');
ok(await p.evaluate(()=>{const top=document.querySelector('#sheetTop');return top.querySelectorAll('.slot').length===16&&top.querySelectorAll('.slot.down').length===1&&!!top.querySelector('.slot.down[data-id="11"]')&&/15 of 16/.test(top.querySelector('.count').textContent)&&document.querySelectorAll('#sheetBot .slot.down').length===0;}),'character sheet marks the d-file black pawn as fallen');
await p.click('#sheetTop .slot[data-id="11"]');ok(/d-file.*taken on move 2/.test(await p.textContent('#sheetTop .who')),'tapping a fallen character says who took it');
await p.click('#undo');await p.waitForTimeout(150);ok(await p.evaluate(()=>moves.length===2&&document.querySelectorAll('#sheetTop .slot.down').length===0&&state.b[27]==='bp'),'undo restores the captured pawn and the sheet');
{const r=await p.$eval('#board',e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.width]});const c=(f,rk)=>[r[0]+(f+.5)*r[2]/8,r[1]+(rk+.5)*r[2]/8];
 await p.mouse.move(...c(6,7));await p.mouse.down();await p.mouse.move(...c(5,5),{steps:4});await p.mouse.up();await p.waitForTimeout(60);await idle(p);
 ok(await p.evaluate(()=>sans.at(-1)==='Nf3'),'drag a piece to its square with the mouse');}
await click(p,'e7');await click(p,'e7');ok(await p.evaluate(()=>sel===-1),'tapping the selected piece again deselects it');
await p.evaluate(()=>rebuild(['a2a4','b7b5','a4b5','a7a6','b5a6','h7h6','a6a7','h6h5']));await mv(p,'a7','b8','q');
ok(await p.evaluate(()=>!!document.querySelector('#sheetBot .slot.promo[data-id="48"]')&&document.querySelectorAll('#sheetTop .slot.down').length===3),'promoted pawn is flagged on its own slot; three black losses shown');
// theme switch + new game mid-battle
await p.click('[data-speed=full]');await p.evaluate(()=>rebuild(['e2e4','d7d5']));
await click(p,'e4');await click(p,'d5');await p.waitForTimeout(800);await p.click('[data-k=dungeon]');await p.click('#newGame');await idle(p);await p.waitForTimeout(300);
ok(await p.evaluate(()=>moves.length===0)&&await consistent(),'theme switch and New game during a battle leave a clean board');
ok(p.errs.length===0,'no page errors in click tests '+p.errs.slice(0,3).join(' | '));
await p.context().close();
// ---------- 5. two devices against a shared fake store ----------
const store={};const subs=[];
const init=uid=>async pg=>{
  await pg.exposeFunction('__dbGet',pt=>store[pt]?JSON.parse(JSON.stringify(store[pt])):null);
  await pg.exposeFunction('__dbSet',async(pt,d,merge)=>{if(merge&&!store[pt])throw new Error('missing');store[pt]=merge?{...store[pt],...d}:d;for(const s of subs)if(s.pt===pt)s.pg.evaluate(([id,d])=>window.__fire(id,d),[s.id,store[pt]]).catch(()=>{});});
  await pg.exposeFunction('__dbSub',(pt,id)=>{subs.push({pt,id,pg});if(store[pt])pg.evaluate(([id,d])=>window.__fire(id,d),[id,store[pt]]).catch(()=>{});});
  await pg.addInitScript(uid=>{const cbs={};let n=0;window.__fire=(id,d)=>cbs[id]&&cbs[id]({exists:!!d,data:()=>d,metadata:{fromCache:false,hasPendingWrites:false}});
    const doc=pt=>({get:async()=>{const d=await __dbGet(pt);return {exists:!!d,data:()=>d||undefined,metadata:{fromCache:false}};},set:d=>__dbSet(pt,d,false),update:d=>__dbSet(pt,d,true),
      onSnapshot:(f)=>{const id=++n;cbs[id]=f;__dbSub(pt,id);return()=>{delete cbs[id];};}});
    window.claude={use:async name=>name==='db'?{doc}:name==='user'?{id:async()=>uid}:null};},uid);};
const A=await mk(init('u_alice')),B=await mk(init('u_bob')),C=await mk(init('u_carol'));
for(const pg of[A,B,C]){await pg.click('[data-speed=quick]');await pg.click('#modeOnline');await pg.waitForFunction(()=>!document.getElementById('create').disabled);}
await A.click('#create');await A.waitForFunction(()=>net.code&&net.color==='w');
const code=await A.evaluate(()=>net.code);
await B.fill('#joinCode',code.toLowerCase());await B.click('#join');await B.waitForFunction(()=>net.color==='b');
ok(await B.evaluate(()=>flipped===true),'joiner plays black with the board flipped');
await C.fill('#joinCode',code);await C.click('#join');await C.waitForFunction(()=>net.code);await C.waitForTimeout(300);
ok(await C.evaluate(()=>net.color===null),'third viewer is a spectator');
await click(B,'e7');ok(await B.evaluate(()=>sel===-1),'black cannot move on white\'s turn');
await mv(A,'e2','e4');await B.waitForFunction(()=>moves.length===1&&busy===0);
await click(A,'d2');ok(await A.evaluate(()=>sel===-1),'white cannot move on black\'s turn');
await mv(B,'d7','d5');await A.waitForFunction(()=>moves.length===2&&busy===0);
await mv(A,'e4','d5');await B.waitForFunction(()=>moves.length===3&&busy===0,{timeout:30000});
await mv(B,'d8','d5');await A.waitForFunction(()=>moves.length===4&&busy===0,{timeout:30000});
await C.waitForFunction(()=>moves.length===4&&busy===0,{timeout:30000});
await click(C,'b1');ok(await C.evaluate(()=>sel===-1),'spectator cannot move');
const same=await Promise.all([A,B,C].map(pg=>pg.evaluate(()=>moves.join(' '))));
ok(same[0]===same[1]&&same[1]===same[2]&&same[0]==='e2e4 d7d5 e4d5 d8d5','all three devices agree: '+same[0]);
await B.click('#newGame');await A.waitForFunction(()=>moves.length===0&&net.color==='b');
ok(await B.evaluate(()=>net.color==='w'&&moves.length===0&&flipped===false)&&await A.evaluate(()=>flipped===true),'rematch swaps sides on both devices');
await A.click('#leave');ok(await A.evaluate(()=>!net.code&&moves.length===0),'leave returns to lobby');
await A.fill('#joinCode','ZZZZZ');await A.click('#join');await A.waitForTimeout(300);ok(/No game/.test(await A.textContent('#netMsg')),'bad code shows a message');
for(const pg of[A,B,C])ok(pg.errs.length===0,'no page errors on device '+pg.errs.slice(0,3).join(' | '));
await b.close();fs.unlinkSync(path.join(root,'_t.html'));console.log(fails?`\n${fails} FAILED`:'\nALL PASSED');process.exit(fails?1:0);})().catch(e=>{console.error(e);process.exit(2);});
