#!/bin/bash
# Quick deployment script for n8n

set -e

echo "=========================================="
echo "N8N QUICK DEPLOYMENT SCRIPT"
echo "=========================================="

# Step 1: Setup
echo -e "\n[1/7] Setting up environment..."
cd "$(dirname "$0")/01_DOCKER"

if [ ! -f ".env" ]; then
    echo "Creating .env from example..."
    cp ../02_ENV/.env.example .env
    echo "✓ .env created - please update with your passwords"
else
    echo "✓ .env already exists"
fi

# Step 2: Start infrastructure
echo -e "\n[2/7] Starting Docker containers..."
docker compose up -d
echo "Waiting for containers to be healthy..."
sleep 10
docker compose ps

# Step 3: Initialize database
echo -e "\n[3/7] Initializing database..."
docker compose exec -T postgres psql -U lsn -d lsn < ../04_SCHEMAS/AI_Business_OS_schema.sql
echo "✓ Database initialized"

# Step 4: Get n8n API key
echo -e "\n[4/7] Waiting for n8n to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:5678 > /dev/null; then
        echo "✓ n8n is ready"
        break
    fi
    echo "Attempt $i/30..."
    sleep 2
done

# Step 5: Import workflows
echo -e "\n[5/7] Importing workflows..."
echo "Please get your n8n API key from Settings → API"
read -p "Enter N8N_API_KEY: " API_KEY
export N8N_API_KEY=$API_KEY
cd ..
python3 import_workflows.py

# Step 6: Get workflow IDs
echo -e "\n[6/7] Retrieving workflow IDs..."
echo "Workflow IDs saved to workflow_ids.json"
echo "Update 01_DOCKER/.env with these IDs and restart n8n:"
echo "  docker compose restart n8n"

# Step 7: Summary
echo -e "\n[7/7] Deployment complete!"
echo ""
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo "1. Update 01_DOCKER/.env with workflow IDs from workflow_ids.json"
echo "2. Create credentials in n8n UI:"
echo "   - Postgres (host: postgres, port: 5432)"
echo "   - MinIO S3 (endpoint: http://minio:9000)"
echo "3. Assign credentials to workflow nodes"
echo "4. Restart n8n: docker compose restart n8n"
echo "5. Test workflows"
echo ""
echo "n8n UI: http://localhost:5678"
echo "MinIO UI: http://localhost:9001"
echo ""
