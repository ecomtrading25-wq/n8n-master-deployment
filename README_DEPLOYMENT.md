# N8N Master Deployment Package - Complete Guide

## What's Included

This package contains a production-ready n8n automation system with 22 workflows across two domains:

### LSN Content Factory (13 workflows)
AI-powered content generation pipeline supporting:
- Image generation (ComfyUI)
- Voice synthesis (ElevenLabs)
- Avatar videos (HeyGen)
- Video generation (Kling AI)
- File uploads and asset management (MinIO)

### AI Business OS Kernel (9 workflows)
Enterprise automation system supporting:
- Event ingestion and processing
- Task dispatching and routing
- Policy validation gates
- Approval workflows
- Finance validation gates
- Emergency kill switches
- Metrics collection

## Quick Start (30 minutes)

### Prerequisites
- Docker & Docker Compose installed
- 10GB+ free disk space
- Ports available: 5678, 5433, 6380, 9000, 9001

### Automated Deployment
```bash
cd N8N_MASTER_DEPLOYMENT_PACKAGE
chmod +x QUICK_DEPLOY.sh
./QUICK_DEPLOY.sh
```

### Manual Deployment

**1. Start Infrastructure**
```bash
cd 01_DOCKER
cp ../02_ENV/.env.example .env
# Edit .env with your passwords
docker compose up -d
```

**2. Initialize Database**
```bash
docker compose exec postgres psql -U lsn -d lsn < ../04_SCHEMAS/AI_Business_OS_schema.sql
```

**3. Import Workflows**
```bash
# Get API key from n8n Settings → API
N8N_API_KEY=your_key python3 ../import_workflows.py
```

**4. Configure Credentials**
- Open http://localhost:5678
- Create Postgres credential (host: postgres, port: 5432)
- Create MinIO S3 credential (endpoint: http://minio:9000)
- Assign to workflow nodes

**5. Update Workflow IDs**
- Get IDs from workflow_ids.json
- Update 01_DOCKER/.env
- Restart n8n: `docker compose restart n8n`

**6. Test**
```bash
# Test MinIO upload
curl -X POST http://localhost:5678/webhook/lsn/job \
  -H "Content-Type: application/json" \
  -d @06_EXAMPLES/LSN_example_jobs.json
```

## Directory Structure

```
N8N_MASTER_DEPLOYMENT_PACKAGE/
├── 00_DOCS/                          # Documentation
│   ├── QUICK_START.md
│   ├── IMPLEMENTATION_ORDER.md
│   ├── CREDENTIALS_MATRIX.md
│   ├── WORKFLOWS_INDEX.md
│   └── ...
├── 01_DOCKER/                        # Docker setup
│   ├── docker-compose.yml
│   └── .env                          # Configuration (create from .env.example)
├── 02_ENV/                           # Environment templates
│   ├── .env.example
│   └── .env.example.lsn
├── 03_WORKFLOWS/                     # All 22 workflows
│   ├── LSN_CONTENT_FACTORY/          # 13 content workflows
│   │   ├── WF00_ORCHESTRATOR.json
│   │   ├── WF01_COMFYUI_LISTING.json
│   │   ├── WF02_ELEVENLABS_VOICE.json
│   │   ├── WF03_HEYGEN_TALKING.json
│   │   ├── WF04_KLING_IMAGE2VIDEO.json
│   │   ├── WF05_VEO_PLACEHOLDER.json
│   │   ├── WF06_PACKAGER_OPTIONAL.json
│   │   ├── WF08_UPLOAD_FILE_TO_MINIO.json
│   │   ├── WF09_VOICE_TTS_AND_UPLOAD.json
│   │   ├── WF10_COMFYUI_RENDER_AND_UPLOAD.json
│   │   ├── WF11_HEYGEN_TALKING_END2END.json
│   │   ├── WF12_KLING_I2V_END2END.json
│   │   └── WF20_RUN_JOB_MANIFEST.json
│   └── AI_BUSINESS_OS_KERNEL/        # 9 automation workflows
│       ├── 01_event_ingest.json
│       ├── 02_task_dispatcher.json
│       ├── 03_policy_gate_subworkflow.json
│       ├── 04_approval_request_subworkflow.json
│       ├── 05_approval_decision_webhook.json
│       ├── 06_content_factory_subworkflow.json
│       ├── 07_finance_gate_subworkflow.json
│       ├── 08_kill_switch_subworkflow.json
│       └── 09_metrics_snapshot.json
├── 04_SCHEMAS/                       # Database schemas
│   ├── AI_Business_OS_schema.sql
│   └── LSN_Job.json
├── 05_CODE_HELPERS/                  # Helper scripts
│   ├── caption_srt.py
│   └── packager.py
├── 06_EXAMPLES/                      # Example data
│   ├── LSN_example_jobs.json
│   └── LSN_JOB_MANIFEST_EXAMPLE.json
├── import_workflows.py               # Automated import script
├── QUICK_DEPLOY.sh                   # Quick deployment script
├── DEPLOYMENT_CHECKLIST.md           # Deployment checklist
└── README_DEPLOYMENT.md              # This file
```

## Key Features

### LSN Content Factory
- **End-to-end workflows**: From job submission to asset delivery
- **Multiple AI providers**: ComfyUI, HeyGen, ElevenLabs, Kling
- **Asset management**: MinIO S3 integration for file storage
- **Job manifest support**: Batch processing capabilities
- **Output packaging**: Optional workflow output packaging

### AI Business OS
- **Event-driven architecture**: Webhook-based event ingestion
- **Policy enforcement**: Configurable policy gates
- **Approval workflows**: Multi-step approval processes
- **Finance validation**: Cost control and budget gates
- **Emergency controls**: Kill switch for stopping operations
- **Metrics**: Real-time metrics collection and snapshots

## Configuration

### Environment Variables
Key variables in `01_DOCKER/.env`:

```bash
# Database
POSTGRES_USER=lsn
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=lsn

# n8n
N8N_ENCRYPTION_KEY=32_character_minimum_encryption_key
N8N_HOST=localhost
N8N_PROTOCOL=http
WEBHOOK_URL=http://localhost:5678/

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
PUBLIC_ASSET_BASE_URL=http://localhost:9000/lsn-assets

# API Keys (optional)
HEYGEN_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
PIAPI_KLING_API_KEY=your_key

# Workflow IDs (populated after import)
WF_LISTING_ID=
WF_VOICE_ID=
WF_TALKING_ID=
# ... etc
```

### Credentials in n8n

**Postgres Credential**
- Host: `postgres`
- Port: `5432`
- Database: `lsn`
- User: `lsn`
- Password: (from .env)

**MinIO S3 Credential**
- Access Key: `minioadmin`
- Secret: `minioadmin`
- Region: `us-east-1`
- Endpoint: `http://minio:9000`
- Force Path Style: ON

## Webhook Endpoints

After deployment, use these webhooks:

### LSN Job Submission
```bash
POST /webhook/lsn/job
Content-Type: application/json

{
  "job_id": "unique_id",
  "content_type": "video",
  "parameters": {...}
}
```

### AIOS Event Ingestion
```bash
POST /webhook/aios/event
Content-Type: application/json

{
  "event_type": "content_request",
  "payload": {...}
}
```

### AIOS Approval Decision
```bash
POST /webhook/aios/approval
Content-Type: application/json

{
  "approval_id": "id",
  "decision": "approved",
  "reason": "..."
}
```

## Monitoring & Maintenance

### Health Checks
```bash
# Check all containers
docker compose ps

# Check n8n logs
docker compose logs n8n

# Check database
docker compose exec postgres psql -U lsn -d lsn -c "SELECT 1"

# Check MinIO
docker compose exec minio mc ls local/
```

### Backups
```bash
# Backup database
docker compose exec postgres pg_dump -U lsn lsn > backup.sql

# Restore database
docker compose exec -T postgres psql -U lsn -d lsn < backup.sql

# Backup n8n data
docker cp n8n_n8n_1:/home/node/.n8n ./n8n_backup
```

## Troubleshooting

### n8n won't start
```bash
docker compose logs n8n | tail -50
# Check encryption key length (32+ chars)
# Check port 5678 availability
```

### Workflow import fails
```bash
# Verify API key
curl -H "X-N8N-API-KEY: your_key" http://localhost:5678/api/v1/workflows

# Check JSON syntax
jq . 03_WORKFLOWS/LSN_CONTENT_FACTORY/WF00_ORCHESTRATOR.json
```

### Postgres connection error
```bash
docker compose exec postgres psql -U lsn -d lsn -c "SELECT 1"
# Check POSTGRES_PASSWORD in .env
```

### MinIO not accessible
```bash
docker compose exec minio mc ls local/
# Check MINIO_ROOT_USER and MINIO_ROOT_PASSWORD
```

## Production Deployment

For production:

1. **Security**
   - Change all default passwords
   - Enable HTTPS/TLS
   - Set up reverse proxy (nginx)
   - Restrict API key access

2. **Scaling**
   - Use external Postgres database
   - Set up MinIO cluster
   - Configure Redis for caching
   - Use load balancer for n8n

3. **Monitoring**
   - Set up container health checks
   - Configure alerting
   - Enable audit logging
   - Monitor disk space

4. **Backups**
   - Automated Postgres backups
   - MinIO bucket versioning
   - n8n data volume backups
   - Document recovery procedures

## Support & Documentation

- **n8n Docs**: https://docs.n8n.io
- **n8n Community**: https://community.n8n.io
- **Package Docs**: See `00_DOCS/` directory
- **API Reference**: http://localhost:5678/api/v1/docs (after startup)

## License & Attribution

This deployment package is provided as-is for n8n automation deployment.

---

**Last Updated**: 2024
**Package Version**: 1.0
**n8n Version**: Latest (from docker-compose.yml)
