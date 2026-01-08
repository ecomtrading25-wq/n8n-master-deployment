# N8N Deployment Checklist

## Pre-Deployment
- [ ] Docker and Docker Compose installed
- [ ] Ports available: 5678, 5433, 6380, 9000, 9001
- [ ] 10GB+ free disk space
- [ ] Git cloned or extracted package

## Phase 1: Infrastructure (5 min)
- [ ] Copy `.env.example` to `.env` in `01_DOCKER/`
- [ ] Update `.env` with secure passwords
- [ ] Run `docker compose up -d`
- [ ] Wait for all containers healthy: `docker compose ps`
- [ ] Verify n8n accessible: http://localhost:5678

## Phase 2: Database (2 min)
- [ ] Connect to Postgres: `docker exec -it <postgres_container> psql -U lsn -d lsn`
- [ ] Run SQL from `04_SCHEMAS/AI_Business_OS_schema.sql`
- [ ] Verify tables created: `\dt`
- [ ] Exit: `\q`

## Phase 3: Workflow Import (10 min)
Choose one method:

### Option A: Manual UI Import
- [ ] Open http://localhost:5678
- [ ] Go to Workflows → Import
- [ ] Import all 22 JSON files from `03_WORKFLOWS/`
- [ ] Import order: sub-workflows first, then orchestrators

### Option B: Automated API Import
- [ ] Get n8n API key from settings
- [ ] Run: `N8N_API_KEY=<key> python3 import_workflows.py`
- [ ] Verify all 22 imported successfully

## Phase 4: Credentials (5 min)
In n8n UI → Credentials:

### Postgres
- [ ] Name: "LSN Postgres"
- [ ] Host: `postgres`
- [ ] Port: `5432`
- [ ] Database: `lsn`
- [ ] User: `lsn`
- [ ] Password: (from .env)
- [ ] Assign to: All Postgres nodes

### MinIO S3
- [ ] Name: "MinIO S3"
- [ ] Access Key: `minioadmin`
- [ ] Secret: `minioadmin`
- [ ] Region: `us-east-1`
- [ ] Endpoint: `http://minio:9000`
- [ ] Force Path Style: ON
- [ ] Assign to: `WF08_UPLOAD_FILE_TO_MINIO`

### Slack (Optional)
- [ ] Create Slack app
- [ ] Get bot token
- [ ] Create credential in n8n
- [ ] Assign to: Approval/incident nodes

## Phase 5: Workflow IDs (5 min)
- [ ] Get all workflow IDs: `curl -H "X-N8N-API-KEY: <key>" http://localhost:5678/api/v1/workflows | jq`
- [ ] Update `.env` with IDs:
  - [ ] `WF_LISTING_ID=`
  - [ ] `WF_VOICE_ID=`
  - [ ] `WF_TALKING_ID=`
  - [ ] `WF_KLING_ID=`
  - [ ] `WF_CINEMATIC_ID=`
  - [ ] `WF_UPLOAD_ID=`
  - [ ] `WF_VOICE_UPLOAD_ID=`
  - [ ] `WF_RENDER_UPLOAD_ID=`
  - [ ] `AIOS_WF_POLICY_GATE_ID=`
  - [ ] `AIOS_WF_APPROVAL_REQUEST_ID=`
  - [ ] `AIOS_WF_CONTENT_FACTORY_ID=`
  - [ ] `AIOS_WF_FINANCE_GATE_ID=`
  - [ ] `AIOS_WF_KILL_SWITCH_ID=`
- [ ] Restart n8n: `docker compose restart n8n`

## Phase 6: API Keys (Optional)
- [ ] Get HeyGen API key (if using)
- [ ] Get ElevenLabs API key (if using)
- [ ] Get Kling API key (if using)
- [ ] Update `.env` with keys
- [ ] Restart n8n

## Phase 7: Testing (5 min)

### Test 1: MinIO Upload
- [ ] Open n8n UI
- [ ] Find `WF08_UPLOAD_FILE_TO_MINIO`
- [ ] Click "Execute Workflow"
- [ ] Verify public URL returned

### Test 2: Event Ingestion
- [ ] Run: `curl -X POST http://localhost:5678/webhook/aios/event -H "Content-Type: application/json" -d '{"event_type":"test"}'`
- [ ] Check n8n execution history

### Test 3: LSN Job
- [ ] Run: `curl -X POST http://localhost:5678/webhook/lsn/job -H "Content-Type: application/json" -d @06_EXAMPLES/LSN_example_jobs.json`
- [ ] Check execution history

## Post-Deployment

### Monitoring
- [ ] Set up container health checks
- [ ] Monitor disk space (MinIO storage)
- [ ] Check n8n logs regularly

### Backups
- [ ] Backup Postgres: `docker exec <postgres> pg_dump -U lsn lsn > backup.sql`
- [ ] Backup n8n data volume
- [ ] Backup MinIO data

### Security
- [ ] Change default passwords
- [ ] Set up reverse proxy (nginx)
- [ ] Enable HTTPS/TLS
- [ ] Restrict API key access
- [ ] Set up firewall rules

### Production Hardening
- [ ] Move to production domain
- [ ] Update `WEBHOOK_URL` in .env
- [ ] Update `PUBLIC_ASSET_BASE_URL` for CDN
- [ ] Enable n8n basic auth
- [ ] Set up monitoring/alerting
- [ ] Configure backup automation

## Troubleshooting

### n8n won't start
```bash
docker compose logs n8n | tail -50
```

### Postgres connection error
```bash
docker compose exec postgres psql -U lsn -d lsn -c "SELECT 1"
```

### Workflow import fails
```bash
# Check API key
curl -H "X-N8N-API-KEY: <key>" http://localhost:5678/api/v1/workflows

# Check JSON syntax
jq . 03_WORKFLOWS/LSN_CONTENT_FACTORY/WF00_ORCHESTRATOR.json
```

### MinIO not accessible
```bash
docker compose exec minio mc ls local/
```

### Webhook not triggering
- Check n8n logs
- Verify webhook URL in workflow
- Test with curl
- Check firewall rules

## Support
- n8n Docs: https://docs.n8n.io
- n8n Community: https://community.n8n.io
- Package Docs: See `00_DOCS/` directory
