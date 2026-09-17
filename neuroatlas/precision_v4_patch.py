from pathlib import Path
import re, sys

path = Path(sys.argv[1])
s = path.read_text()

# Precision v4 is deliberately narrow: preserve the protected viewer and fix
# boundary visibility, ventricular precedence, nearby-label fallback, and
# brainstem search vocabulary.
old = '<select id="outline"><option value="0.01">Outlined regions</option><option value="0">Filled regions</option><option value="-1">Black boundaries</option></select>'
new = '<select id="outline"><option value="1">Sharp color boundaries</option><option value="0.01">Thin gap boundaries</option><option value="0">Filled regions</option><option value="-1">Black boundaries</option></select>'
if old not in s:
    raise SystemExit('outline selector not found')
s = s.replace(old, new, 1)
s = s.replace("nv.setAtlasOutline(.01)", "nv.setAtlasOutline(+$('#outline').value)")

old_near = "function nearestLabel(src,r=2){const i=vIdx(src),vol=nv.volumes?.[i];if(!vol||!vol.mm2vox||!vol.getValue)return null;const mm=nv.frac2mm(nv.scene.crosshairPos),v=vol.mm2vox(mm);let best=0,bd=1e9;for(let dz=-r;dz<=r;dz++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const d=dx*dx+dy*dy+dz*dz;if(d>r*r||d>=bd)continue;const val=Math.round(vol.getValue(v[0]+dx,v[1]+dy,v[2]+dz));if(val>0){best=val;bd=d}}return best?{id:best,d:Math.sqrt(bd)}:null}"
new_near = "function nearestLabel(src,r=2){const i=vIdx(src),vol=nv.volumes?.[i];if(!vol||!vol.mm2vox||!vol.getValue)return null;const mm=nv.frac2mm(nv.scene.crosshairPos),v=vol.mm2vox(mm),pd=vol.hdr?.pixDims||vol.hdr?.pixdim||[0,1,1,1],sx=Math.abs(+pd[1]||1),sy=Math.abs(+pd[2]||1),sz=Math.abs(+pd[3]||1);let best=0,bmm=1e9,bvox=1e9;for(let dz=-r;dz<=r;dz++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const dv=dx*dx+dy*dy+dz*dz;if(dv>r*r)continue;const dm=(dx*sx)*(dx*sx)+(dy*sy)*(dy*sy)+(dz*sz)*(dz*sz);if(dm>=bmm)continue;const val=Math.round(vol.getValue(v[0]+dx,v[1]+dy,v[2]+dz));if(val>0){best=val;bmm=dm;bvox=dv}}return best?{id:best,d:Math.sqrt(bvox),mm:Math.sqrt(bmm),src}:null}\nfunction bestNearbyLabel(){const c=[];const a=nearestLabel('AAL',8);if(a&&a.mm<=8&&labels[a.id])c.push({...a,name:pretty(labels[a.id])});if(hoReady){const h=nearestLabel('HO',4);if(h&&h.mm<=8&&HO_LABELS[h.id])c.push({...h,name:HO_LABELS[h.id]})}if(jhuReady){const j=nearestLabel('JHU',6);if(j&&j.mm<=6&&JHU_LABELS[j.id])c.push({...j,name:pretty(JHU_LABELS[j.id])})}c.sort((x,y)=>x.mm-y.mm);return c[0]||null}"
if old_near not in s:
    raise SystemExit('nearestLabel block not found')
s = s.replace(old_near, new_near, 1)

needle = "'caudal medulla':{mm:[0,-38,-58],title:'Caudal medulla'},\n"
extra = "'caudal medulla':{mm:[0,-38,-58],title:'Caudal medulla'},\n'open medulla':{mm:[0,-36,-48],title:'Rostral medulla'},\n'closed medulla':{mm:[0,-38,-58],title:'Caudal medulla'},\n'upper medulla':{mm:[0,-36,-48],title:'Rostral medulla'},\n'lower medulla':{mm:[0,-38,-58],title:'Caudal medulla'},\n'upper pons':{mm:[0,-27,-28],title:'Rostral pons'},\n'lower pons':{mm:[0,-34,-39],title:'Caudal pons'},\n'upper midbrain':{mm:[0,-20,-8],title:'Rostral midbrain'},\n'lower midbrain':{mm:[0,-24,-17],title:'Caudal midbrain'},\n"
if needle not in s:
    raise SystemExit('brainstem aliases anchor not found')
s = s.replace(needle, extra, 1)

pat = re.compile(r"function moved\(d\)\{.*?\nconst nv=new Niivue", re.S)
m = pat.search(s)
if not m:
    raise SystemExit('moved function block not found')
new_moved = """function moved(d){const v=d?.values||[],pos=d?.string?`Crosshair: ${d.string}`:'Crosshair moved';let j=0,h=0,a=0;if(jhuReady&&Number.isFinite(v[jhuIndex]?.value))j=Math.round(v[jhuIndex].value);if(hoReady&&Number.isFinite(v[hoIndex]?.value))h=Math.round(v[hoIndex].value);if(Number.isFinite(v[1]?.value))a=Math.round(v[1].value);if(j>0&&JHU_LABELS[j]){const nm=pretty(JHU_LABELS[j]);selectStructure('JHU',[j],nm);teacher(JHU_LABELS[j],j,'JHU');loc.textContent=pos+' · White matter: '+nm;return}if(h>0&&HO_LABELS[h]&&/ventricle/i.test(HO_LABELS[h])){selectStructure('HO',[h],HO_LABELS[h]);teacher(HO_LABELS[h],h,'HO');loc.textContent=pos+' · '+HO_LABELS[h];return}const vent=midlineVentricleAtCursor();if(vent){for(const x of ['AAL','JHU','HO']){const i=vIdx(x);if(i>0&&nv.volumes?.[i])nv.setOpacity(i,0)}currentSource='';currentIds=[];teacherSpecial(vent);loc.textContent=pos+' · Ventricular landmark: '+vent;return}if(h===8){const level=brainstemLevel();selectStructure('HO',[8],level);teacherSpecial(level);loc.textContent=pos+' · Brainstem cross section: '+level;return}if(a>0&&labels[a]){active(a);loc.textContent=pos+' · Region: '+pretty(labels[a]);return}if(h>0&&HO_LABELS[h]){selectStructure('HO',[h],HO_LABELS[h]);teacher(HO_LABELS[h],h,'HO');loc.textContent=pos+' · '+HO_LABELS[h];return}const near=bestNearbyLabel();if(near){const dist=(Math.round(near.mm*10)/10).toFixed(near.mm<1?1:0);if(near.src==='AAL'){active(near.id);loc.textContent=pos+' · Nearest atlas region: '+near.name+' ('+dist+' mm)';return}if(near.src==='HO'){selectStructure('HO',[near.id],near.name);teacher(HO_LABELS[near.id],near.id,'HO');loc.textContent=pos+' · Nearest structural label: '+near.name+' ('+dist+' mm)';return}selectStructure('JHU',[near.id],near.name);teacher(JHU_LABELS[near.id],near.id,'JHU');loc.textContent=pos+' · Nearest white-matter label: '+near.name+' ('+dist+' mm)';return}setSel('MRI anatomy · no validated atlas boundary nearby');loc.textContent=pos+' · No validated named atlas label within the local fallback radius'}
const nv=new Niivue"""
s = s[:m.start()] + new_moved + s[m.end():]

s = s.replace("meta.textContent='Template teaching point · cross-sectional orientation'", "meta.textContent=/ventricle/i.test(title)?'Ventricular teaching landmark · MNI template orientation':'Template teaching point · cross-sectional orientation'")
s = s.replace('–','-').replace('—','-')

path.write_text(s)
print('precision v4 patch applied')
