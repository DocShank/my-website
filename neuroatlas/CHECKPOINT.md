# NeuroAtlas checkpoint

Current stable implementation checkpoint after repeated chat streaming interruptions.

## Protected visual baseline
Do not redesign or replace the working NeuroAtlas interface. Preserve the current 4-view, axial, coronal, sagittal, 3D, cursor interaction, opacity controls, loading behavior, and overall visual presentation unless explicitly requested.

## Current implementation state
Precision v3 was deployed from commit `52f2124407f1bba9a44165286f93563650c65bec`.

The precision v3 work includes:
- FIND/search landing points taken from actual voxels inside atlas labels rather than mathematical centroids.
- JHU ICBM-DTI-81 white-matter labels for detailed structures such as internal capsule, corona radiata, external capsule, callosal regions, and major tracts.
- Harvard-Oxford subcortical labels for lateral ventricles, brainstem, and major deep structures.
- Third and fourth ventricle recognition near the cursor.
- Nearest meaningful atlas-label fallback when the exact cursor voxel is unlabeled.
- Teaching opacity target around 45 percent rather than forcing 100 percent.
- Sharper outlined-region presentation.
- Finer brainstem teaching levels: rostral midbrain, caudal midbrain, rostral pons, caudal pons, rostral medulla, caudal medulla.
- Expanded brainstem cross-sectional teaching descriptions.

## User-reported requirements that define acceptance
1. Searching `internal capsule` must move the crosshair into a real internal-capsule label, not a random central location.
2. Ventricles and CSF spaces must be clearly identified, including lateral ventricles and useful third/fourth-ventricle recognition.
3. Manual cursor identification must remain accurate and should fall back to the nearest meaningful structure rather than only reporting that no atlas boundary exists.
4. Structure outlines and color delineation should be sharp but must not significantly degrade performance.
5. Teaching opacity should normally be around 40 to 50 percent when a structure is selected so MRI anatomy remains visible underneath.
6. Midbrain, pons, and medulla cross sections need level-specific identification and teaching detail.
7. Preserve the current interaction, mobility, 3D behavior, loading behavior, and visual layout.
8. Do not use long dash characters in user-facing descriptions.

## Next test pass
On iPhone Safari, test:
- `internal capsule`
- `anterior limb of internal capsule`
- `posterior limb of internal capsule`
- `left lateral ventricle`
- `right lateral ventricle`
- cursor placement in third ventricle and fourth ventricle regions
- sagittal cortical points that previously returned no valid atlas boundary
- rostral/caudal midbrain, pons, and medulla locations
- atlas opacity around 45 percent

If a chat stream is interrupted again, resume from this file and the latest GitHub commit rather than reconstructing the state from memory.
