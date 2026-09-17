from pathlib import Path
import re, sys

path = Path(sys.argv[1])
s = path.read_text()

# Precision v5: preserve the protected NeuroAtlas viewer, add premium branding,
# use filled atlas regions by default, and add an opt-in single-plane
# cross-section teaching snapshot below the viewer.

old_header = '<header class="top"><div><div class="brand">NeuroAtlas MRI</div><div class="sub">real MRI · registered anatomy · learning-first</div></div><button id="about">DATA</button></header>'
new_header = '''<header class="top"><div class="brandlock"><div class="mark" aria-hidden="true"><svg viewBox="0 0 44 44" role="img"><defs><linearGradient id="ng" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#86e5ff"/><stop offset="1" stop-color="#6c7dff"/></linearGradient></defs><rect x="2" y="2" width="40" height="40" rx="12" fill="#0b1420" stroke="url(#ng)" stroke-width="1.5"/><path d="M12 29V15l10 14V15" fill="none" stroke="url(#ng)" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M27 15h5m-5 7h7m-7 7h5" fill="none" stroke="#c9f5ff" stroke-width="2" stroke-linecap="round"/><circle cx="34" cy="15" r="2" fill="#86e5ff"/><circle cx="36" cy="22" r="2" fill="#7fbfff"/><circle cx="34" cy="29" r="2" fill="#7d8cff"/></svg></div><div><div class="brand">NeuroAtlas MRI <sup>TM</sup></div><div class="sub">real MRI · registered anatomy · learning-first</div><div class="creator">Created by Dr. Shashank Neupane and Team</div></div></div><button id="about">DATA</button></header>'''
if old_header not in s:
    raise SystemExit('header anchor not found')
s = s.replace(old_header, new_header, 1)

old_outline = '<select id="outline"><option value="1">Sharp color boundaries</option><option value="0.01">Thin gap boundaries</option><option value="0">Filled regions</option><option value="-1">Black boundaries</option></select>'
new_outline = '<select id="outline"><option value="0" selected>Filled regions</option><option value="1">Sharp color boundaries</option><option value="0.01">Thin gap boundaries</option><option value="-1">Black boundaries</option></select>'
if old_outline not in s:
    raise SystemExit('outline options anchor not found')
s = s.replace(old_outline, new_outline, 1)

old_end = '<div class="loc" id="loc">Tap or drag through the MRI to identify anatomy.</div>\n</section>'
new_end = '''<div class="loc" id="loc">Tap or drag through the MRI to identify anatomy.</div>
<div class="cross-cta"><div><b>CROSS-SECTION TEACHER</b><span id="crossHint">Switch to axial, coronal, or sagittal view to label the current slice.</span></div><button id="labelSection" disabled>LABEL THIS CROSS SECTION</button></div>
<div class="cross-panel" id="crossPanel" hidden><div class="cross-head"><div><div class="ey">LABELED CROSS SECTION</div><h3 id="crossTitle">Current slice</h3><div class="tiny" id="crossMeta"></div></div><button id="closeCross">CLOSE</button></div><div class="cross-stage" id="crossStage"><canvas id="crossCanvas"></canvas><div id="crossPins" class="cross-pins"></div></div><div class="cross-legend"><div class="cross-key"><span class="k csf"></span>CSF / ventricular <span class="k wm"></span>white matter <span class="k deep"></span>deep gray <span class="k cortex"></span>cortex / cerebellum</div><div id="crossList" class="cross-list"></div></div></div>
</section>'''
if old_end not in s:
    raise SystemExit('viewer end anchor not found')
s = s.replace(old_end, new_end, 1)

css_anchor = '.brand{font-weight:850;font-size:19px}.sub,.tiny{color:var(--muted);font-size:11px}'
css_repl = '''.brandlock{display:flex;align-items:center;gap:10px;min-width:0}.mark{width:38px;height:38px;flex:0 0 38px;filter:drop-shadow(0 6px 16px rgba(100,201,255,.14))}.mark svg{display:block;width:100%;height:100%}.brand{font-weight:850;font-size:19px;letter-spacing:-.02em}.brand sup{font-size:8px;letter-spacing:.04em;color:#9edfff;vertical-align:top;margin-left:2px}.sub,.tiny{color:var(--muted);font-size:11px}.creator{font-size:10px;color:#b8c7d7;margin-top:2px;letter-spacing:.01em}'''
if css_anchor not in s:
    raise SystemExit('brand css anchor not found')
s = s.replace(css_anchor, css_repl, 1)

css2_anchor = '.foot{text-align:center;color:var(--muted);font-size:10px;padding:10px}.error{color:#ffac9f}'
css2_repl = '''.cross-cta{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 11px;border-top:1px solid var(--line);background:#080d13}.cross-cta>div{display:flex;flex-direction:column;gap:3px}.cross-cta b{font-size:10px;letter-spacing:.14em;color:#d8e8f5}.cross-cta span{font-size:11px;color:var(--muted);line-height:1.35}.cross-cta button:disabled{opacity:.45}.cross-panel{border-top:1px solid var(--line);padding:10px;background:linear-gradient(180deg,#09111a,#070b10)}.cross-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:8px}.cross-head h3{margin:3px 0 2px;font-size:17px}.cross-stage{position:relative;background:#000;border:1px solid #26384b;border-radius:12px;overflow:hidden}.cross-stage canvas{display:block;width:100%;height:auto}.cross-pins{position:absolute;inset:0;pointer-events:none}.cross-pin{position:absolute;transform:translate(-50%,-50%);display:flex;align-items:center;gap:5px;max-width:170px;padding:3px 6px 3px 4px;border-radius:999px;background:rgba(4,8,13,.88);border:1px solid currentColor;box-shadow:0 4px 12px rgba(0,0,0,.35);font-size:9px;font-weight:800;line-height:1.15;white-space:nowrap;color:#dcecff}.cross-pin i{display:grid;place-items:center;width:18px;height:18px;flex:0 0 18px;border-radius:50%;background:currentColor;color:#061018;font-style:normal;font-size:9px}.cross-pin.csf{color:#62d9ff}.cross-pin.wm{color:#ffd27a}.cross-pin.deep{color:#ff9fd0}.cross-pin.cortex{color:#9ff0be}.cross-legend{padding:9px 2px 2px}.cross-key{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:10px;color:var(--muted);margin-bottom:8px}.cross-key .k{width:9px;height:9px;border-radius:50%;display:inline-block;margin-left:5px}.k.csf{background:#62d9ff}.k.wm{background:#ffd27a}.k.deep{background:#ff9fd0}.k.cortex{background:#9ff0be}.cross-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}.cross-item{display:flex;gap:7px;align-items:flex-start;padding:7px 8px;border:1px solid #203043;border-radius:9px;background:#0b121a;font-size:11px;color:#d5e0ea}.cross-item strong{display:grid;place-items:center;width:20px;height:20px;flex:0 0 20px;border-radius:50%;color:#061018;font-size:10px}.cross-item.csf strong{background:#62d9ff}.cross-item.wm strong{background:#ffd27a}.cross-item.deep strong{background:#ff9fd0}.cross-item.cortex strong{background:#9ff0be}.cross-item span{line-height:1.3}.cross-item small{display:block;color:var(--muted);font-size:9px;margin-top:2px}.foot{text-align:center;color:var(--muted);font-size:10px;padding:10px}.foot .creator-foot{color:#b9c9d9}.error{color:#ffac9f}'''
if css2_anchor not in s:
    raise SystemExit('cross css anchor not found')
s = s.replace(css2_anchor, css2_repl, 1)

s = s.replace('@media(max-width:430px){.bar button{font-size:11px;padding:8px}.viewer{height:52vh}.search{grid-template-columns:1fr}.search button{width:100%}}', '@media(max-width:430px){.bar button{font-size:11px;padding:8px}.viewer{height:52vh}.search{grid-template-columns:1fr}.search button{width:100%}.mark{width:34px;height:34px;flex-basis:34px}.creator{font-size:9px}.cross-cta{align-items:stretch;flex-direction:column}.cross-cta button{width:100%}.cross-list{grid-template-columns:1fr}.cross-pin .pin-name{display:none}.cross-pin{padding:3px;max-width:none}}')

s = s.replace('</main><div class="foot">Educational anatomy reference · not for diagnosis</div>', '</main><div class="foot"><span class="creator-foot">Created by Dr. Shashank Neupane and Team</span> · Educational anatomy reference · not for diagnosis</div>', 1)

old_state = "let labels=[],aalMap=null,jhuReady=false,jhuIndex=-1,hoReady=false,hoIndex=-1,currentSource='',currentIds=[],centroids={},extrasReady=null,userOpacityTouched=false;const esc="
new_state = "let labels=[],aalMap=null,jhuReady=false,jhuIndex=-1,hoReady=false,hoIndex=-1,currentSource='',currentIds=[],centroids={},extrasReady=null,userOpacityTouched=false,currentView='multi',crossCandidates=[];const esc="
if old_state not in s:
    raise SystemExit('state anchor not found')
s = s.replace(old_state, new_state, 1)

anchor = 'const nv=new Niivue'
if anchor not in s:
    raise SystemExit('Niivue anchor not found')
cross_js = r'''
function crossKind(name,src){const x=String(name||'').toLowerCase();if(/ventricle|aqueduct|csf/.test(x))return{kind:'csf',label:'CSF / ventricular',p:120};if(src==='JHU'||/internal capsule|external capsule|corona radiata|corpus callosum|corticospinal|cerebellar peduncle|cerebral peduncle|medial lemniscus|cingulum|fornix|fasciculus|thalamic radiation|sagittal stratum|tapetum/.test(x))return{kind:'wm',label:'white matter',p:105};if(/thalam|caudate|putamen|pallid|hippocamp|amygdala|accumbens|brainstem|midbrain|pons|medulla/.test(x))return{kind:'deep',label:'deep gray / brainstem',p:110};return{kind:'cortex',label:'cortex / cerebellum',p:55}}
function crossValue(src,frac){const i=vIdx(src),v=nv.volumes?.[i];if(!v||!v.mm2vox||!v.getValue)return 0;const mm=nv.frac2mm(frac),q=v.mm2vox(mm);return Math.round(v.getValue(q[0],q[1],q[2]))||0}
function crossCanonical(name){let x=String(name||'').toLowerCase().replace(/_/g,' ').replace(/\s+/g,' ').trim(),side='';if(/^left\b/.test(x)){side='l';x=x.replace(/^left\s+/,'')}else if(/^right\b/.test(x)){side='r';x=x.replace(/^right\s+/,'')}else if(/, left$/.test(x)){side='l';x=x.replace(/, left$/,'')}else if(/, right$/.test(x)){side='r';x=x.replace(/, right$/,'')}return x.replace(/nucleus/g,'').replace(/cortex/g,'').replace(/\s+/g,' ').trim()+'|'+side}
function addCrossBucket(buckets,src,id,name,x,y){if(!id||!name)return;const info=crossKind(name,src),key=crossCanonical(name);let b=buckets.get(key);if(!b||info.p>b.info.p){b={src,id,name,info,count:0,sx:0,sy:0};buckets.set(key,b)}b.count++;b.sx+=x;b.sy+=y}
function collectCrossCandidates(){const gl=$('#gl'),w=gl.width,h=gl.height;if(!w||!h)return[];const buckets=new Map(),step=Math.max(26,Math.round(Math.min(w,h)/28));for(let y=Math.floor(step/2);y<h;y+=step){for(let x=Math.floor(step/2);x<w;x+=step){const f=nv.canvasPos2frac([x,y]);if(!f||f[0]<0)continue;if(hoReady){const id=crossValue('HO',f),nm=HO_LABELS[id];if(id>0&&nm&&( /ventricle/i.test(nm)||/thalam|caudate|putamen|globus pallidus|hippocampus|amygdala|brainstem/i.test(nm)))addCrossBucket(buckets,'HO',id,nm,x,y)}if(jhuReady){const id=crossValue('JHU',f),nm=JHU_LABELS[id];if(id>0&&nm)addCrossBucket(buckets,'JHU',id,pretty(nm),x,y)}const a=crossValue('AAL',f),an=labels[a];if(a>0&&an)addCrossBucket(buckets,'AAL',a,pretty(an),x,y)}}const arr=[...buckets.values()].map(b=>({...b,x:b.sx/b.count,y:b.sy/b.count,score:b.info.p*1000+b.count}));arr.sort((a,b)=>b.score-a.score);const limit=window.innerWidth<=430?10:14;return arr.slice(0,limit)}
function renderCrossPins(){const gl=$('#gl'),pins=$('#crossPins'),list=$('#crossList');if(!crossCandidates.length||!gl.width||!gl.height)return;pins.innerHTML='';list.innerHTML='';crossCandidates.forEach((c,i)=>{const px=Math.max(4,Math.min(96,c.x/gl.width*100)),py=Math.max(5,Math.min(95,c.y/gl.height*100)),n=i+1;const pin=document.createElement('div');pin.className='cross-pin '+c.info.kind;pin.style.left=px+'%';pin.style.top=py+'%';pin.innerHTML='<i>'+n+'</i><span class="pin-name">'+esc(c.name)+'</span>';pins.appendChild(pin);const item=document.createElement('div');item.className='cross-item '+c.info.kind;item.innerHTML='<strong>'+n+'</strong><span>'+esc(c.name)+'<small>'+esc(c.info.label)+'</small></span>';list.appendChild(item)})}
function syncCrossButton(){const ok=['axial','coronal','sagittal'].includes(currentView),b=$('#labelSection'),h=$('#crossHint');b.disabled=!ok;h.textContent=ok?'Capture and label the exact '+currentView+' slice currently on screen.':'Switch to axial, coronal, or sagittal view to label the current slice.';if(!ok)$('#crossPanel').hidden=true}
async function labelCrossSection(){if(!['axial','coronal','sagittal'].includes(currentView))return;if(extrasReady)await extrasReady;const src=$('#gl'),dst=$('#crossCanvas'),panel=$('#crossPanel');dst.width=src.width;dst.height=src.height;const ctx=dst.getContext('2d');ctx.clearRect(0,0,dst.width,dst.height);ctx.drawImage(src,0,0,dst.width,dst.height);crossCandidates=collectCrossCandidates();const mm=nv.frac2mm(nv.scene.crosshairPos).map(v=>Math.round(v*10)/10);$('#crossTitle').textContent=currentView.toUpperCase()+' cross section';$('#crossMeta').textContent='Current MNI crosshair: '+mm[0]+', '+mm[1]+', '+mm[2]+' mm · '+crossCandidates.length+' teaching labels';panel.hidden=false;requestAnimationFrame(()=>{renderCrossPins();panel.scrollIntoView({behavior:'smooth',block:'nearest'})})}
'''
s = s.replace(anchor, cross_js + '\n' + anchor, 1)

old_views = "const views={multi:()=>nv.setSliceType(nv.sliceTypeMultiplanar),axial:()=>nv.setSliceType(nv.sliceTypeAxial),coronal:()=>nv.setSliceType(nv.sliceTypeCoronal),sagittal:()=>nv.setSliceType(nv.sliceTypeSagittal),render:()=>nv.setSliceType(nv.sliceTypeRender)};document.querySelectorAll('.view').forEach(b=>b.onclick=()=>{document.querySelectorAll('.view').forEach(x=>x.classList.remove('on'));b.classList.add('on');views[b.dataset.v]?.()});"
new_views = "const views={multi:()=>nv.setSliceType(nv.sliceTypeMultiplanar),axial:()=>nv.setSliceType(nv.sliceTypeAxial),coronal:()=>nv.setSliceType(nv.sliceTypeCoronal),sagittal:()=>nv.setSliceType(nv.sliceTypeSagittal),render:()=>nv.setSliceType(nv.sliceTypeRender)};document.querySelectorAll('.view').forEach(b=>b.onclick=()=>{document.querySelectorAll('.view').forEach(x=>x.classList.remove('on'));b.classList.add('on');currentView=b.dataset.v;views[currentView]?.();syncCrossButton()});"
if old_views not in s:
    raise SystemExit('view handler anchor not found')
s = s.replace(old_views, new_views, 1)

old_tail = "$('#outline').onchange=e=>nv.setAtlasOutline(+e.target.value);$('#hide').onclick=()=>{userOpacityTouched=true;op.value=0;op.oninput()};"
new_tail = "$('#outline').onchange=e=>nv.setAtlasOutline(+e.target.value);$('#labelSection').onclick=labelCrossSection;$('#closeCross').onclick=()=>{$('#crossPanel').hidden=true};window.addEventListener('resize',()=>{if(!$('#crossPanel').hidden)renderCrossPins()});syncCrossButton();$('#hide').onclick=()=>{userOpacityTouched=true;op.value=0;op.oninput()};"
if old_tail not in s:
    raise SystemExit('event anchor not found')
s = s.replace(old_tail, new_tail, 1)

old_reset = "$('#reset').onclick=()=>{userOpacityTouched=false;op.value=18;opv.textContent='18%';nv.scene.crosshairPos=nv.mm2frac([0,-18,8]);nv.setSliceType(nv.sliceTypeMultiplanar);nv.setAtlasOutline(+$('#outline').value);nv.updateGLVolume()};"
new_reset = "$('#reset').onclick=()=>{userOpacityTouched=false;op.value=18;opv.textContent='18%';nv.scene.crosshairPos=nv.mm2frac([0,-18,8]);nv.setSliceType(nv.sliceTypeMultiplanar);currentView='multi';document.querySelectorAll('.view').forEach(x=>x.classList.toggle('on',x.dataset.v==='multi'));$('#crossPanel').hidden=true;syncCrossButton();nv.setAtlasOutline(+$('#outline').value);nv.updateGLVolume()};"
if old_reset not in s:
    raise SystemExit('reset anchor not found')
s = s.replace(old_reset, new_reset, 1)

s = s.replace('–','-').replace('—','-')

path.write_text(s)
print('precision v5 patch applied')
