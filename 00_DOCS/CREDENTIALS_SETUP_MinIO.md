# Credentials Setup in n8n (MinIO)

Create an **AWS S3** credential named: `MinIO S3`
- Access Key: your MinIO user
- Secret: your MinIO password
- Region: us-east-1
- Endpoint: http://minio:9000
- Force Path Style: ON (if available)

Workflows use the AWS S3 node to upload to MinIO.
