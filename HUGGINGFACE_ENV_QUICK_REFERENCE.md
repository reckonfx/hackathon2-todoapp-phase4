# Hugging Face Environment Variables - Quick Reference

Copy and paste these environment variables into your Hugging Face Space settings:

## Essential Variables (Required)

### Database Connection
```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_fCJHD4Ak9ixo@ep-withered-dream-a8z1ay07-pooler.eastus2.azure.neon.tech/neondb
```

### JWT Secret (CHANGE THIS!)
```
SECRET_KEY=CHANGE_THIS_TO_A_SECURE_RANDOM_STRING_IN_PRODUCTION
```

**Generate a secure key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Environment
```
BACKEND_ENV=production
```

## Optional Variables (Recommended)

### Port Configuration
```
PORT=7860
BACKEND_PORT=7860
```

### CORS (Leave empty to allow all origins)
```
CORS_ORIGINS=
```

Or specify your frontend:
```
CORS_ORIGINS=https://your-frontend.vercel.app
```

### JWT Algorithm
```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Connection Pooling (for serverless)
```
POOL_SIZE=10
MAX_OVERFLOW=0
POOL_TIMEOUT=30
POOL_RECYCLE=300
POOL_PRE_PING=True
```

## How to Add in Hugging Face

1. Go to your Space: https://huggingface.co/spaces/aamirshamsi/webapp-hackathon-2
2. Click **Settings** tab
3. Scroll to **Repository secrets** or **Variables**
4. Click **Add a new secret/variable**
5. Enter the variable name (e.g., `DATABASE_URL`)
6. Enter the value
7. Click **Add**
8. Repeat for all variables above

## Verification After Deployment

Test your endpoints:

```bash
# Health check
curl https://aamirshamsi-webapp-hackathon-2.hf.space/health

# Register a user
curl -X POST https://aamirshamsi-webapp-hackathon-2.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass","name":"Test User"}'

# Login
curl -X POST https://aamirshamsi-webapp-hackathon-2.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass"}'
```

## Security Note

⚠️ **IMPORTANT:** Always use a strong, unique `SECRET_KEY` in production. Never use the default value!
