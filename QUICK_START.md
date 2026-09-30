# STEP-BY-STEP UPLOAD & DEPLOYMENT GUIDE

Complete walkthrough to get Business Estimator running on your local machine or cloud.

---

## 📋 PART 1: DOWNLOAD & EXTRACT

### Step 1: Download the project
You've received a `business-estimator.zip` file

### Step 2: Extract on your computer

**Windows:**
- Right-click the zip file
- Select "Extract All..."
- Choose a folder (e.g., `C:\projects\`)

**macOS:**
- Double-click the zip file (auto-extracts)
- Or: Open Terminal and run:
```bash
unzip business-estimator.zip
cd business-estimator
```

**Linux:**
```bash
unzip business-estimator.zip
cd business-estimator
```

---

## 🔧 PART 2: PREREQUISITES CHECK

### What you need:

**Option A: Docker (Easiest - Recommended)**
- ✅ [Install Docker](https://docs.docker.com/get-docker/)
- ✅ [Install Docker Compose](https://docs.docker.com/compose/install/)
- ✅ Claude API Key from [console.anthropic.com](https://console.anthropic.com)

**Option B: Manual Setup**
- ✅ Python 3.11+ ([Download](https://www.python.org/))
- ✅ Node.js 18+ ([Download](https://nodejs.org/))
- ✅ PostgreSQL 13+ ([Download](https://www.postgresql.org/))
- ✅ Claude API Key

### Check installations:

```bash
# Docker
docker --version
docker-compose --version

# OR Manual setup
python --version      # Should be 3.11+
node --version        # Should be 18+
npm --version         # Should be 8+
psql --version        # Should be 13+
```

---

## 🚀 PART 3: QUICK START WITH DOCKER (RECOMMENDED)

### Step 1: Get your Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Login/Signup
3. Create API key
4. Copy the key (starts with `sk-ant-`)

### Step 2: Create environment file

In the project root folder, create a file named `.env`:

```bash
# Windows: Use Notepad or VS Code
# macOS/Linux: Use Terminal

cat > .env <<EOF
# Database
DB_USER=postgres
DB_PASSWORD=secure_password_123

# Claude API
CLAUDE_API_KEY=sk-ant-YOUR_API_KEY_HERE

# Environment
ENVIRONMENT=development
DEBUG=True

# Frontend API URL
VITE_API_URL=http://localhost:8000
EOF
```

**On Windows (using Notepad):**
1. Open Notepad
2. Paste this content:
```
DB_USER=postgres
DB_PASSWORD=secure_password_123
CLAUDE_API_KEY=sk-ant-YOUR_API_KEY_HERE
ENVIRONMENT=development
DEBUG=True
VITE_API_URL=http://localhost:8000
```
3. Save as `.env` in the project root (not `.env.txt`)

### Step 3: Start everything

```bash
cd business-estimator
docker-compose up --build
```

**What's happening:**
- 🐘 PostgreSQL database starting
- 🐍 FastAPI backend starting
- ⚛️ React frontend starting
- 🔄 Nginx proxy starting

**Wait for this message:**
```
business-estimator-frontend   | ➜  Local:   http://localhost:3000/
```

### Step 4: Access the application

Open your browser:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📦 PART 4: MANUAL SETUP (NO DOCKER)

### Backend Setup

#### Step 1: Create database

```bash
# macOS/Linux with PostgreSQL installed
psql -U postgres

# In psql terminal:
CREATE DATABASE business_estimator_db;
\q
```

#### Step 2: Create backend environment

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/business_estimator_db
CLAUDE_API_KEY=sk-ant-YOUR_API_KEY_HERE
DEBUG=True
ENVIRONMENT=development
```

#### Step 3: Install & run backend

```bash
# Create virtual environment
python -m venv venv

# Activate
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

---

### Frontend Setup

In a **new terminal window**:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## ✅ PART 5: VERIFY EVERYTHING WORKS

### Test 1: Backend health

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{"status": "healthy"}
```

### Test 2: Get businesses

```bash
curl http://localhost:8000/api/businesses/
```

**Expected response:**
```json
[
  {
    "id": "...",
    "name": "Cafe",
    "description": "Coffee shop or casual dining cafe",
    "category": "Food & Beverage",
    "icon": "☕"
  },
  ...
]
```

### Test 3: View API documentation

Open browser: http://localhost:8000/docs

Should see interactive API docs (Swagger UI)

### Test 4: Access frontend

Open browser: http://localhost:3000

Should see the Business Estimator homepage

---

## 🌍 PART 6: DEPLOY TO CLOUD

### Deploy to DigitalOcean (Simple)

#### Step 1: Create droplet

1. Go to [DigitalOcean](https://www.digitalocean.com)
2. Create account
3. Click "Create" → "Droplets"
4. Select:
   - Image: Ubuntu 22.04
   - Size: $6/month (2GB RAM minimum)
5. Add SSH key or password
6. Create

#### Step 2: SSH into server

```bash
ssh root@your_droplet_ip
```

#### Step 3: Clone project

```bash
git clone https://github.com/YOUR_USERNAME/business-estimator.git
cd business-estimator
```

#### Step 4: Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

#### Step 5: Setup environment

```bash
nano .env
# Paste your configuration
# Ctrl+X → Y → Enter to save
```

#### Step 6: Start

```bash
docker-compose up -d
```

#### Step 7: Access

Open browser: `http://your_droplet_ip`

---

### Deploy to Azure (Alternative)

1. Create resource group
2. Create Container Registry
3. Push Docker images
4. Create Azure Database for PostgreSQL
5. Deploy container instances
6. Link with DNS

[Detailed Azure guide →](./docs/DEPLOYMENT_GUIDE.md#option-1-azure-deployment)

---

### Deploy to AWS (Enterprise)

1. Create ECR repositories
2. Push Docker images
3. Create RDS PostgreSQL
4. Create ECS cluster
5. Create task definitions
6. Create services and load balancer

[Detailed AWS guide →](./docs/DEPLOYMENT_GUIDE.md#option-2-aws-ecs--rds-deployment)

---

## 🐛 TROUBLESHOOTING

### "Port already in use"

```bash
# Kill process using port 8000
# macOS/Linux:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "CLAUDE_API_KEY not found"

1. Check `.env` file exists in project root
2. Verify key format: `sk-ant-xxxxxxxxxxxx`
3. Restart containers: `docker-compose restart`

### "PostgreSQL connection failed"

```bash
# Docker version:
docker-compose ps
docker-compose logs postgres

# Manual version:
# Verify PostgreSQL is running
# Check DATABASE_URL format
psql postgresql://postgres:password@localhost:5432/business_estimator_db
```

### "Frontend shows blank page"

1. Check browser console (F12 → Console)
2. Check VITE_API_URL in frontend/.env
3. Verify backend is running: `curl http://localhost:8000`
4. Restart frontend: `npm run dev`

### "npm install fails"

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Project Statistics

```
Backend:
├── FastAPI with async/await
├── SQLAlchemy ORM + PostgreSQL
├── Claude AI integration
├── Multi-agent architecture
└── RESTful API (25+ endpoints)

Frontend:
├── React 18 + Hooks
├── Tailwind CSS
├── Vite bundler
├── Axios for API calls
└── Responsive design

Infrastructure:
├── Docker + Docker Compose
├── PostgreSQL 16
├── Nginx reverse proxy
├── Health checks
└── Production-ready
```

---

## 🎯 Next Steps After Setup

1. ✅ **Verify basic functionality**
   - Open http://localhost:3000
   - Click through different business types
   - Try the cost calculator

2. 📊 **Test AI estimation**
   - Go to API docs: http://localhost:8000/docs
   - Try `/api/ai/estimate` endpoint
   - Verify Claude integration works

3. 🎨 **Customize data**
   - Add more business types
   - Customize cost categories
   - Add cost items per business

4. 🧪 **Run tests**
   - Test on different browsers
   - Test on mobile devices
   - Verify all features work

5. 🚀 **Deploy to production**
   - Follow [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)
   - Set up monitoring
   - Configure domain & SSL

---

## 📚 Documentation

- **Setup Details**: [SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)
- **Deployment**: [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)
- **API Docs**: http://localhost:8000/docs (when running)
- **Repository**: Check GitHub for latest code

---

## 💬 Support

Having issues? Check:

1. **Error messages** in terminal logs
2. **Docker logs**: `docker-compose logs -f backend`
3. **Browser console**: Press F12 → Console tab
4. **API docs**: http://localhost:8000/docs

---

## 🎉 Success!

You now have a fully functional Business Estimator application with:
- ✅ Cost calculation engine
- ✅ AI-powered insights via Claude
- ✅ Multi-business type support
- ✅ Professional UI
- ✅ Production-ready deployment

**Happy coding! 🚀**
