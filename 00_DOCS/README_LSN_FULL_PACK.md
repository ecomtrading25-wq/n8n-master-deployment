# LSN n8n — Full Workflows + Code Pack
Generated: 2026-01-07

This pack includes:
- Importable **n8n workflows** (JSON) for your Avatar + Content Factory pipeline
- A **Windows-friendly Docker Compose** stack (n8n + Postgres + Redis + MinIO)
- A **Job JSON contract** (schema)
- Optional helper scripts for captions/packaging

## Windows note (ComfyUI local)
If n8n runs in Docker, it must reach your Windows host via:
- `http://host.docker.internal:8188`

## Start
1) Copy `.env.example` → `.env` and fill keys
2) `cd DOCKER && docker compose up -d`
3) Open `http://localhost:5678`
4) Import workflows from `N8N_WORKFLOWS/`

## Post a job
`POST http://localhost:5678/webhook/lsn/job`
Body must match `JOB_SCHEMA/Job.json`.
