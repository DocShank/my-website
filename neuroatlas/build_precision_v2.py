from pathlib import Path
import base64, zlib, sys

root = Path(__file__).resolve().parent
payload = ''.join((root / f'v2_payload_{i}.txt').read_text().strip() for i in range(1, 5))
out = Path(sys.argv[1] if len(sys.argv) > 1 else 'site/neuroatlas/index.html')
out.write_bytes(zlib.decompress(base64.b64decode(payload)))
print('wrote', out, out.stat().st_size, 'bytes')
