# N8N Master Deployment Package

Complete production-ready n8n automation system with 22 workflows across two domains: **LSN Content Factory** and **AI Business OS Kernel**.

## 🚀 Quick Start

```bash
git clone https://github.com/ecomtrading25-wq/n8n-master-deployment.git
cd n8n-master-deployment
chmod +x QUICK_DEPLOY.sh
./QUICK_DEPLOY.sh
```

## 📦 What's Included

### LSN Content Factory (13 Workflows)
AI-powered content generation pipeline:
- **Image Generation**: ComfyUI integration
- **Voice Synthesis**: ElevenLabs TTS
- **Avatar Videos**: HeyGen talking avatars
- **Video Generation**: Kling AI image-to-video
- **Asset Management**: MinIO S3 storage
- **Job Orchestration**: Batch processing with manifests

### AI Business OS Kernel (9 Workflows)
Enterprise automation system:
- **Event Ingestion**: Webhook-based event processing
- **Task Dispatching**: Intelligent task routing
- **Policy Gates**: Configurable validation rules
- **Approval Workflows**: Multi-step approval processes
- **Finance Gates**: Budget and cost control
- **Kill Switches**: Emergency operation controls
- **Metrics Collection**: Real-time monitoring

## 🛠️ Infrastructure

- **n8n**: Workflow automation platform
- **PostgreSQL**: Persistent data storage
- **Redis**: Caching and session management
- **MinIO**: S3-compatible object storage

All services configured via Docker Compose for easy deployment.

## 📋 Prerequisites

- Docker & Docker Compose installed
- 10GB+ free disk space
- Available ports: 5678, 5433, 6380, 9000, 9001

## 🔧 Deployment Options

### Option 1: Automated (Recommended)
```bash
chmod +x QUICK_DEPLOY.sh
./QUICK_DEPLOY.sh
```

### Option 2: Manual
```bash
# 1. Setup environment
cd 01_DOCKER
cp ../02_ENV/.env.example .env
# Edit .env with your passwords

# 2. Start infrastructure
docker compose up -d

# 3. Initialize database
docker compose exec postgres psql -U lsn -d lsn < ../04_SCHEMAS/AI_Business_OS_schema.sql

# 4. Import workflows
N8N_API_KEY=<your_key> python3 ../import_workflows.py

# 5. Configure credentials in n8n UI
# 6. Update .env with workflow IDs
# 7. Restart n8n
docker compose restart n8n
```

## 📚 Documentation

- **[README_DEPLOYMENT.md](README_DEPLOYMENT.md)** - Complete deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step checklist
- **[00_DOCS/QUICK_START.md](00_DOCS/QUICK_START.md)** - 5-10 minute quick start
- **[00_DOCS/IMPLEMENTATION_ORDER.md](00_DOCS/IMPLEMENTATION_ORDER.md)** - Detailed timeline
- **[00_DOCS/CREDENTIALS_MATRIX.md](00_DOCS/CREDENTIALS_MATRIX.md)** - Credential setup
- **[00_DOCS/WORKFLOWS_INDEX.md](00_DOCS/WORKFLOWS_INDEX.md)** - Workflow descriptions

## 🔐 Configuration

### Required Credentials (Create in n8n UI)

**Postgres**
```
Host: postgres
Port: 5432
Database: lsn
User: lsn
Password: <from .env>
```

**MinIO S3**
```
Endpoint: http://minio:9000
Access Key: minioadmin
Secret: minioadmin
Region: us-east-1
Force Path Style: ON
```

### Optional API Keys (Add to .env)
- `HEYGEN_API_KEY` - HeyGen avatar videos
- `ELEVENLABS_API_KEY` - Voice synthesis
- `PIAPI_KLING_API_KEY` - Video generation

## 🌐 Webhook Endpoints

After deployment, these webhooks are available:

```bash
# LSN Job Submission
POST http://localhost:5678/webhook/lsn/job

# AIOS Event Ingestion
POST http://localhost:5678/webhook/aios/event

# AIOS Approval Decision
POST http://localhost:5678/webhook/aios/approval
```

## 📁 Directory Structure

```
.
├── 00_DOCS/                    # Documentation
├── 01_DOCKER/                  # Docker Compose setup
│   ├── docker-compose.yml
│   └── .env (create from template)
├── 02_ENV/                     # Environment templates
├── 03_WORKFLOWS/               # All 22 workflow JSON files
│   ├── LSN_CONTENT_FACTORY/    # 13 content workflows
│   └── AI_BUSINESS_OS_KERNEL/  # 9 automation workflows
├── 04_SCHEMAS/                 # Database schemas
├── 05_CODE_HELPERS/            # Helper scripts
├── 06_EXAMPLES/                # Example payloads
├── import_workflows.py         # Automated import script
├── QUICK_DEPLOY.sh            # Quick deployment script
└── README_DEPLOYMENT.md       # Complete guide
```

## 🧪 Testing

```bash
# Test MinIO upload
curl -X POST http://localhost:5678/webhook/lsn/job \
  -H "Content-Type: application/json" \
  -d @06_EXAMPLES/LSN_example_jobs.json

# Test event ingestion
curl -X POST http://localhost:5678/webhook/aios/event \
  -H "Content-Type: application/json" \
  -d '{"event_type":"test","payload":{}}'
```

## 🔍 Monitoring

```bash
# Check container status
docker compose ps

# View n8n logs
docker compose logs n8n

# Check database
docker compose exec postgres psql -U lsn -d lsn -c "SELECT 1"

# Check MinIO
docker compose exec minio mc ls local/
```

## 🛡️ Production Deployment

For production use:

1. **Security**
   - Change all default passwords
   - Enable HTTPS/TLS
   - Set up reverse proxy (nginx)
   - Restrict API access

2. **Scaling**
   - Use external PostgreSQL
   - Set up MinIO cluster
   - Configure Redis clustering
   - Load balance n8n instances

3. **Monitoring**
   - Container health checks
   - Application monitoring
   - Log aggregation
   - Alerting setup

4. **Backups**
   - Automated database backups
   - MinIO bucket versioning
   - n8n data volume backups

## 🐛 Troubleshooting

### n8n won't start
```bash
docker compose logs n8n | tail -50
# Check N8N_ENCRYPTION_KEY length (32+ chars)
```

### Workflow import fails
```bash
# Verify API key
curl -H "X-N8N-API-KEY: <key>" http://localhost:5678/api/v1/workflows
```

### Database connection error
```bash
docker compose exec postgres psql -U lsn -d lsn -c "SELECT 1"
```

## 📄 License

This deployment package is provided as-is for n8n automation deployment.

## 🔗 Links

- **n8n Documentation**: https://docs.n8n.io
- **n8n Community**: https://community.n8n.io
- **Docker Documentation**: https://docs.docker.com

## 🤝 Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

**Version**: 1.0  
**Last Updated**: 2024  
**n8n Version**: Latest
