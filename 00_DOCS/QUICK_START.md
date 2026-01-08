# QUICK_START (5–10 minutes)

## 1) Start the stack
1. Open `02_ENV/.env.example` and copy it to `01_DOCKER/.env` (same folder as `docker-compose.yml`)
2. Fill at least:
   - `POSTGRES_PASSWORD`
   - `N8N_ENCRYPTION_KEY` (32+ chars)
   - Any API keys you plan to use (HeyGen / ElevenLabs / Kling / etc.)
3. Run:
   ```bash
   cd 01_DOCKER
   docker compose up -d
   ```
4. Open n8n: `http://localhost:5678`

## 2) Import workflows
Import everything under:
- `03_WORKFLOWS/LSN_CONTENT_FACTORY/`
- `03_WORKFLOWS/AI_BUSINESS_OS_KERNEL/`

**Import order suggestion**
1) All sub-workflows first (WF01..WF12, AI-OS 03..08)
2) Then orchestrators/dispatchers (WF00, AI-OS 02)
3) Then webhooks (WF00 + AI-OS 01 + AI-OS 05)

## 3) Wire credentials (1-time)
In n8n, create and assign:
- **Postgres** credential (host `postgres`, port `5432`) → assign to Postgres nodes
- **MinIO S3** credential (AWS S3 node) → assign in `WF08_UPLOAD_FILE_TO_MINIO`

See: `00_DOCS/CREDENTIALS_MATRIX.md`.

## 4) Set workflow IDs in env
After import, each workflow has an internal **ID**.
Add them into `.env` (then restart docker compose) for:
- `WF_LISTING_ID`, `WF_VOICE_ID`, `WF_TALKING_ID`, `WF_KLING_ID`, `WF_UPLOAD_ID`, ...
- `AIOS_WF_POLICY_GATE_ID`, `AIOS_WF_CONTENT_FACTORY_ID`, ...

References:
- `00_DOCS/WORKFLOW_ID_MAPPING.md`
- `00_DOCS/WORKFLOWS_INDEX.md`

## 5) Smoke test
- Run `WF08_UPLOAD_FILE_TO_MINIO` manually (upload a small local file) and confirm you get a public URL.
- Trigger `WF00_ORCHESTRATOR` by posting a job to its webhook (see below).

### Post a job (LSN)
`POST http://localhost:5678/webhook/lsn/job`

Body examples: `06_EXAMPLES/LSN_example_jobs.json` and schema in `04_SCHEMAS/LSN_Job.json`.
