#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
text = path.read_text()

creator = "Created by Dr. Shashank Neupane and Team"
if text.count(creator) != 2:
    raise SystemExit(f"Expected two creator strings, found {text.count(creator)}")
text = text.replace(creator, "Created by Dr. Shashank Neupane · Precision v7.1")

watermark_creator = "Dr. Shashank Neupane and Team"
if text.count(watermark_creator) != 1:
    raise SystemExit(
        f"Expected one watermark creator string, found {text.count(watermark_creator)}"
    )
text = text.replace(watermark_creator, "Dr. Shashank Neupane", 1)

replacements = {
    "NeuroAtlas MRI <sup>TM</sup>": "NeuroAtlas MRI",
    "real MRI · registered anatomy · learning-first":
        "standardized MNI152 template · registered atlases · learning-first",
    "Loading real MRI volume and registered atlas…":
        "Loading standardized MNI152 template and registered atlases...",
    "Move through authentic MRI-derived anatomy. The colored atlas is a separate registered layer, so you can fade it away and learn the grayscale MRI itself.":
        "Move through a standardized MNI152 T1 template with separate registered atlas layers. Fade the labels to review the grayscale template on its own.",
    "<dialog id=\"dlg\"><h3>Data & provenance</h3><p>This development build displays the MNI152 demonstration T1 MRI volume with a registered AAL regional label volume. A second, invisible JHU ICBM-DTI-81 white-matter label atlas is loaded after the core viewer so white-matter structures can be identified without changing the appearance or delaying the working MRI interface.</p><p>MRI intensity and anatomical labels remain separate layers. The JHU layer is used for educational identification only in this prototype; redistribution and production licensing will be reviewed before any wider release.</p><button id=\"close\">Close</button></dialog>":
        "<dialog id=\"dlg\"><h3>Data and provenance</h3><p>NeuroAtlas MRI Precision v7.1 is a non-commercial educational prototype. It displays a downsampled MNI152 T1 template with separate AAL regional, JHU ICBM-DTI-81 white-matter, and Harvard-Oxford subcortical atlas layers. It contains no patient data and is not a diagnostic system.</p><p>Atlas labels are standardized educational references, not patient-specific segmentations. A nearby-label result is reported with its distance and is not direct voxel membership.</p><p><a href=\"../THIRD_PARTY_NOTICES.md\" target=\"_blank\" rel=\"noopener\">Sources, citations, checksums, and license notices</a></p><button id=\"close\">Close</button></dialog>",
    "await nv.loadVolumes([{url:'https://niivue.com/demos/images/mni152.nii.gz'},{url:'https://niivue.com/demos/images/aal.nii.gz',opacity:.18}]);let map=await fetch('https://niivue.com/demos/images/aal.json').then(r=>r.json());":
        "await nv.loadVolumes([{url:'./data/mni152.nii.gz'},{url:'./data/aal.nii.gz',opacity:.18}]);let map=await fetch('./data/aal.json').then(r=>r.json());",
}

for old, new in replacements.items():
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one occurrence, found {count}: {old[:90]}")
    text = text.replace(old, new, 1)

path.write_text(text)
