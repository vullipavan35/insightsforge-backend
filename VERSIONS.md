# InsightForge Backend - Version Specification (VERSIONS.md)

> **Purpose**: Single source of truth for runtime engines, framework versions, database specifications, and dependencies for the `insightsforge-backend` repository.

---

## 1. Runtime & Language Environment

| Component | Target Version | Status / Notes |
|---|---|---|
| **Python Runtime** | `3.12+` / `3.14.x` | Active system engine |
| **Package Management** | `pip` / `requirements.txt` / `pyproject.toml` | Pinned dependencies with hashes |
| **ASGI Web Server** | `uvicorn 0.24.x` / `gunicorn 21.x` | High-performance async server |

---

## 2. Core Framework & Database Stack

| Layer | Package | Target Version | Rationale & Rules |
|---|---|---|---|
| **Web Framework** | `fastapi` | `^0.104.0` | Async request handling, OpenAPI auto-generation |
| **Validation Engine** | `pydantic` & `pydantic-settings` | `^2.5.0` | Schema validation and typed environment management |
| **ORM & Database** | `sqlalchemy` | `^2.0.0` | Declarative 2.0 style ORM mapping |
| **PostgreSQL Driver** | `psycopg2-binary` | `^2.9.9` | High-performance synchronous/pooled driver |
| **Database Migrations** | `alembic` | `^1.13.0` | Declarative revision-based schema migrations |
| **Cache & Sessions** | `redis` & `aioredis` | `^5.0.0` | Distributed caching and async pub/sub |

---

## 3. Machine Learning & Analytics Libraries

| Purpose | Package | Target Version | Usage |
|---|---|---|---|
| **DataFrames & Arrays** | `pandas`, `numpy` | `^2.1.0` / `^1.26.0` | Data manipulation, cleaning, aggregations |
| **Forecasting Engines** | `prophet`, `statsmodels` | `^1.1.5` / `^0.14.0` | Additive time-series and ARIMA forecasting |
| **Anomaly Detection** | `scikit-learn` | `^1.3.0` | IsolationForest anomaly detection algorithms |
| **File Formats** | `openpyxl`, `pyarrow`, `python-multipart` | Latest | Multipart CSV, Excel, and JSON streaming |

---

## 4. Authentication & Security

| Tool | Package | Target Version | Usage |
|---|---|---|---|
| **Password Hashing** | `passlib[bcrypt]` / `bcrypt` | `^1.7.4` / `^4.0.0` | Secure one-way hashing |
| **JWT Tokens** | `python-jose[cryptography]` | `^3.3.0` | HS256 / RS256 token generation and verification |
| **CORS & Rate Limits** | `fastapi.middleware.cors` | Built-in | Security policy enforcement |

---

## 5. Environments & Database Infrastructure

| Profile / Environment | Database Engine | Host / Provider | Cache Layer | Backend Profile File |
|---|---|---|---|---|
| **Development** (`dev`) | PostgreSQL 18+ | Local (`insightsforge_dev` on `:5432`) | Local Redis (`:6379/0`) | `.env.development` |
| **Testing / CI** (`test`) | Ephemeral PostgreSQL / SQLite | In-Memory / Local (`insightsforge_test`) | Redis (`:6379/1`) / Mock | `.env.testing` |
| **Staging** (`staging`) | Managed PostgreSQL 15+ | Supabase Staging Project | Supabase / Upstash Redis | `.env.staging` |
| **Production** (`prod`) | Managed PostgreSQL 15+ | **Supabase Production** (Supavisor pooled port `6543`, SSL) | Managed Redis Cluster | `.env.production` |
