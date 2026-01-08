# Credentials Matrix (what to create in n8n)

The imported workflows intentionally **do not include secrets**. After import, n8n will show nodes with missing credentials.

## 1) Postgres credential (required)
Create a Postgres credential named (suggested): `LSN Postgres`

If you use the included Docker Compose:
- Host: `postgres`
- Port: `5432`
- Database: `${POSTGRES_DB}`
- User: `${POSTGRES_USER}`
- Password: `${POSTGRES_PASSWORD}`

Then open each workflow and assign this credential to every **Postgres** node (n8n highlights missing creds).

## 2) MinIO S3 credential (required for uploads)
Create an **AWS S3** credential named: `MinIO S3`
- Access Key: `${MINIO_ROOT_USER}` (or your MinIO user)
- Secret: `${MINIO_ROOT_PASSWORD}`
- Region: `us-east-1`
- Endpoint: `http://minio:9000`
- Force Path Style: ON (if available)

Assign it in:
- `WF08_UPLOAD_FILE_TO_MINIO` (AWS S3 node)

## 3) Slack credential (optional)
Used in AI Business OS workflows:
- approval notifications
- incident notifications (kill-switch)

Create a Slack credential and assign it to the Slack nodes in:
- `AI-OS 04 - Approval Request (Sub-workflow)`
- `AI-OS 08 - Kill Switch (Sub-workflow)`

## 4) API keys (no n8n credential needed)
HeyGen / ElevenLabs / Kling are called via **HTTP Request** nodes and read keys from `.env`.
Fill env vars:
- `HEYGEN_API_KEY`
- `ELEVENLABS_API_KEY` (+ `ELEVENLABS_VOICE_ID`)
- `PIAPI_KLING_API_KEY`
