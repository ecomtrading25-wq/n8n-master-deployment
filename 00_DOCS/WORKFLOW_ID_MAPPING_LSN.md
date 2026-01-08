# Workflow ID Mapping
WF00 orchestrator calls sub-workflows via env vars:

- WF_TALKING_ID  -> WF03_HEYGEN_TALKING
- WF_VOICE_ID    -> WF02_ELEVENLABS_VOICE
- WF_CINEMATIC_ID-> WF04_KLING_IMAGE2VIDEO or your Veo workflow
- WF_LISTING_ID  -> WF01_COMFYUI_LISTING

After importing, copy each workflow's internal id into your `.env` and restart.
