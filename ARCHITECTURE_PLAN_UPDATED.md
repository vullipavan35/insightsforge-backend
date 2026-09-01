# InsightForge AI Lite - Monolithic Architecture Plan

## 🏗️ System Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                │
│                    (Web Browser / Mobile)                          │
│                   Next.js (TypeScript/React)                       │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTPS/WebSocket
┌───────────────────────────┼─────────────────────────────────────────┐
│                    PYTHON MONOLITHIC BACKEND                        │
│                   (FastAPI / Flask with async)                     │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              API Layer (FastAPI Routes)                    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Auth         │  │ Upload       │  │ Analytics    │    │   │
│  │  │ Endpoints    │  │ Endpoints    │  │ Endpoints    │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Dashboard    │  │ Chat         │  │ Billing      │    │   │
│  │  │ Endpoints    │  │ Endpoints    │  │ Endpoints    │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │           Business Logic Services Layer                    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Auth Service │  │ Dataset      │  │ Data         │    │   │
│  │  │              │  │ Service      │  │ Cleaning     │    │   │
│  │  └──────────────┘  └──────────────┘  │ Service      │    │   │
│  │  ┌──────────────┐  ┌──────────────┐  └──────────────┘    │   │
│  │  │ Dashboard    │  │ Quality      │  ┌──────────────┐    │   │
│  │  │ Service      │  │ Service      │  │ Insights     │    │   │
│  │  └──────────────┘  └──────────────┘  │ Service (ML) │    │   │
│  │  ┌──────────────┐  ┌──────────────┐  └──────────────┘    │   │
│  │  │ Chat Service │  │ Forecast     │  ┌──────────────┐    │   │
│  │  │ (LLM)        │  │ Service (ML) │  │ Recommend    │    │   │
│  │  └──────────────┘  │              │  │ Service (ML) │    │   │
│  │                    └──────────────┘  └──────────────┘    │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │         Data Access Layer (ORM/Repository)                 │   │
│  │    (SQLAlchemy ORM, Database queries, SQL operations)      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │         Background Job Processing (APScheduler/Celery)    │   │
│  │    (Async data processing, scheduled tasks, webhooks)      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              Middleware & Utilities                        │   │
│  │   (Logging, Error Handling, Rate Limiting, CORS, etc)     │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────┬──────────────────────────────────────────────────────────┘
         │
         └────┬─────────────┬──────────────┬────────────────┐
              │             │              │                │
        ┌─────▼────┐  ┌─────▼────┐  ┌────▼─────┐  ┌─────▼─────┐
        │PostgreSQL│  │  Redis   │  │ File     │  │External   │
        │Database  │  │  Cache   │  │ Storage  │  │Services   │
        └──────────┘  └──────────┘  └─────────┘  └───────────┘
                      (Session &         (S3/Azure)  (Stripe,
                       Computed         (Local Dev)   SendGrid,
                       Metrics)                       Payment)
```

---

## 🔑 Architecture Principles

1. **Monolithic Backend** - Single Python application with clear separation of concerns
2. **Layered Architecture** - API → Services → Data Access
3. **No Microservices** - All features in one deployable unit
4. **No Docker Locally** - Run services directly on machine
5. **Next.js Frontend** - Server-side rendering + API calls
6. **Async Processing** - Background jobs for long-running tasks
7. **Environment Separation** - Development, Testing, Staging, Production

---

## 📁 Project Structure

```
insightsforge/
├── frontend/                          # Next.js Application
│   ├── src/
│   │   ├── app/                       # Next.js 14+ app directory
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── (auth)/                # Auth routes group
│   │   │   │   ├── login/page.tsx
│   │   │   │   ├── signup/page.tsx
│   │   │   │   └── forgot-password/page.tsx
│   │   │   ├── (dashboard)/           # Protected routes group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx           # Main dashboard
│   │   │   │   ├── datasets/
│   │   │   │   ├── datasets/[id]/
│   │   │   │   │   ├── page.tsx       # Dataset overview
│   │   │   │   │   ├── quality/page.tsx
│   │   │   │   │   ├── analytics/page.tsx
│   │   │   │   │   ├── chat/page.tsx
│   │   │   │   │   ├── insights/page.tsx
│   │   │   │   │   ├── forecast/page.tsx
│   │   │   │   │   └── recommendations/page.tsx
│   │   │   │   ├── settings/
│   │   │   │   └── billing/
│   │   │   └── api/                   # API routes (optional)
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── SignupForm.tsx
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── DashboardLayout.tsx
│   │   │   │   ├── ChartCard.tsx
│   │   │   │   └── MetricsGrid.tsx
│   │   │   ├── upload/
│   │   │   │   ├── FileUploader.tsx
│   │   │   │   └── UploadProgress.tsx
│   │   │   └── chat/
│   │   │       ├── ChatInterface.tsx
│   │   │       └── MessageBubble.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useDataset.ts
│   │   │   └── useChat.ts
│   │   ├── lib/
│   │   │   ├── api-client.ts
│   │   │   ├── auth.ts
│   │   │   └── utils.ts
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── styles/
│   │   │   └── globals.css
│   │   └── types/
│   │       └── index.ts
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── .env.local (local only, not in git)
│
├── backend/                           # Python FastAPI Monolith
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # Application entry point
│   │   ├── config.py                  # Configuration management
│   │   ├── dependencies.py            # Dependency injection
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py          # API router aggregator
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auth.py        # Auth routes
│   │   │   │   │   ├── datasets.py    # Dataset routes
│   │   │   │   │   ├── dashboards.py  # Dashboard routes
│   │   │   │   │   ├── chat.py        # Chat routes
│   │   │   │   │   ├── insights.py    # Insights routes
│   │   │   │   │   ├── forecast.py    # Forecast routes
│   │   │   │   │   ├── billing.py     # Billing routes
│   │   │   │   │   └── admin.py       # Admin routes
│   │   │   │   └── schemas/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── auth.py
│   │   │   │       ├── dataset.py
│   │   │   │       ├── dashboard.py
│   │   │   │       └── shared.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py        # Auth business logic
│   │   │   ├── dataset_service.py     # Dataset operations
│   │   │   ├── data_cleaning.py       # Data cleaning logic
│   │   │   ├── quality_service.py     # Quality assessment
│   │   │   ├── dashboard_service.py   # Dashboard generation
│   │   │   ├── insights_service.py    # Insights analysis (ML)
│   │   │   ├── forecast_service.py    # Forecasting (ML)
│   │   │   ├── recommendations.py     # Recommendations (ML)
│   │   │   ├── chat_service.py        # AI chat/LLM integration
│   │   │   ├── billing_service.py     # Billing logic
│   │   │   ├── file_service.py        # File upload/storage
│   │   │   └── email_service.py       # Email notifications
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User ORM model
│   │   │   ├── dataset.py             # Dataset ORM model
│   │   │   ├── dashboard.py           # Dashboard ORM model
│   │   │   ├── insight.py             # Insight ORM model
│   │   │   ├── forecast.py            # Forecast ORM model
│   │   │   ├── subscription.py        # Subscription ORM model
│   │   │   └── base.py                # Base ORM model
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── session.py             # Database session management
│   │   │   ├── base.py                # Base model for all tables
│   │   │   └── migrations/            # Alembic migrations folder
│   │   │       ├── env.py
│   │   │       ├── script.py.mako
│   │   │       └── versions/
│   │   │           └── (migration files)
│   │   │
│   │   ├── ml_models/
│   │   │   ├── __init__.py
│   │   │   ├── forecasting/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── prophet_model.py
│   │   │   │   └── arima_model.py
│   │   │   ├── insights/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── anomaly_detection.py
│   │   │   │   └── trend_analysis.py
│   │   │   └── recommendations/
│   │   │       ├── __init__.py
│   │   │       └── rule_engine.py
│   │   │
│   │   ├── tasks/                     # Background jobs (APScheduler/Celery)
│   │   │   ├── __init__.py
│   │   │   ├── data_processing.py
│   │   │   ├── scheduled.py           # Scheduled tasks
│   │   │   └── webhooks.py
│   │   │
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # JWT verification
│   │   │   ├── error_handler.py       # Global error handling
│   │   │   ├── rate_limiter.py        # Rate limiting
│   │   │   └── logging.py             # Request logging
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── security.py            # Password hashing, JWT
│   │   │   ├── validators.py          # Data validation
│   │   │   ├── formatters.py          # Data formatting
│   │   │   └── constants.py
│   │   │
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── settings.py            # Environment settings
│   │       └── security.py            # Security utilities
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                # Pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_datasets.py
│   │   ├── test_data_cleaning.py
│   │   ├── test_insights.py
│   │   ├── test_forecast.py
│   │   ├── integration_tests/
│   │   └── fixtures/
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── .env.development (local only, not in git)
│   ├── .env.testing (local only, not in git)
│   ├── .env.staging
│   ├── .env.production
│   ├── wsgi.py                        # WSGI entry point for production
│   ├── asgi.py                        # ASGI entry point (for async workers)
│   ├── Dockerfile                     # Docker for CI/CD pipelines only
│   └── pytest.ini
│
├── docker/                            # Docker files for CI/CD only
│   ├── Dockerfile.backend             # Python backend
│   ├── Dockerfile.frontend            # Next.js frontend
│   └── docker-compose.ci.yml          # CI/CD pipeline only
│
├── .github/
│   └── workflows/
│       ├── test.yml                   # Run tests
│       ├── build.yml                  # Build images
│       ├── deploy-staging.yml         # Deploy to staging
│       └── deploy-production.yml      # Deploy to production
│
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

---

## 🛠️ Development Setup (Local Machine)

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Git

### **Backend Setup**

1. **Clone & Navigate**
```bash
git clone <repo>
cd backend
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements-dev.txt
```

4. **Configure Local Database**
- PostgreSQL running locally on default port 5432
- Create database: `createdb insightsforge_dev`
- Set connection string in `.env.development`

5. **Initialize Database**
```bash
# Run Alembic migrations
alembic upgrade head
```

6. **Run Backend**
```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# OR with Gunicorn + multiple workers (production-like)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --reload
```

### **Frontend Setup**

1. **Clone & Navigate**
```bash
cd frontend
```

2. **Install Dependencies**
```bash
npm install
# or
yarn install
```

3. **Configure Environment**
```
# .env.local (not in git)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

4. **Run Frontend**
```bash
npm run dev
# Runs on http://localhost:3000
```

### **Database Setup (Local)**

Create three separate databases:

```bash
# Development Database
createdb insightsforge_dev

# Testing Database (recreated each test run)
createdb insightsforge_test

# Optional: Staging Database
createdb insightsforge_staging
```

**PostgreSQL Connection Strings:**
```
Development: postgresql://username:password@localhost:5432/insightsforge_dev
Testing:     postgresql://username:password@localhost:5432/insightsforge_test
Staging:     postgresql://username:password@localhost:5432/insightsforge_staging
Production:  Managed RDS (AWS/Azure)
```

### **Redis Setup (Local)**

```bash
# Install Redis (if not installed)
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server
# Windows: Use Windows Subsystem for Linux or Redis for Windows

# Start Redis
redis-server

# Test connection
redis-cli ping  # Should return "PONG"
```

---

## 🗄️ Database Configuration

### **Development (Local)**
```
Database: PostgreSQL (local instance)
Port: 5432
Database Name: insightsforge_dev
Backup: None (local development)
Connection: Direct local connection
Migrations: Manual (alembic upgrade head)
```

### **Testing (Local)**
```
Database: SQLite (in-memory for speed, or fresh PostgreSQL)
Database Name: insightsforge_test
Backup: None (recreated each test run)
Connection: Pytest fixtures in conftest.py
Migrations: Automatic (creates fresh schema)
Isolation: Each test gets a clean database
```

### **Staging (AWS/Azure)**
```
Database: AWS RDS PostgreSQL 14 (or Azure Database for PostgreSQL)
Instance Type: db.t3.small (for staging)
Backup: Daily (7-day retention)
Multi-AZ: No (staging doesn't need HA)
Replicas: None
Connection: SSL/TLS encrypted
Migrations: Automated via CI/CD pipeline
Database Name: insightsforge_staging
```

### **Production (AWS/Azure)**
```
Database: AWS RDS PostgreSQL 14 (or Azure Database for PostgreSQL)
Instance Type: db.t3.medium or larger
Backup: Continuous (35-day retention)
Multi-AZ: Yes (High Availability)
Read Replicas: Yes (for analytics)
Connection: SSL/TLS encrypted + IAM authentication
Migrations: Blue-green deployment
Database Name: insightsforge_prod
```

### **All Environments: Required Tables**
- Users
- Businesses
- Datasets
- Dashboards
- Charts
- Insights
- Forecasts
- Recommendations
- Subscriptions
- Audit Logs
- Sessions (for Redis/PostgreSQL)

---

## 🔄 Environment Separation

### **1. Development Environment**

**Purpose:** Local development by engineers

**Configuration:**
```python
# .env.development
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://user:password@localhost:5432/insightsforge_dev
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-not-for-production
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
JWT_EXPIRATION_HOURS=24
FILE_UPLOAD_DIR=./uploads/dev
MAX_FILE_SIZE_MB=500
STRIPE_API_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
AWS_S3_BUCKET=insightsforge-dev
ENABLE_API_DOCS=true
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW_SECONDS=60
```

**Characteristics:**
- Hot reload enabled
- Full logging and debugging
- Swagger/OpenAPI docs at /docs
- No rate limiting (or very high)
- Small file upload limits okay
- Test data seeding scripts

---

### **2. Testing Environment**

**Purpose:** Automated testing (unit, integration)

**Configuration:**
```python
# .env.testing (pytest auto-loads)
ENVIRONMENT=testing
DEBUG=True
LOG_LEVEL=WARNING
DATABASE_URL=sqlite:///test.db  # or postgresql://...
REDIS_URL=redis://localhost:6379/1  # Different Redis DB
SECRET_KEY=test-secret-key-change-me
CORS_ORIGINS=["*"]
JWT_EXPIRATION_HOURS=1
FILE_UPLOAD_DIR=./uploads/test
MAX_FILE_SIZE_MB=50
STRIPE_API_KEY=sk_test_...
AWS_S3_BUCKET=insightsforge-test
ENABLE_API_DOCS=false
RATE_LIMIT_REQUESTS=10000
RATE_LIMIT_WINDOW_SECONDS=60
```

**Characteristics:**
- Separate database (SQLite or fresh PostgreSQL)
- Fast in-memory Redis
- Test data factories
- Mocked external services (Stripe, S3)
- No file I/O (use temp directories)
- Runs in CI/CD pipeline

---

### **3. Staging Environment**

**Purpose:** Pre-production testing

**Configuration:**
```python
# .env.staging
ENVIRONMENT=staging
DEBUG=False
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:password@insightsforge-staging.rds.amazonaws.com:5432/insightsforge_staging
REDIS_URL=redis://insightsforge-staging-cache.xxxxx.ng.0001.use1.cache.amazonaws.com:6379
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=["https://staging.insightsforge.io"]
JWT_EXPIRATION_HOURS=12
FILE_UPLOAD_DIR=/var/uploads/staging
MAX_FILE_SIZE_MB=500
STRIPE_API_KEY=sk_test_...
AWS_S3_BUCKET=insightsforge-staging
ENABLE_API_DOCS=false
RATE_LIMIT_REQUESTS=500
RATE_LIMIT_WINDOW_SECONDS=60
```

**Characteristics:**
- Cloud database (RDS/Azure)
- Cloud cache (ElastiCache/Redis)
- Real payment processing (test mode)
- Real file storage (S3)
- Automated deployments from main branch
- Real SSL certificates
- Performance monitoring enabled

---

### **4. Production Environment**

**Purpose:** Live customer environment

**Configuration:**
```python
# .env.production (AWS Secrets Manager or Azure Key Vault)
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://user:password@insightsforge-prod.rds.amazonaws.com:5432/insightsforge_prod
REDIS_URL=redis://insightsforge-prod-cache.xxxxx.ng.0001.use1.cache.amazonaws.com:6379
SECRET_KEY=<highly-secure-key-from-secrets-manager>
CORS_ORIGINS=["https://insightsforge.io", "https://www.insightsforge.io"]
JWT_EXPIRATION_HOURS=8
FILE_UPLOAD_DIR=/var/uploads/prod
MAX_FILE_SIZE_MB=500
STRIPE_API_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_live_...
AWS_S3_BUCKET=insightsforge-prod
ENABLE_API_DOCS=false
RATE_LIMIT_REQUESTS=200
RATE_LIMIT_WINDOW_SECONDS=60
EMAIL_SMTP_SERVER=smtp.sendgrid.net
EMAIL_SMTP_PORT=587
DATADOG_API_KEY=<monitoring-key>
NEW_RELIC_LICENSE_KEY=<apm-key>
```

**Characteristics:**
- No debugging enabled
- Minimal logging (only errors/warnings)
- Cloud database with backups
- Cloud cache with clustering
- Real payment processing
- CDN for static assets
- WAF protection
- DDoS protection
- SSL/TLS enforced
- APM monitoring
- Error tracking (Sentry)
- Multi-region failover ready

---

## 🌳 Git Branching Strategy (Git Flow)

### **Branch Types**

```
main (production)
  └── Protected branch
      └── Only receives merges from release-* and hotfix-* branches
      └── Auto-deploys to production

develop (development)
  └── Integration branch
      └── Receives feature merges
      └── Auto-deploys to staging

feature/* (feature branches)
  └── Created from: develop
  └── Naming: feature/user-authentication, feature/data-cleaning-engine
  └── Merged back to: develop via Pull Request
  └── Deleted after merge

release/* (release branches)
  └── Created from: develop
  └── Naming: release/v1.0.0, release/v1.1.0
  └── Merged to: main AND back to develop
  └── Auto-deploys to production

hotfix/* (hotfix branches)
  └── Created from: main
  └── Naming: hotfix/critical-bug, hotfix/payment-issue
  └── Merged to: main AND develop
  └── Auto-deploys to production immediately
```

### **Branch Workflow**

**Starting a Feature:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/dashboard-improvements
```

**Committing & Pushing:**
```bash
git add .
git commit -m "feat: add interactive dashboard filters"
git push origin feature/dashboard-improvements
```

**Creating Pull Request:**
- Push to GitHub
- Create PR against `develop` branch
- Request code review
- Pass CI/CD checks (tests, linting)
- 2 approvals required
- Merge via "Squash and merge" for clean history

**Merging Feature:**
```bash
# After PR approval in GitHub UI
# Use "Squash and merge" to keep history clean
```

**Creating Release:**
```bash
# When ready to release
git checkout -b release/v1.0.0 develop
# Bump version in package.json, requirements.txt, etc.
git commit -am "chore: bump version to v1.0.0"
git push origin release/v1.0.0

# Create PR against main and develop
# After approval:
git checkout main
git merge --no-ff release/v1.0.0
git tag v1.0.0
git push origin main --tags

git checkout develop
git merge --no-ff release/v1.0.0
git push origin develop

# Delete release branch
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

**Hotfix (Critical Bug):**
```bash
git checkout -b hotfix/security-issue main
# Fix the bug
git commit -am "fix: security vulnerability in auth"
git push origin hotfix/security-issue

# Create PR to main, get approved, merge
git checkout main
git merge --no-ff hotfix/security-issue
git tag v1.0.1
git push origin main --tags

# Also merge back to develop
git checkout develop
git merge --no-ff hotfix/security-issue
git push origin develop

git branch -d hotfix/security-issue
git push origin --delete hotfix/security-issue
```

### **Branching Rules (GitHub)**

**Main Branch Protection:**
```
✓ Require pull request reviews before merging (2 approvals)
✓ Require status checks to pass (CI/CD pipeline)
✓ Require branches to be up to date before merging
✓ Include administrators in restrictions
✓ Dismiss stale PR approvals when new commits pushed
✓ Require code owner reviews
✓ Auto-delete head branches after merge
```

**Develop Branch Protection:**
```
✓ Require pull request reviews before merging (1 approval)
✓ Require status checks to pass
✓ Require branches to be up to date
✓ Auto-delete head branches
```

---

## 🚀 Deployment Strategy

### **Development (Local)**
```
No deployment - runs on developer machine
Database: Local PostgreSQL
Cache: Local Redis
Frontend: http://localhost:3000
Backend: http://localhost:8000
```

### **Staging (AWS/Azure)**
```
Trigger: Push to develop branch
Pipeline: GitHub Actions
Steps:
  1. Run tests
  2. Build backend Docker image
  3. Build frontend (Next.js)
  4. Push images to registry
  5. Deploy to staging infrastructure
  6. Run smoke tests
  7. Notify team

Frontend: https://staging.insightsforge.io
Backend: https://api-staging.insightsforge.io
Database: AWS RDS (staging)
Cache: AWS ElastiCache (staging)
```

### **Production (AWS/Azure)**
```
Trigger: Create release tag (v*.*.*)
Pipeline: GitHub Actions
Steps:
  1. Run full test suite
  2. Build backend Docker image
  3. Build frontend (Next.js)
  4. Push images to registry
  5. Blue-green deployment (old + new versions)
  6. Run smoke tests
  7. If all pass: Switch traffic to new version
  8. If fails: Rollback to old version
  9. Notify team

Frontend: https://insightsforge.io
Backend: https://api.insightsforge.io
Database: AWS RDS (production, Multi-AZ)
Cache: AWS ElastiCache (production, clustered)
```

---

## 🧪 Testing Strategy

### **Unit Tests (Backend)**
```
Location: backend/tests/test_*.py
Framework: pytest
Commands:
  pytest tests/
  pytest tests/ -v  (verbose)
  pytest tests/ --cov  (with coverage)
  pytest tests/test_auth.py::test_user_login  (single test)
```

### **Integration Tests (Backend)**
```
Location: backend/tests/integration_tests/
Focus: Service interactions, database operations
Database: SQLite or separate test DB
Commands:
  pytest tests/integration_tests/
```

### **E2E Tests (Frontend + Backend)**
```
Tool: Cypress or Playwright
Location: frontend/e2e/
Scenarios:
  - User signup → Login → Upload → View Dashboard
  - File validation → Data cleaning → Results
  - Chat queries → Get answers

Commands:
  npm run e2e
  npm run e2e:headed
```

### **Test Coverage Requirements**
```
Backend: ≥ 80% coverage
Frontend: ≥ 70% coverage
Critical paths: 100% coverage
```

### **Test Configuration Files**
```python
# backend/pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests

# backend/conftest.py
import pytest
from app.database import Base, engine

@pytest.fixture
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    # ... return connection
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    """Create test client"""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)
```

---

## 📊 Application Configuration (config.py)

```python
# backend/app/config.py
import os
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings:
    # Environment
    ENVIRONMENT: Environment = Environment(os.getenv("ENVIRONMENT", "development"))
    DEBUG: bool = ENVIRONMENT == Environment.DEVELOPMENT
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/insightsforge_dev"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    if ENVIRONMENT == Environment.STAGING:
        CORS_ORIGINS = ["https://staging.insightsforge.io"]
    elif ENVIRONMENT == Environment.PRODUCTION:
        CORS_ORIGINS = ["https://insightsforge.io", "https://www.insightsforge.io"]
    
    # File Upload
    FILE_UPLOAD_DIR: str = os.getenv("FILE_UPLOAD_DIR", "./uploads/dev")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "500"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG" if DEBUG else "INFO")
    
    # Feature Flags
    ENABLE_API_DOCS: bool = ENVIRONMENT in [Environment.DEVELOPMENT, Environment.TESTING]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "1000"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

settings = Settings()
```

---

## 🔄 Running Services Locally

### **Terminal 1: Backend**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### **Terminal 2: Frontend**
```bash
cd frontend
npm run dev
# Access at http://localhost:3000
```

### **Terminal 3: Redis**
```bash
redis-server
```

### **Terminal 4: Background Jobs (Optional)**
```bash
cd backend
source venv/bin/activate
python -m app.tasks.worker  # If using Celery/APScheduler
```

---

## 📦 Dependencies

### **Backend (Python)**
```
# requirements.txt
FastAPI==0.104.0
uvicorn[standard]==0.24.0
SQLAlchemy==2.0.0
psycopg2-binary==2.9.0
pydantic==2.0.0
pydantic-settings==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.0
python-multipart==0.0.6
redis==5.0.0
aioredis==2.0.0
Pillow==10.0.0
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
pystan==2.19.0
prophet==1.1.0
statsmodels==0.14.0
requests==2.31.0
httpx==0.24.0
python-dotenv==1.0.0
gunicorn==21.0.0
alembic==1.12.0
email-validator==2.0.0
```

### **Frontend (Node.js)**
```
"dependencies": {
  "next": "^14.0.0",
  "react": "^18.0.0",
  "react-dom": "^18.0.0",
  "typescript": "^5.0.0",
  "tailwindcss": "^3.3.0",
  "recharts": "^2.10.0",
  "axios": "^1.5.0",
  "react-hook-form": "^7.48.0",
  "zod": "^3.22.0"
}
```

---

## 🛡️ Security Checklist

- [ ] Secrets stored in environment variables (not in code)
- [ ] Database credentials never in git
- [ ] JWT secrets strong (≥32 characters)
- [ ] HTTPS/SSL enforced in production
- [ ] CORS properly configured per environment
- [ ] Rate limiting enabled
- [ ] SQL injection prevention (ORM usage)
- [ ] XSS protection (React auto-escaping)
- [ ] CSRF tokens on state-changing operations
- [ ] Input validation on all endpoints
- [ ] Audit logging for sensitive actions
- [ ] Regular security updates for dependencies

---

## 📋 Summary

| Component | Development | Testing | Staging | Production |
|-----------|------------|---------|---------|-----------|
| Frontend | localhost:3000 | N/A | staging.* | insightsforge.io |
| Backend | localhost:8000 | pytest | api-staging.* | api.insightsforge.io |
| Database | PostgreSQL local | SQLite/PG | AWS RDS | AWS RDS Multi-AZ |
| Cache | Redis local | Redis local | AWS ElastiCache | AWS ElastiCache Cluster |
| Deployment | Manual (none) | CI/CD test | Auto (develop) | Manual (release tag) |
| Scaling | Single machine | N/A | Small | Medium+ |
| SSL | No | N/A | Yes | Yes |

This architecture is production-ready, scalable, and maintainable!
