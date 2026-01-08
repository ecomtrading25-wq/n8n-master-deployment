# Workflow ID Mapping (unified)

Several workflows call other workflows using **Execute Workflow** nodes. n8n assigns a numeric/string **workflow ID** on import.
Put these IDs into your `.env` and restart n8n.

## LSN Content Factory
- `WF_LISTING_ID`  -> `WF01_COMFYUI_LISTING`
- `WF_VOICE_ID`    -> `WF02_ELEVENLABS_VOICE`
- `WF_TALKING_ID`  -> `WF03_HEYGEN_TALKING`
- `WF_KLING_ID`    -> `WF04_KLING_IMAGE2VIDEO`
- `WF_CINEMATIC_ID`-> `WF04_KLING_IMAGE2VIDEO` (or your future VEO workflow)
- `WF_UPLOAD_ID`         -> `WF08_UPLOAD_FILE_TO_MINIO`
- `WF_VOICE_UPLOAD_ID`   -> `WF09_VOICE_TTS_AND_UPLOAD`
- `WF_RENDER_UPLOAD_ID`  -> `WF10_COMFYUI_RENDER_AND_UPLOAD`

## AI Business OS Kernel
- `AIOS_WF_POLICY_GATE_ID`        -> `AI-OS 03 - Policy Gate (Sub-workflow)`
- `AIOS_WF_APPROVAL_REQUEST_ID`   -> `AI-OS 04 - Approval Request (Sub-workflow)`
- `AIOS_WF_CONTENT_FACTORY_ID`    -> `AI-OS 06 - Content Factory (Sub-workflow)`
- `AIOS_WF_FINANCE_GATE_ID`       -> `AI-OS 07 - Finance Gate (Sub-workflow)`
- `AIOS_WF_KILL_SWITCH_ID`        -> `AI-OS 08 - Kill Switch (Sub-workflow)`
