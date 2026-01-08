# MinIO Public URL Strategy (SaaS-friendly)

HeyGen/Kling generally need HTTPS public URLs for audio/images.

Recommended:
- Put MinIO behind Cloudflare Tunnel or reverse proxy with TLS
- Use stable URLs: https://assets.yourdomain.com/lsn-assets/{object_key}
- Set PUBLIC_ASSET_BASE_URL accordingly

Avoid presigned URLs at first (they expire).
