import gzip, struct, json, math, sys
from array import array
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
data_dir = root / 'data'
brain_path = data_dir / 'mni152_2mm_brain.nii.gz'
tissue_path = data_dir / 'mni152_2mm_fast_seg.nii.gz'
atlas_path = data_dir / 'aal.nii.gz'
json_path = data_dir / 'aal.json'

DTYPES = {
    2: ('B',1),
    4: ('h',2),
    8: ('i',4),
    16: ('f',4),
    64: ('d',8),
    256: ('b',1),
    512: ('H',2),
    768: ('I',4),
}

def load_nii(path):
    with gzip.open(path, 'rb') as f:
        raw = f.read()
    endian = '<'
    sizeof_hdr = struct.unpack('<i', raw[:4])[0]
    if sizeof_hdr != 348:
        sizeof_hdr = struct.unpack('>i', raw[:4])[0]
        if sizeof_hdr != 348:
            raise RuntimeError(f'Not NIfTI-1: {path}')
        endian = '>'
    dim = struct.unpack(endian+'8h', raw[40:56])
    ndim = dim[0]
    dims = tuple(int(x) for x in dim[1:1+ndim])
    datatype = struct.unpack(endian+'h', raw[70:72])[0]
    vox_offset = int(round(struct.unpack(endian+'f', raw[108:112])[0]))
    slope = struct.unpack(endian+'f', raw[112:116])[0] or 1.0
    inter = struct.unpack(endian+'f', raw[116:120])[0]
    _qform, sform = struct.unpack(endian+'2h', raw[252:256])
    if sform > 0:
        sx = struct.unpack(endian+'4f', raw[280:296])
        sy = struct.unpack(endian+'4f', raw[296:312])
        sz = struct.unpack(endian+'4f', raw[312:328])
        affine = [list(sx), list(sy), list(sz), [0.0,0.0,0.0,1.0]]
    else:
        pixdim = struct.unpack(endian+'8f', raw[76:108])
        affine = [[pixdim[1],0,0,0],[0,pixdim[2],0,0],[0,0,pixdim[3],0],[0,0,0,1]]
    if datatype not in DTYPES:
        raise RuntimeError(f'Unsupported datatype {datatype}: {path}')
    code, size = DTYPES[datatype]
    n = math.prod(dims)
    arr = array(code)
    arr.frombytes(raw[vox_offset:vox_offset+n*size])
    if (endian == '>' and sys.byteorder == 'little') or (endian == '<' and sys.byteorder == 'big'):
        arr.byteswap()
    return {'dims':dims, 'datatype':datatype, 'data':arr, 'slope':slope, 'inter':inter, 'affine':affine}

def inv3(m):
    a,b,c=m[0]; d,e,f=m[1]; g,h,i=m[2]
    det=a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
    if abs(det) < 1e-12:
        raise RuntimeError('Singular affine')
    return [
        [(e*i-f*h)/det,(c*h-b*i)/det,(b*f-c*e)/det],
        [(f*g-d*i)/det,(a*i-c*g)/det,(c*d-a*f)/det],
        [(d*h-e*g)/det,(b*g-a*h)/det,(a*e-b*d)/det],
    ]

def world_to_vox_inv(aff):
    M=[row[:3] for row in aff[:3]]
    t=[aff[r][3] for r in range(3)]
    return inv3(M),t

def apply_aff(aff,x,y,z):
    return [aff[0][0]*x+aff[0][1]*y+aff[0][2]*z+aff[0][3],
            aff[1][0]*x+aff[1][1]*y+aff[1][2]*z+aff[1][3],
            aff[2][0]*x+aff[2][1]*y+aff[2][2]*z+aff[2][3]]

def world_to_vox(Mi,t,w):
    q=[w[j]-t[j] for j in range(3)]
    return [Mi[r][0]*q[0]+Mi[r][1]*q[1]+Mi[r][2]*q[2] for r in range(3)]

brain=load_nii(brain_path)
tissue=load_nii(tissue_path)
atlas=load_nii(atlas_path)
if brain['dims'][:3] != tissue['dims'][:3]:
    raise RuntimeError('Brain/tissue dimensions do not match')

nx,ny,nz=brain['dims'][:3]
vals=[float(v)*brain['slope']+brain['inter'] for v in brain['data'] if float(v)>0]
vals.sort()
lo=vals[max(0,int(len(vals)*0.002))]
hi=vals[min(len(vals)-1,int(len(vals)*0.998))]
if hi <= lo:
    hi=lo+1

outb=array('H')
for v in brain['data']:
    fv=float(v)*brain['slope']+brain['inter']
    if fv <= 0:
        q=0
    else:
        q=round((fv-lo)/(hi-lo)*65535)
        q=max(0,min(65535,q))
    outb.append(q)
if sys.byteorder != 'little':
    outb.byteswap()
(data_dir/'brain_u16.bin').write_bytes(outb.tobytes())

outt=bytes(max(0,min(255,int(round(float(v)*tissue['slope']+tissue['inter'])))) for v in tissue['data'])
(data_dir/'tissue_u8.bin').write_bytes(outt)

ax,ay,az=atlas['dims'][:3]
Mi,tvec=world_to_vox_inv(atlas['affine'])
outa=bytearray(nx*ny*nz)
adata=atlas['data']
for z in range(nz):
    for y in range(ny):
        base=nx*(y+ny*z)
        for x in range(nx):
            w=apply_aff(brain['affine'],x,y,z)
            av=world_to_vox(Mi,tvec,w)
            xa,ya,za=(int(round(av[0])),int(round(av[1])),int(round(av[2])))
            if 0<=xa<ax and 0<=ya<ay and 0<=za<az:
                val=int(adata[xa+ax*(ya+ay*za)])
                if 0<=val<=255:
                    outa[base+x]=val
(data_dir/'aal_u8.bin').write_bytes(outa)

lut=json.loads(json_path.read_text())
meta={
    'dims':[nx,ny,nz],
    'affine':brain['affine'],
    'labels':lut.get('labels',[]),
    'R':lut.get('R',[]),
    'G':lut.get('G',[]),
    'B':lut.get('B',[]),
    'brainWindow':{'low':lo,'high':hi},
    'source':{
        'brain':'MNI152_T1_2mm_Brain',
        'tissue':'MNI152 FAST segmentation',
        'atlas':'AAL resampled nearest-neighbor to 2 mm grid'
    }
}
(data_dir/'meta.json').write_text(json.dumps(meta,separators=(',',':')))

n=nx*ny*nz
assert (data_dir/'brain_u16.bin').stat().st_size == n*2
assert (data_dir/'tissue_u8.bin').stat().st_size == n
assert (data_dir/'aal_u8.bin').stat().st_size == n
print('Prepared',n,'voxels; atlas labels present:',len(set(outa))-1)
