# Hugging Face Deployment Guide

This guide provides step-by-step instructions for deploying the Todo Web Application backend to Hugging Face Spaces.

## Prerequisites

- Hugging Face account
- Backend code ready in the repository
- Neon PostgreSQL database credentials

## Required Environment Variables

Configure the following environment variables in your Hugging Face Space settings:

### 1. Database Configuration

```bash
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_fCJHD4Ak9ixo@ep-withered-dream-a8z1ay07-pooler.eastus2.azure.neon.tech/neondb
```

**Important:** Make sure to use your actual Neon database connection string with `postgresql+asyncpg://` protocol.

### 2. Authentication & Security

```bash
SECRET_KEY=your-super-secret-jwt-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Security Note:** Generate a strong, unique `SECRET_KEY` for production. You can generate one using:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3. Application Settings

```bash
BACKEND_ENV=production
BACKEND_HOST=0.0.0.0
BACKEND_PORT=7860
```

**Note:** Hugging Face Spaces use port 7860 by default. The Dockerfile is configured to use the `PORT` environment variable.

### 4. CORS Configuration (Optional)

```bash
CORS_ORIGINS=https://your-frontend-domain.com,https://another-domain.com
```

**Default Behavior:** In production mode, if `CORS_ORIGINS` is not set or only has default localhost values, the application will allow all origins (`*`). For better security, specify your frontend URLs.

### 5. Connection Pooling (Recommended)

```bash
POOL_SIZE=10
MAX_OVERFLOW=0
POOL_TIMEOUT=30
POOL_RECYCLE=300
POOL_PRE_PING=True
```

**Note:** Lower `POOL_SIZE` for serverless/free-tier deployments to avoid connection limits.

## Deployment Steps

### Step 1: Create a Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **Name:** `webapp-hackathon-2` (or your preferred name)
   - **SDK:** Docker
   - **Visibility:** Public or Private

### Step 2: Configure Environment Variables

1. Navigate to your Space's **Settings** tab
2. Scroll to **Repository secrets** or **Variables** section
3. Add all the environment variables listed above
4. Click **Save** for each variable

### Step 3: Push Your Code

#### Option A: Direct Upload
1. Upload your `backend/` folder to the Space repository
2. Ensure `Dockerfile` and `requirements.txt` are in the root of the Space

#### Option B: Git Push
```bash
# Clone your Hugging Face Space repository
git clone https://huggingface.co/spaces/your-username/webapp-hackathon-2
cd webapp-hackathon-2

# Copy backend files
cp -r /path/to/your/backend/* .

# Commit and push
git add .
git commit -m "Deploy backend to Hugging Face"
git push
```

### Step 4: Wait for Build

Hugging Face will automatically:
1. Build the Docker container
2. Install dependencies from `requirements.txt`
3. Start the application on port 7860
4. Make it available at `https://your-username-webapp-hackathon-2.hf.space`

### Step 5: Verify Deployment

Test your deployed backend:

```bash
# Test root endpoint
curl https://your-username-webapp-hackathon-2.hf.space/

# Test health check
curl https://your-username-webapp-hackathon-2.hf.space/health

# Test registration
curl -X POST https://your-username-webapp-hackathon-2.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","name":"Test User"}'

# Test login
curl -X POST https://your-username-webapp-hackathon-2.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## Troubleshooting

### Issue: "Internal Server Error" on Authentication

**Cause:** Missing `asyncpg` dependency or environment variables

**Solution:**
1. Verify `asyncpg>=0.29.0` is in `requirements.txt`
2. Check all environment variables are set correctly
3. View Space logs for detailed error messages

### Issue: CORS Errors from Frontend

**Cause:** Frontend domain not allowed in CORS configuration

**Solution:**
1. Add your frontend URL to `CORS_ORIGINS` environment variable
2. Or, leave it unset for production to allow all origins (less secure)
3. Restart the Space after changing environment variables

### Issue: Database Connection Errors

**Cause:** Incorrect `DATABASE_URL` or Neon database not accessible

**Solution:**
1. Verify Neon database is running and accessible
2. Check connection string format: `postgresql+asyncpg://user:pass@host/dbname`
3. Ensure SSL is enabled for Neon connections (handled automatically)

### Issue: Port Binding Errors

**Cause:** Hugging Face expects port 7860 but app uses different port

**Solution:**
1. Ensure `PORT=7860` environment variable is set
2. Or, Dockerfile will default to 7860 if not specified

## Monitoring

### View Logs
1. Go to your Space's page
2. Click on the **Logs** tab
3. Monitor startup messages and errors

### Expected Startup Logs
```
✓ Database Configuration Validated
  Database Type: PostgreSQL (async)
  Database Name: neondb
  Database Host: ep-withered-dream-a8z1ay07-pooler.eastus2.azure.neon.tech
  Provider: Neon PostgreSQL
✓ Database connection validated successfully
  Application is ready to accept requests
```

## Security Best Practices

1. **Never commit `.env` files** - Use Hugging Face Secrets for sensitive data
2. **Use strong `SECRET_KEY`** - Generate cryptographically secure keys
3. **Enable HTTPS only** - Hugging Face provides HTTPS by default
4. **Limit CORS origins** - Specify exact frontend URLs in production
5. **Rotate credentials** - Change passwords and keys periodically
6. **Monitor access logs** - Review Space logs regularly for suspicious activity

## Database Migration

If you need to run Alembic migrations:

1. Access the Space's terminal (if available) or run locally:
```bash
alembic upgrade head
```

2. Or, create a startup script that runs migrations before starting the app:
```bash
#!/bin/bash
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
```

## Support

For issues specific to:
- **Hugging Face Spaces:** [HF Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- **Neon Database:** [Neon Docs](https://neon.tech/docs)
- **FastAPI:** [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Next Steps

After successful deployment:
1. Update frontend's `NEXT_PUBLIC_API_BASE_URL` to point to your Hugging Face Space URL
2. Test all API endpoints thoroughly
3. Set up monitoring and alerting
4. Configure custom domain (optional)
5. Enable authentication rate limiting for production
