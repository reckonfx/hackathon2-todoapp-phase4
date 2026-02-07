# Hugging Face Deployment Checklist

Use this checklist to ensure successful deployment of your Todo App backend to Hugging Face Spaces.

## Pre-Deployment Checks

- [ ] **Code Changes Committed**
  - All fixes have been applied to the codebase
  - `backend/requirements.txt` includes `asyncpg>=0.29.0`
  - CORS configuration updated in `backend/src/main.py`
  - Dockerfile updated for port 7860

- [ ] **Local Testing Passed**
  ```bash
  cd backend
  pip install -r requirements.txt
  uvicorn src.main:app --reload
  # Test: http://localhost:8000/health
  ```

- [ ] **Database Accessible**
  - Neon PostgreSQL database is running
  - Connection string is correct
  - Database has required tables (run migrations if needed)

---

## Hugging Face Space Setup

- [ ] **Space Created**
  - Space name: `webapp-hackathon-2`
  - SDK: Docker
  - Visibility: Public/Private (your choice)

- [ ] **Environment Variables Configured**

  Navigate to: Space Settings → Repository Secrets/Variables

  ### Required Variables:
  - [ ] `DATABASE_URL`
    ```
    postgresql+asyncpg://neondb_owner:npg_fCJHD4Ak9ixo@ep-withered-dream-a8z1ay07-pooler.eastus2.azure.neon.tech/neondb
    ```

  - [ ] `SECRET_KEY`
    ```bash
    # Generate with:
    python3 -c "import secrets; print(secrets.token_urlsafe(32))"
    ```

  - [ ] `BACKEND_ENV`
    ```
    production
    ```

  ### Recommended Variables:
  - [ ] `PORT` = `7860`
  - [ ] `ALGORITHM` = `HS256`
  - [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
  - [ ] `POOL_SIZE` = `10`
  - [ ] `CORS_ORIGINS` = (leave empty for wildcard, or set your frontend URL)

---

## Code Deployment

- [ ] **Files Uploaded to Hugging Face**

  Ensure these files are in the Space repository root:
  - `Dockerfile`
  - `requirements.txt`
  - `src/` directory (all application code)
  - `alembic/` directory (database migrations)
  - `alembic.ini`

  ```bash
  # Option 1: Git Push
  git clone https://huggingface.co/spaces/aamirshamsi/webapp-hackathon-2
  cd webapp-hackathon-2
  cp -r /path/to/backend/* .
  git add .
  git commit -m "Deploy backend with fixes"
  git push
  ```

- [ ] **Build Started**
  - Check Space page for build status
  - Monitor build logs for errors

---

## Post-Deployment Verification

### Step 1: Check Build Logs
- [ ] Build completed successfully
- [ ] No dependency installation errors
- [ ] Application started without errors

Expected log output:
```
✓ Database Configuration Validated
  Database Type: PostgreSQL (async)
  Database Name: neondb
  Database Host: ep-withered-dream-a8z1ay07-pooler.eastus2.azure.neon.tech
  Provider: Neon PostgreSQL
✓ Database connection validated successfully
  Application is ready to accept requests
```

### Step 2: Test Endpoints

- [ ] **Root Endpoint**
  ```bash
  curl https://aamirshamsi-webapp-hackathon-2.hf.space/
  # Expected: {"message":"Todo API is running!"}
  ```

- [ ] **Health Check**
  ```bash
  curl https://aamirshamsi-webapp-hackathon-2.hf.space/health
  # Expected: {"status":"healthy","service":"todo-api","database":{...}}
  ```

- [ ] **User Registration**
  ```bash
  curl -X POST https://aamirshamsi-webapp-hackathon-2.hf.space/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123","name":"Test User"}'
  # Expected: {"success":true,"user":{...},"message":"Registration successful"}
  ```

- [ ] **User Login**
  ```bash
  curl -X POST https://aamirshamsi-webapp-hackathon-2.hf.space/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"test123"}'
  # Expected: {"success":true,"user":{...},"token":"..."}
  ```

### Step 3: Frontend Integration

- [ ] **Update Frontend Environment**

  File: `frontend/.env.local`
  ```
  NEXT_PUBLIC_API_BASE_URL=https://aamirshamsi-webapp-hackathon-2.hf.space
  ```

- [ ] **Test Frontend Login**
  - Open frontend in browser
  - Try to register a new user
  - Try to login with credentials
  - Check browser console for CORS errors (should be none)

- [ ] **Test Frontend Task Operations**
  - Create a new task
  - Edit a task
  - Delete a task
  - Toggle task completion

---

## Troubleshooting

If any checks fail, refer to:

### Build Failures
- Check `requirements.txt` has all dependencies
- Verify Dockerfile syntax
- Check Hugging Face build logs for specific errors

### Database Connection Errors
- Verify `DATABASE_URL` is correct
- Check Neon database is running
- Ensure connection string uses `postgresql+asyncpg://`
- Test connection locally first

### CORS Errors
- Check `BACKEND_ENV=production` is set
- Verify CORS middleware in logs
- Try setting `CORS_ORIGINS` to your frontend URL explicitly

### Authentication Errors
- Verify `SECRET_KEY` is set
- Check JWT settings (`ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Test registration endpoint first, then login

---

## Success Criteria

✅ All checks passed when:

1. Backend builds and starts without errors
2. All API endpoints respond correctly
3. Database connection is established
4. Frontend can communicate with backend
5. User registration and login work
6. Task CRUD operations work
7. No CORS errors in browser console

---

## Additional Resources

- [HUGGINGFACE_DEPLOYMENT.md](./HUGGINGFACE_DEPLOYMENT.md) - Detailed deployment guide
- [HUGGINGFACE_ENV_QUICK_REFERENCE.md](./HUGGINGFACE_ENV_QUICK_REFERENCE.md) - Environment variables reference
- [FIXES_APPLIED.md](./FIXES_APPLIED.md) - Summary of fixes applied

---

## Contact & Support

- **Hugging Face Spaces:** https://huggingface.co/docs/hub/spaces
- **Neon Database:** https://neon.tech/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

**Last Updated:** 2026-01-24
**Status:** Ready for Deployment ✅
