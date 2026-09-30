# Deployment Guide - Production Setup

Complete guide to deploy Business Estimator to production on Azure, AWS, or any cloud provider.

## Deployment Options

### Option 1: Azure Container Instances (Recommended for simplicity)
### Option 2: AWS ECS + RDS
### Option 3: DigitalOcean App Platform
### Option 4: Self-hosted with VPS

---

## Prerequisites

- Docker & Docker Compose
- Domain name (optional, use IP for now)
- Cloud account (Azure/AWS/DigitalOcean)
- Claude API key
- GitHub account (for CI/CD)

---

## Option 1: Azure Deployment

### 1. Prepare Docker images

```bash
# Build images
docker-compose build

# Create Azure Container Registry
az acr create --resource-group myResourceGroup --name myregistry --sku Basic

# Login to registry
az acr login --name myregistry

# Tag and push images
docker tag business-estimator-backend myregistry.azurecr.io/backend:latest
docker tag business-estimator-frontend myregistry.azurecr.io/frontend:latest

docker push myregistry.azurecr.io/backend:latest
docker push myregistry.azurecr.io/frontend:latest
```

### 2. Create PostgreSQL Database

```bash
az postgres server create \
  --resource-group myResourceGroup \
  --name mydbserver \
  --location eastus \
  --admin-user postgres \
  --admin-password MySecurePassword123
```

### 3. Deploy with Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name business-estimator \
  --image myregistry.azurecr.io/backend:latest \
  --registry-login-server myregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --environment-variables \
    DATABASE_URL=postgresql://postgres:MySecurePassword123@mydbserver.postgres.database.azure.com/business_estimator_db \
    CLAUDE_API_KEY=$CLAUDE_API_KEY \
  --ports 8000 \
  --ip-address public
```

### 4. Setup environment variables

Create `.env` in production with:
```
# Database
DATABASE_URL=postgresql://postgres:password@mydbserver.postgres.database.azure.com/business_estimator_db

# API Keys
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxx

# Settings
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=generate-a-secure-random-key
CORS_ORIGINS=["https://yourdomain.com"]
```

---

## Option 2: AWS ECS + RDS Deployment

### 1. Create RDS PostgreSQL instance

```bash
aws rds create-db-instance \
  --db-instance-identifier business-estimator-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password MySecurePassword123 \
  --allocated-storage 20 \
  --publicly-accessible
```

### 2. Push images to ECR

```bash
# Create ECR repositories
aws ecr create-repository --repository-name business-estimator-backend
aws ecr create-repository --repository-name business-estimator-frontend

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag business-estimator-backend 123456789.dkr.ecr.us-east-1.amazonaws.com/business-estimator-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/business-estimator-backend:latest
```

### 3. Create ECS Cluster and Task Definitions

```bash
# Create cluster
aws ecs create-cluster --cluster-name business-estimator

# Create task definition (reference aws-task-definition.json)
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json
```

### 4. Create ECS Services

```bash
aws ecs create-service \
  --cluster business-estimator \
  --service-name backend \
  --task-definition business-estimator-backend:1 \
  --desired-count 2 \
  --launch-type EC2
```

---

## Option 3: DigitalOcean App Platform

### 1. Prepare app.yaml

```yaml
name: business-estimator
services:
- name: backend
  github:
    repo: your-username/business-estimator
    branch: main
  build_command: cd backend && pip install -r requirements.txt
  run_command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  http_port: 8000
  envs:
  - key: DATABASE_URL
    value: ${db.username}:${db.password}@${db.host}:${db.port}/${db.name}
  - key: CLAUDE_API_KEY
    value: ${CLAUDE_API_KEY}
    type: SECRET
  health_check:
    http_path: /health

- name: frontend
  github:
    repo: your-username/business-estimator
    branch: main
  build_command: cd frontend && npm install && npm run build
  http_port: 3000
  source_dir: frontend/dist

databases:
- name: db
  engine: PG
  version: "13"
  production: true
```

### 2. Deploy

```bash
doctl apps create --spec app.yaml
```

---

## Option 4: Self-hosted VPS (DigitalOcean/Linode)

### 1. SSH into VPS

```bash
ssh root@your_vps_ip
```

### 2. Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 3. Clone repository

```bash
git clone https://github.com/your-username/business-estimator.git
cd business-estimator
```

### 4. Create production .env

```bash
cat > .env <<EOF
DB_USER=postgres
DB_PASSWORD=$(openssl rand -base64 32)
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxx
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=$(openssl rand -base64 32)
CORS_ORIGINS=["https://yourdomain.com"]
VITE_API_URL=https://yourdomain.com
EOF
```

### 5. Start services

```bash
docker-compose -f docker-compose.yml up -d
```

### 6. Setup SSL with Let's Encrypt

```bash
apt-get install certbot python3-certbot-nginx
certbot certonly --standalone -d yourdomain.com
```

Update `nginx.conf` with SSL certificates and restart.

### 7. Setup domain DNS

Point your domain to VPS IP in DNS settings:
```
A record: @ -> your_vps_ip
CNAME: www -> @ (or your_vps_ip)
```

---

## Post-Deployment Checklist

- [ ] Database migrations completed
- [ ] Environment variables set
- [ ] API endpoints working
- [ ] Frontend loading
- [ ] SSL certificate installed
- [ ] Domain pointing to server
- [ ] Health checks passing
- [ ] Logs monitored
- [ ] Backup strategy in place
- [ ] Monitoring/alerts configured

---

## Monitoring & Maintenance

### View logs

```bash
# Docker compose
docker-compose logs -f backend
docker-compose logs -f frontend

# VPS syslog
tail -f /var/log/syslog
```

### Database backup

```bash
# Manual backup
pg_dump business_estimator_db > backup-$(date +%Y%m%d).sql

# Automated daily backup
0 2 * * * pg_dump business_estimator_db | gzip > /backups/db-$(date +\%Y\%m\%d).sql.gz
```

### Update application

```bash
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```

---

## Performance Optimization

### 1. Database tuning

```sql
-- Add indexes
CREATE INDEX idx_estimates_business_id ON estimates(business_type_id);
CREATE INDEX idx_estimates_created_at ON estimates(created_at);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM estimates WHERE business_type_id = 'xxx';
```

### 2. Caching

Add Redis for caching:
```yaml
# In docker-compose.yml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

### 3. CDN

Serve frontend assets through Cloudflare or AWS CloudFront:
- Faster image delivery
- Automatic compression
- DDoS protection

---

## Scaling

### Horizontal scaling (multiple instances)

1. Use load balancer (AWS ALB, Azure Load Balancer)
2. Deploy multiple backend instances
3. Use RDS for shared database
4. Use S3/Blob Storage for media

### Vertical scaling

1. Increase instance size (CPU, RAM)
2. Upgrade RDS instance class
3. Increase database connection pool

---

## Troubleshooting

### Container won't start
```bash
docker-compose logs backend
docker-compose ps
```

### Database connection timeout
- Check security groups/firewall rules
- Verify DATABASE_URL
- Test connection: `psql $DATABASE_URL`

### High memory usage
- Check for memory leaks in logs
- Restart services: `docker-compose restart`
- Increase container limits in compose file

### API slow response
- Check database query performance
- Enable query logging
- Add database indexes
- Check API rate limits

---

## Support & Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Compose Production](https://docs.docker.com/compose/production/)
- [PostgreSQL Administration](https://www.postgresql.org/docs/current/admin.html)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

Next: Monitor logs and collect user feedback!
