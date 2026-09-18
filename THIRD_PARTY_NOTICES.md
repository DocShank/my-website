# NeuroAtlas MRI third-party notices

NeuroAtlas MRI is a non-commercial educational prototype. It is not a
diagnostic system and does not display patient data. The original application
code is released under the repository's BSD 2-Clause License. The resources
below remain the property of their respective creators and retain their own
licenses and attribution requirements.

## NiiVue 0.62.1

- Use: Browser-based NIfTI loading, multiplanar visualization, and 3D rendering.
- Package: `@niivue/niivue@0.62.1`, loaded from jsDelivr with the version pinned.
- Project: https://github.com/niivue/niivue
- License: BSD 2-Clause License.
- Copyright notice: Copyright (c) 2021, Niivue. All rights reserved.
- Citation: Eckstein K, Androulakis A, Dao TT, et al. Seamless neuroimaging
  visualization: the NiiVue wrapper ecosystem. Aperture Neuro. 2026;6.
  https://doi.org/10.52294/001c.167815

## MNI152 demonstration T1 volume

- Deployed file: `neuroatlas/data/mni152.nii.gz`
- Use: Standard-space T1 background template.
- Exact source: `mni152.nii.gz` from `niivue/niivue-demo-images`, commit
  `f6f98294c1fa89a3a32e8a44eab92368374150a0`.
- Source URL: https://github.com/niivue/niivue-demo-images
- SHA-256: `dbbd4542823c1e2b12265c9b7e3cf959ee02ff7829bbf05cdcfbecc0013a00fa`
- Provenance stated by the source repository: derived from the ICBM 152
  Nonlinear Atlases version 2009; the demonstration image is downsampled for
  browser use.
- Source-repository license: BSD 2-Clause License, copyright (c) 2022,
  Chris Rorden.
- Original MNI notice: Copyright (C) 1993-2004 Louis Collins, McConnell Brain
  Imaging Centre, Montreal Neurological Institute, McGill University.
  Permission to use, copy, modify, and distribute the software and its
  documentation for any purpose and without fee is granted provided that the
  copyright notice appears in all copies. The resource is provided as-is.
- Original atlas page and full notice:
  https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009

## Automated Anatomical Labeling resource

- Deployed files: `neuroatlas/data/aal.nii.gz` and
  `neuroatlas/data/aal.json`.
- Use: Regional anatomical labels and the associated label-color table.
- Exact source: NiiVue demonstration files from `niivue/niivue`, commit
  `ee9aefce6ce006a8b1a466434cc0d7ba2ac58344`.
- Source URLs:
  - https://github.com/niivue/niivue/blob/ee9aefce6ce006a8b1a466434cc0d7ba2ac58344/packages/niivue/demos/images/aal.nii.gz
  - https://github.com/niivue/niivue/blob/ee9aefce6ce006a8b1a466434cc0d7ba2ac58344/packages/niivue/demos/images/aal.json
- SHA-256, NIfTI: `af9fcba49420955020e61c72cf28ab89e12662e2ce64659456c10592ad88f834`
- SHA-256, JSON: `d22783485b5f8054c77e03c44b48048d29bcc2633648dcdb2a14377b60e92c24`
- Source-repository license: BSD 2-Clause License, copyright (c) 2021, Niivue.
- Scientific attribution: Tzourio-Mazoyer N, Landeau B, Papathanassiou D, et
  al. Automated anatomical labeling of activations in SPM using a macroscopic
  anatomical parcellation of the MNI MRI single-subject brain. Neuroimage.
  2002;15:273-289. https://doi.org/10.1006/nimg.2001.0978
- AAL project: https://www.gin.cnrs.fr/en/tools/aal/

## JHU ICBM-DTI-81 white-matter labels

- Deployed file: `neuroatlas/data/JHU-ICBM-labels-1mm.nii.gz`
- Use: White-matter label identification and cross-section annotation.
- Exact source: `MASILab/PreQual`, commit
  `09c64b495284cc7145617d31650a7819f71bd0a1`.
- Source URL: https://github.com/MASILab/PreQual/blob/09c64b495284cc7145617d31650a7819f71bd0a1/src/SUPPLEMENTAL/JHU-ICBM-labels-1mm.nii.gz
- SHA-256: `fac584ec75ff2a8631710d3345df96733ed87d9bde3387f5b462f8d22914ed69`
- License: At the atlas owners' request, the JHU atlases are distributed under
  the main FSL license. That license permits non-commercial reproduction,
  transmission, and transfer when its conditions are passed to the receiver;
  commercial use requires separate permission.
- Full license and coordinator contact:
  https://fsl.fmrib.ox.ac.uk/fsl/docs/license.html
- Citation: Mori S, Oishi K, Jiang H, et al. Stereotaxic white matter atlas
  based on diffusion tensor imaging in an ICBM template. Neuroimage.
  2008;40:570-582. https://doi.org/10.1016/j.neuroimage.2007.12.035

## Harvard-Oxford subcortical structural atlas

- Deployed file:
  `neuroatlas/data/HarvardOxford-sub-maxprob-thr25-2mm.nii.gz`
- Use: Selected deep gray-matter, lateral ventricular, and brainstem labels.
- File type: 2 mm maximum-probability summary image thresholded at 25%.
- Exact source: FSL `data_atlases` release `2103.0`.
- Source URL: https://git.fmrib.ox.ac.uk/fsl/data_atlases/-/blob/2103.0/HarvardOxford/HarvardOxford-sub-maxprob-thr25-2mm.nii.gz
- SHA-256: `72140df8117250d915b753ca2937e078c917525d206e6185e2c1b4ab703fbfcc`
- Modification statement: The NIfTI file is redistributed unmodified. The
  NeuroAtlas interface uses its integer label values for display and teaching
  annotations; it does not alter the atlas file.
- License: Creative Commons Attribution-ShareAlike 4.0 International,
  https://creativecommons.org/licenses/by-sa/4.0/
- Official FSL atlas documentation:
  https://fsl.fmrib.ox.ac.uk/fsl/docs/other/datasets.html
- Official FSL licensing page:
  https://fsl.fmrib.ox.ac.uk/fsl/docs/license.html

## Scope and no-endorsement statement

The inclusion of these resources does not imply endorsement of NeuroAtlas MRI
by NiiVue, McGill University, the Montreal Neurological Institute, the AAL
authors, Johns Hopkins University, FSL, Oxford University, or the
Harvard-Oxford atlas contributors. Atlas labels are standardized educational
references and are not patient-specific segmentations.
