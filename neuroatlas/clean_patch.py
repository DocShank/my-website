from pathlib import Path
import re, sys
p=Path(sys.argv[1])
s=p.read_text()
s=s.replace('MRI-native brain anatomy learning · resilient 2D MPR + optional 3D','MRI-native brain anatomy learning · clean clinical MPR + optional 3D')
s=s.replace('The core slice viewer uses Canvas 2D, so the brain remains visible even when WebGL is unavailable.','Real MRI first. Labels and tissue overlays stay off until you ask for them.')
s=s.replace('TISSUE OVERLAY <b id="tv">16%</b>','TISSUE OVERLAY <b id="tv">0%</b>').replace('min="0" max="70" value="16"','min="0" max="70" value="0"',1)
s=s.replace('REGIONAL ATLAS <b id="av">12%</b>','REGIONAL ATLAS <b id="av">0%</b>').replace('min="0" max="60" value="12"','min="0" max="60" value="0"',1)
s=s.replace('<button id="lab" class="on">AUTO LABELS</button><button id="bnd" class="on">BOUNDARIES</button>','<button id="lab">SELECTED LABEL</button><button id="bnd">BOUNDARIES</button><button id="clean" class="on">CLEAN MRI</button>')
s=s.replace("let brain,tissue,atlas,info,labels=[],mode='multi',plane='axial',focus=0,showLabels=true,bounds=true,nv3d,threeD=false;","let brain,tissue,atlas,info,labels=[],mode='multi',plane='axial',focus=0,showLabels=false,bounds=false,nv3d,threeD=false;")
start=s.find('function autoLabels('); end=s.find('function drawPanel(',start)
if start>=0 and end>start:
    new="""function selectedLabel(ctx,p,r){if(!showLabels)return;const a=atlas[id(pos.x,pos.y,pos.z)];if(!a)return;const n=pretty(labels[a]);if(!n)return;let ux,vy;if(p==='axial'){ux=pos.x/(info.dims[0]-1);vy=(info.dims[1]-1-pos.y)/(info.dims[1]-1)}else if(p==='coronal'){ux=pos.x/(info.dims[0]-1);vy=(info.dims[2]-1-pos.z)/(info.dims[2]-1)}else{ux=pos.y/(info.dims[1]-1);vy=(info.dims[2]-1-pos.z)/(info.dims[2]-1)}const x=r.x+ux*r.w,y=r.y+vy*r.h,t=n.length>34?n.slice(0,32)+'…':n;ctx.font='700 11px system-ui';const tw=ctx.measureText(t).width+14,tx=Math.max(r.x+7,Math.min(r.x+r.w-tw-7,x+9)),ty=Math.max(r.y+22,Math.min(r.y+r.h-18,y-10));ctx.fillStyle='rgba(3,8,13,.90)';ctx.fillRect(tx,ty-14,tw,22);ctx.strokeStyle='rgba(110,215,255,.55)';ctx.strokeRect(tx+.5,ty-13.5,tw-1,21);ctx.fillStyle='#fff';ctx.fillText(t,tx+7,ty+1)}\n"""
    s=s[:start]+new+s[end:]
s=s.replace('autoLabels(ctx,p,r);','selectedLabel(ctx,p,r);')
s=re.sub(r"function rect\(p,W,H\)\{.*?\}\nfunction selectedLabel", "function rect(p,W,H){if(mode!=='multi')return{x:10,y:10,w:W-20,h:H-20,p:mode};const g=10,topH=(H-g*3)*.54,botH=H-g*3-topH,half=(W-g*3)/2;if(p==='axial')return{x:g,y:g,w:W-g*2,h:topH,p};if(p==='coronal')return{x:g,y:g*2+topH,w:half,h:botH,p};if(p==='sagittal')return{x:g*2+half,y:g*2+topH,w:half,h:botH,p};return{x:0,y:0,w:0,h:0,p}}\nfunction selectedLabel", s, flags=re.S)
s=s.replace("if(mode==='multi'){drawPanel(ctx,'axial',rect('axial',W,H));drawPanel(ctx,'coronal',rect('coronal',W,H));drawPanel(ctx,'sagittal',rect('sagittal',W,H));drawInfo(ctx,rect('info',W,H))}else drawPanel(ctx,mode,rect(mode,W,H));","if(mode==='multi'){drawPanel(ctx,'axial',rect('axial',W,H));drawPanel(ctx,'coronal',rect('coronal',W,H));drawPanel(ctx,'sagittal',rect('sagittal',W,H))}else drawPanel(ctx,mode,rect(mode,W,H));")
s=s.replace("function foc(v,e){focus=v;[fAll,fCSF,fGM,fWM].forEach(x=>x.classList.remove('on'));e.currentTarget.classList.add('on');redraw()}","function foc(v,e){focus=v;[fAll,fCSF,fGM,fWM].forEach(x=>x.classList.remove('on'));e.currentTarget.classList.add('on');if(v&&+to.value===0){to.value=12;tv.textContent='12%'}redraw()}")
s=s.replace("$('#bnd').onclick=e=>{bounds=!bounds;e.currentTarget.classList.toggle('on',bounds);redraw()};","$('#bnd').onclick=e=>{bounds=!bounds;e.currentTarget.classList.toggle('on',bounds);if(bounds&&+to.value===0){to.value=8;tv.textContent='8%'}redraw()};$('#clean').onclick=e=>{to.value=0;ao.value=0;tv.textContent='0%';av.textContent='0%';focus=0;bounds=false;showLabels=false;[fAll,fCSF,fGM,fWM].forEach((x,i)=>x.classList.toggle('on',i===0));$('#bnd').classList.remove('on');$('#lab').classList.remove('on');e.currentTarget.classList.add('on');redraw()};")
s=s.replace("$('#learn').onclick=()=>{showLabels=true;$('#lab').classList.add('on');section();redraw()};","$('#learn').onclick=()=>{section();redraw()};")
s=s.replace("status.textContent='MRI ready · CSF/gray/white boundaries ready · regional atlas ready';","status.textContent='MRI ready · clean grayscale view active';")
s=s.replace('Blue, pink and mint boundaries make CSF, gray matter and white matter separations visible independently of regional labels.','The MRI opens clean and grayscale. Use CSF, GRAY or WHITE only when you want a tissue teaching overlay; regional atlas color is also off by default.')
p.write_text(s)
print('Applied clean premium patch', p)
