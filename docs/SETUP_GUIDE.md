# Setup Guide - Local Development

This guide helps you set up Business Estimator for local development.

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 13+**
- **Git**
- **Claude API Key** from [console.anthropic.com](https://console.anthropic.com)

## Quick Start with Docker Compose (Recommended)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd business-estimator
```

### 2. Create environment files

**Create `.env` file in project root:**
```bash
cp backend/.env.example .env
```

**Edit `.env` and add:**
```
DB_USER=postgres
DB_PASSWORD=your_secure_password
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
ENVIRONMENT=development
VITE_API_URL=http://localhost:8000
```

### 3. Start all services

```bash
docker-compose up --build
```

This starts:
- PostgreSQL (port 5432)
- FastAPI Backend (port 8000)
- React Frontend (port 3000)
- Nginx Reverse Proxy (port 80)

### 4. Verify services

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Nginx (unified)**: http://localhost

---

## Manual Setup (Without Docker)

### Backend Setup

#### 1. Install Python dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Set up database

```bash
# Create PostgreSQL database
createdb business_estimator_db

# Or use psql:
psql -U postgres
CREATE DATABASE business_estimator_db;
\q
```

#### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/business_estimator_db
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
DEBUG=True
ENVIRONMENT=development
```

#### 4. Initialize database

```bash
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

#### 5. Run backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: **http://localhost:8000**

---

### Frontend Setup

#### 1. Install dependencies

```bash
cd frontend
npm install
```

#### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:
```
VITE_API_URL=http://localhost:8000
```

#### 3. Run development server

```bash
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## Testing the Setup

### 1. Check backend health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Check API docs
Visit: http://localhost:8000/docs

### 3. List businesses
```bash
curl http://localhost:8000/api/businesses/
```

### 4. Seed database (optional)
```bash
curl -X POST http://localhost:8000/api/businesses/seed
```

---

## Common Issues & Solutions

### Issue: PostgreSQL connection error
**Solution**: Verify PostgreSQL is running and credentials are correct in `.env`

### Issue: CLAUDE_API_KEY not set
**Solution**: Ensure your API key is in `.env` and backend is restarted

### Issue: Port already in use
**Solution**: Change port in docker-compose.yml or kill existing process:
```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: npm dependencies fail
**Solution**: Clear cache and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Development Workflow

### 1. Backend changes
- Edit files in `backend/app/`
- API auto-reloads with `uvicorn --reload`
- Check logs in terminal

### 2. Frontend changes
- Edit files in `frontend/src/`
- Vite hot-reloads automatically
- Check browser dev console for errors

### 3. Database changes
- Add new models in `backend/app/models.py`
- Restart backend to create tables
- Optionally use Alembic for migrations

### 4. Testing API
- Use Swagger UI: http://localhost:8000/docs
- Or use curl commands
- Or use Postman/Insomnia with localhost URLs

---

## Next Steps

1. ✅ Verify setup works
2. 📖 Read [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
3. 🎨 Customize business types and costs in database
4. 🧪 Test AI estimation endpoint
5. 🚀 Deploy to production

---

## Getting Help

- Check logs: `docker-compose logs -f backend`
- View API docs: http://localhost:8000/docs
- Check frontend console: Browser DevTools → Console

---

Happy coding! 🚀
