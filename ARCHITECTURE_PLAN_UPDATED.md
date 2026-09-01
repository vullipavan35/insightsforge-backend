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

### **Staging (Supabase / Cloud)**
```
Database: Supabase Managed PostgreSQL 15+
Connection: Supavisor Transaction Pooler (Port 6543) / Direct (Port 5432)
Backup: Daily automated backups
SSL/TLS: Enforced (SSL mode require)
Migrations: Automated via CI/CD pipeline
```

### **Production (Supabase Managed PostgreSQL)**
```
Database: Supabase Managed PostgreSQL 15+ (Production)
Connection: Supavisor Transaction Pooler (Port 6543) with SSL
Backup: Point-in-time recovery & continuous backups
SSL/TLS: Enforced
High Availability: Supabase managed enterprise HA
Migrations: Zero-downtime backward-compatible migrations via CI/CD
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
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
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
- Managed Supabase PostgreSQL (with Supavisor connection pooling)
- Cloud cache (ElastiCache/Redis)
- Real payment processing (test mode)
- Real file storage (S3 / Supabase Storage)
- Automated deployments from main branch
- Real SSL certificates
- Performance monitoring enabled

---

### **4. Production Environment**

**Purpose:** Live customer environment

**Configuration:**
```python
# .env.production (AWS Secrets Manager or Azure Key Vault / Supabase)
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
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

## 🌳 Git Branching Strategy (GitHub Flow / Trunk-Based)

### **1. Branch Topology & Architecture**

```
main ──────────●───────────────────●───────────────────●─────── (Deploy to Production)
               │                  ▲                   ▲
               │ (branch)         │ (PR / Merge)      │
feat/auth ─────┴──────●───────●────┘                   │
                                                       │
feat/dataset-upload ─────────────────●──────────●──────┘
```

#### **Primary Branch**
* **`main`**:
  * The single source of truth; always deployable and protected.
  * Direct commits are prohibited; all changes land via reviewed Pull Requests.
  * Connected to automated CI/CD pipelines and preview verification.

#### **Ephemeral Branches (Short-Lived Feature Branches)**
* Feature branches are branched off `main` and merged back into `main` after automated checks and validation pass.
* Lifespan: ideally **1–2 days max** per branch to avoid drift and merge conflicts.

---

### **2. Standard Branch Naming Conventions**

All branch names follow `<type>/<scope>-<short-description>` using kebab-case:

| Type | Purpose | Example |
|---|---|---|
| `feat/` | New UI component, page, or feature | `feat/dataset-uploader`, `feat/chat-stream` |
| `fix/` | Bug fixes or patch releases | `fix/auth-token-refresh`, `fix/table-virtual-scroll` |
| `refactor/` | Code structure improvements without feature change | `refactor/api-client-interceptor` |
| `perf/` | Performance optimizations | `perf/chart-render-memoization` |
| `docs/` | Documentation or specifications update | `docs/update-frontend-spec` |
| `chore/` | Tooling, dependencies, or config updates | `chore/upgrade-tanstack-query` |

---

### **3. Phased Branching Execution Plan**

Short-lived feature branches mapped to roadmap milestones:

#### **Phase 1: Foundation & Authentication**
1. `feat/setup-design-system` — Next.js project init, Tailwind CSS, `shadcn/ui` base components, layout shell.
2. `feat/auth-session-flow` — API client wrapper, JWT interceptor, `AuthContext`, login/signup pages, middleware protection.

#### **Phase 2: Dataset Workspace**
3. `feat/dataset-ingestion` — File uploader (`react-dropzone`), upload progress, dataset listing page.
4. `feat/dataset-quality-preview` — Data health score card, column distribution badges, virtualized table preview.

#### **Phase 3: Analytics & Visualizations**
5. `feat/analytics-dashboard` — Metric KPI cards, Recharts time-series and anomaly charts, URL-synced date filter bar.

#### **Phase 4: Machine Learning & Forecasts**
6. `feat/ml-forecast-insights` — Forecast confidence band visualizer, anomaly feed, prescriptive recommendation cards.

#### **Phase 5: AI Chat Interface**
7. `feat/chat-streaming` — SSE / streaming chat interface, message history, dataset context selector chips.

#### **Phase 6: Billing & Account**
8. `feat/billing-settings` — Stripe customer portal redirection, quota usage gauges, user settings.

---

### **4. Commit Message Standard (Conventional Commits)**

Commit messages must follow the Conventional Commits specification:

```
<type>(<scope>): <short imperative summary>

[optional body]
```

* **Examples**:
  * `feat(auth): implement jwt refresh token interceptor in api-client`
  * `feat(datasets): add file dropzone with mime validation`
  * `fix(chat): handle empty token stream buffer on SSE disconnect`
  * `docs(spec): document query key tuple conventions`

---

### **5. Pull Request & Merge Policy**

1. **Rebase & Fast-Forward / Squash & Merge**:
   * Use **Squash and Merge** for clean, atomic history on `main`.
2. **Pre-Merge Validation**:
   * Type checking: `tsc --noEmit` must pass with 0 errors.
   * Linter: ESLint / Prettier check must be clean.
   * Build check: `next build` must compile successfully without warnings.
   * Automated tests must pass all test suites.

---

### **6. Branch Protection Rules (GitHub)**

**`main` Branch Protection:**
```
✓ Require pull request reviews before merging (1-2 approvals)
✓ Require status checks to pass (CI/CD pipeline: build, lint, test)
✓ Require branches to be up to date before merging
✓ Include administrators in restrictions
✓ Dismiss stale PR approvals when new commits pushed
✓ Require linear commit history (Squash and Merge)
✓ Auto-delete head branches after merge
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
```json
"dependencies": {
  "next": "16.3.4",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5.0.0",
  "tailwindcss": "4.3.3",
  "@tanstack/react-query": "5.102.8",
  "zustand": "5.0.5",
  "recharts": "3.10",
  "@tanstack/react-table": "^8.20.0",
  "axios": "^1.7.0",
  "react-hook-form": "^7.54.0",
  "zod": "^3.24.0",
  "lucide-react": "^1.0.0"
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
| Database | PostgreSQL local (:5432) | SQLite / Local PG | Supabase Staging | **Supabase Production** (SSL, Port 6543) |
| Cache | Redis local (:6379) | Redis local / Mock | Supabase / Redis Cloud | Managed Redis Cluster |
| Deployment | Manual (none) | CI/CD test | Auto (develop) | Manual (release tag) |
| Scaling | Single machine | N/A | Serverless / Cloud | High Availability Managed |
| SSL | No | N/A | Yes | Yes |

This architecture is production-ready, scalable, and maintainable!
