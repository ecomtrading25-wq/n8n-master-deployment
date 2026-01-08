# IMPLEMENTATION_ORDER (Days 1–23)

This is a practical deployment sequence for the workflows and stack contained in this package.

## Phase 0 — Prereqs (Days 1–2)
Day 1
- Install Docker Desktop (Windows) and enable WSL2
- Confirm ports available: 5678 (n8n), 5433 (Postgres mapped), 9000/9001 (MinIO)
- Install Python 3.10+ (optional, for helper scripts)

Day 2
- Ensure ComfyUI is running locally (Windows host) on `http://127.0.0.1:8188`
- Confirm Docker can reach host: `http://host.docker.internal:8188`

## Phase 1 — Foundation (Days 3–5)
Day 3
- Copy env:
  - `02_ENV/.env.example` → `01_DOCKER/.env`
- Set `N8N_ENCRYPTION_KEY` and DB creds
- Start stack:
  ```bash
  cd 01_DOCKER
  docker compose up -d
  ```
- Verify:
  - n8n UI loads: `http://localhost:5678`
  - Postgres reachable (container healthy)

Day 4
- Create Postgres tables for AI Business OS:
  - Open `04_SCHEMAS/AI_Business_OS_schema.sql`
  - Apply to Postgres (psql or a DB tool)
- Verify tables exist: `events`, `tasks`, `policies`, `approvals`, etc.

Day 5
- Configure n8n user + security basics (admin user, encryption key set, backups)
- Confirm volume persistence under `01_DOCKER/data/`

## Phase 2 — Workflows import + wiring (Days 6–10)
Day 6
- Import all workflows in `03_WORKFLOWS/AI_BUSINESS_OS_KERNEL/`

Day 7
- Import all workflows in `03_WORKFLOWS/LSN_CONTENT_FACTORY/`

Day 8
- Create credentials in n8n:
  - Postgres credential and assign to all Postgres nodes
  - MinIO S3 credential and assign in WF08

Day 9
- Populate workflow ID env vars in `01_DOCKER/.env`
- Restart:
  ```bash
  cd 01_DOCKER
  docker compose restart n8n
  ```

Day 10
- Smoke tests:
  - Run WF08 upload → confirm public URL
  - Trigger AI-OS 01 Event Ingest webhook → ensure event row inserted

## Phase 3 — Integrations (Days 11–15)
Day 11
- Fill HeyGen / ElevenLabs / Kling keys in `.env` (only what you use)
- Re-test WF09 (voice) and WF11 (HeyGen end-to-end)

Day 12
- Configure MinIO public URL strategy:
  - local dev: `PUBLIC_ASSET_BASE_URL=http://localhost:9000/lsn-assets`
  - prod: put MinIO behind a domain/CDN and set `PUBLIC_ASSET_BASE_URL=https://assets.yourdomain.com/lsn-assets`
  See: `00_DOCS/MINIO_PUBLIC_URL_STRATEGY.md`

Day 13–15
- Turn on additional workflows (activate cron/dispatcher only after you’re confident)
- Add Slack creds if you want approval + incident notifications

## Phase 4 — Integration testing (Days 16–18)
Day 16
- Run end-to-end job via LSN webhook:
  - `POST /webhook/lsn/job` with an example payload
Day 17
- Validate output artifacts on disk (`LSN_OUTPUT_DIR`) and in MinIO bucket
Day 18
- Failure tests: invalid API keys, missing files, retry behavior

## Phase 5 — Production hardening (Days 19–21)
Day 19
- Backups: Postgres dumps + n8n data volume backups
Day 20
- Lock down access: reverse proxy, basic auth/VPN, HTTPS, IP allowlists
Day 21
- Monitoring: container health checks, workflow error alerts

## Phase 6 — Go live (Days 22–23)
Day 22
- Move WEBHOOK_URL + N8N_HOST to production domain
- Update PUBLIC_ASSET_BASE_URL to production CDN
Day 23
- Enable cron dispatchers
- Start live job intake + measure success rate
