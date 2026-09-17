from pathlib import Path
import array, gzip, json, math, struct, sys

TYPECODES = {
    2: ('B', 1),
    4: ('h', 2),
    8: ('i', 4),
    16: ('f', 4),
    64: ('d', 8),
    256: ('b', 1),
    512: ('H', 2),
    768: ('I', 4),
}

def read_bytes(path):
    p = Path(path)
    if p.suffix == '.gz':
        with gzip.open(p, 'rb') as f:
            return f.read()
    return p.read_bytes()

def qform_affine(buf, endian, pixdim):
    b, c, d = struct.unpack(endian + '3f', buf[256:268])
    qx, qy, qz = struct.unpack(endian + '3f', buf[268:280])
    a2 = max(0.0, 1.0 - (b*b + c*c + d*d))
    a = math.sqrt(a2)
    qfac = -1.0 if pixdim[0] < 0 else 1.0
    dx, dy, dz = pixdim[1], pixdim[2], pixdim[3] * qfac
    r11 = a*a + b*b - c*c - d*d
    r12 = 2*(b*c - a*d)
    r13 = 2*(b*d + a*c)
    r21 = 2*(b*c + a*d)
    r22 = a*a + c*c - b*b - d*d
    r23 = 2*(c*d - a*b)
    r31 = 2*(b*d - a*c)
    r32 = 2*(c*d + a*b)
    r33 = a*a + d*d - c*c - b*b
    return [
        [r11*dx, r12*dy, r13*dz, qx],
        [r21*dx, r22*dy, r23*dz, qy],
        [r31*dx, r32*dy, r33*dz, qz],
        [0.0, 0.0, 0.0, 1.0],
    ]

def read_nifti(path):
    buf = read_bytes(path)
    if len(buf) < 352:
        raise ValueError(f'{path}: not a NIfTI-1 file')
    if struct.unpack('<i', buf[:4])[0] == 348:
        endian = '<'
    elif struct.unpack('>i', buf[:4])[0] == 348:
        endian = '>'
    else:
        raise ValueError(f'{path}: unsupported NIfTI header')
    dims = struct.unpack(endian + '8h', buf[40:56])
    datatype = struct.unpack(endian + 'h', buf[70:72])[0]
    pixdim = struct.unpack(endian + '8f', buf[76:108])
    vox_offset = int(round(struct.unpack(endian + 'f', buf[108:112])[0]))
    qform_code = struct.unpack(endian + 'h', buf[252:254])[0]
    sform_code = struct.unpack(endian + 'h', buf[254:256])[0]
    if datatype not in TYPECODES:
        raise ValueError(f'{path}: unsupported datatype {datatype}')
    nx, ny, nz = int(dims[1]), int(dims[2]), int(dims[3])
    nvox = nx * ny * nz
    typecode, itemsize = TYPECODES[datatype]
    raw = buf[vox_offset:vox_offset + nvox * itemsize]
    if len(raw) < nvox * itemsize:
        raise ValueError(f'{path}: truncated voxel data')
    vals = array.array(typecode)
    vals.frombytes(raw)
    host_little = sys.byteorder == 'little'
    file_little = endian == '<'
    if itemsize > 1 and host_little != file_little:
        vals.byteswap()
    if sform_code > 0:
        sx = struct.unpack(endian + '4f', buf[280:296])
        sy = struct.unpack(endian + '4f', buf[296:312])
        sz = struct.unpack(endian + '4f', buf[312:328])
        affine = [list(sx), list(sy), list(sz), [0.0, 0.0, 0.0, 1.0]]
    elif qform_code > 0:
        affine = qform_affine(buf, endian, pixdim)
    else:
        affine = [
            [pixdim[1], 0.0, 0.0, 0.0],
            [0.0, pixdim[2], 0.0, 0.0],
            [0.0, 0.0, pixdim[3], 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    return vals, (nx, ny, nz), affine

def voxel_to_mm(v, affine):
    x, y, z = v
    return [
        affine[0][0]*x + affine[0][1]*y + affine[0][2]*z + affine[0][3],
        affine[1][0]*x + affine[1][1]*y + affine[1][2]*z + affine[1][3],
        affine[2][0]*x + affine[2][1]*y + affine[2][2]*z + affine[2][3],
    ]

def representative_points(path):
    vals, (nx, ny, nz), affine = read_nifti(path)
    plane = nx * ny

    # First pass: geometric center of each label in voxel space.
    acc = {}
    for idx, rawv in enumerate(vals):
        lab = int(round(float(rawv)))
        if lab <= 0:
            continue
        z = idx // plane
        rem = idx - z * plane
        y = rem // nx
        x = rem - y * nx
        row = acc.get(lab)
        if row is None:
            acc[lab] = [1, float(x), float(y), float(z)]
        else:
            row[0] += 1
            row[1] += x
            row[2] += y
            row[3] += z

    centers = {lab: (sx/n, sy/n, sz/n) for lab, (n, sx, sy, sz) in acc.items()}

    # Second pass: choose the real label voxel closest to that center.
    # This guarantees FIND never jumps to a mathematical centroid outside
    # an irregular or crescent-shaped anatomical region.
    best = {lab: [float('inf'), None] for lab in centers}
    for idx, rawv in enumerate(vals):
        lab = int(round(float(rawv)))
        if lab <= 0 or lab not in centers:
            continue
        z = idx // plane
        rem = idx - z * plane
        y = rem // nx
        x = rem - y * nx
        cx, cy, cz = centers[lab]
        d = (x-cx)**2 + (y-cy)**2 + (z-cz)**2
        if d < best[lab][0]:
            best[lab] = [d, (x, y, z)]

    out = {}
    for lab, (_, voxel) in best.items():
        if voxel is None:
            continue
        mm = voxel_to_mm(voxel, affine)
        out[str(lab)] = [round(float(v), 3) for v in mm]
    return out

def main():
    if len(sys.argv) != 5:
        raise SystemExit('usage: build_atlas_centroids.py AAL.nii[.gz] JHU.nii[.gz] HO.nii[.gz] output.json')
    aal, jhu, ho, out = sys.argv[1:]
    data = {
        'AAL': representative_points(aal),
        'JHU': representative_points(jhu),
        'HO': representative_points(ho),
    }
    Path(out).write_text(json.dumps(data, separators=(',', ':')))
    print('representative labels:', {k: len(v) for k, v in data.items()})

if __name__ == '__main__':
    main()
