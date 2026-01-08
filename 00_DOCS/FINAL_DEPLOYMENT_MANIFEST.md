# FINAL_DEPLOYMENT_MANIFEST

Generated: 2026-01-08 (Australia/Melbourne)

This is the consolidated **n8n deployment package** created from the three uploaded archives:

- `LSN_N8N_FULL_WORKFLOWS_AND_CODE.zip`
- `LSN_N8N_CONTINUE_PACK.zip`
- `AI_Business_OS_n8n_pack_v1 (1).zip`

## What’s included
- Docker Compose stack for **n8n + Postgres + Redis + MinIO**
- **22 n8n workflows** (JSON) across:
  - LSN Content Factory (WF00–WF12 + WF20)
  - AI Business OS Kernel (01–09)
- Postgres schema for AI Business OS
- Job contracts + example jobs + job manifest example
- Helper code (caption + packager scripts)
- Documentation for import, credentials, and deployment order

## Directory map
- `00_DOCS/` – all documentation (start here)
- `01_DOCKER/` – docker-compose stack
- `02_ENV/` – env templates
- `03_WORKFLOWS/` – importable workflows
- `04_SCHEMAS/` – Postgres + job schema files
- `05_CODE_HELPERS/` – optional python helpers
- `06_EXAMPLES/` – sample payloads and manifests
