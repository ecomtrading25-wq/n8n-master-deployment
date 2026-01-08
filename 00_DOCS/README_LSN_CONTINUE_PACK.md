# LSN n8n — Continue Pack (Next Big Chunk)
Generated: 2026-01-07

Adds end-to-end plumbing:
- Upload assets to **MinIO** so you get stable **public URLs**
- End-to-end flows for **HeyGen** + **Kling** that auto-create required public URLs
- Batch runner for **JOB_MANIFEST.json**

## Workflows
- WF08_UPLOAD_FILE_TO_MINIO
- WF09_VOICE_TTS_AND_UPLOAD
- WF10_COMFYUI_RENDER_AND_UPLOAD
- WF11_HEYGEN_TALKING_END2END
- WF12_KLING_I2V_END2END
- WF20_RUN_JOB_MANIFEST

## Env vars to add
MINIO_BUCKET=lsn-assets
PUBLIC_ASSET_BASE_URL=https://assets.yourdomain.com/lsn-assets
WF_UPLOAD_ID=...
WF_VOICE_UPLOAD_ID=...
WF_RENDER_UPLOAD_ID=...

See `N8N_WORKFLOWS/WORKFLOW_ID_MAPPING_CONTINUE.md`.
