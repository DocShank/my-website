# NeuroAtlas checkpoint

Current stable implementation checkpoint after repeated chat streaming interruptions.

## Protected visual baseline
Do not redesign or replace the working NeuroAtlas interface. Preserve the current 4-view, axial, coronal, sagittal, 3D, cursor interaction, opacity controls, loading behavior, and overall visual presentation unless explicitly requested.

## Current implementation state
Precision v4 is the active implementation target, built on the protected Precision v3 release.

Precision v4 keeps the viewer unchanged and adds:
- FIND/search landing points from actual atlas voxels inside each requested label.
- JHU ICBM-DTI-81 white-matter labels for internal capsule, corona radiata, external capsule, callosal regions, and major tracts.
- Harvard-Oxford labels for lateral ventricles, brainstem, and major deep structures.
- Third and fourth ventricle landmark recognition before adjacent AAL or brainstem labels can override it.
- Nearest-label fallback chosen by real physical distance across AAL, Harvard-Oxford, and JHU atlases.
- A displayed distance for fallback labels so nearby labels are not presented as exact voxel matches.
- Teaching opacity around 45 percent for searched structures.
- Sharp color boundaries using the NiiVue opaque-boundary mode while preserving translucent structure fill.
- Finer brainstem teaching levels: rostral and caudal midbrain, pons, and medulla.
- Search aliases for upper/lower midbrain, upper/lower pons, open/closed medulla, and upper/lower medulla.
- No long dash characters in user-facing descriptions.

## User-reported requirements that define acceptance
1. Searching `internal capsule` must move the crosshair into a real internal-capsule label, not a random central location.
2. Ventricles and CSF spaces must be clearly identified, including lateral ventricles and useful third/fourth-ventricle recognition.
3. Manual cursor identification must remain accurate and should fall back to the nearest meaningful structure rather than only reporting that no atlas boundary exists.
4. Structure outlines and color delineation should be sharp but must not significantly degrade performance.
5. Teaching opacity should normally be around 40 to 50 percent when a structure is selected so MRI anatomy remains visible underneath.
6. Midbrain, pons, and medulla cross sections need level-specific identification and teaching detail.
7. Preserve the current interaction, mobility, 3D behavior, loading behavior, and visual layout.
8. Do not use long dash characters in user-facing descriptions.

## Test pass after Precision v4 deploys
On iPhone Safari, test:
- `internal capsule`
- `anterior limb of internal capsule`
- `posterior limb of internal capsule`
- `left lateral ventricle`
- `right lateral ventricle`
- `third ventricle`
- `fourth ventricle`
- sagittal cortical points that previously returned no valid atlas boundary
- `rostral midbrain`, `caudal midbrain`
- `rostral pons`, `caudal pons`
- `open medulla`, `closed medulla`
- atlas opacity around 45 percent
- Sharp color boundaries mode

If a chat stream is interrupted again, resume from this file and the latest GitHub commit rather than reconstructing the state from memory.
