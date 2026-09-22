# Online Shop Backend — Commands

## 1. Create project

```bash
mkdir online-shop-be
cd online-shop-be
```

## 2. Create virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
python -m pip install fastapi uvicorn sqlalchemy asyncpg alembic greenlet pydantic-settings python-dotenv pyjwt "pwdlib[argon2]" email-validator python-multipart
```

Save installed versions:

```bash
python -m pip freeze > requirements.txt
```

Install dependencies on another device:

```bash
python -m pip install -r requirements.txt
```

## 4. Create project folders

```bash
mkdir -p app/api/v1 app/core app/models app/repositories app/schemas app/services app/utils
```

Create Python package files:

```bash
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/repositories/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
```

Create main project files:

```bash
touch app/main.py
touch app/config.py
touch app/database.py
```

## 5. Run FastAPI

```bash
python -m uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

## 6. Check Python environment

```bash
which python
which pip
which uvicorn
```

Check FastAPI installation:

```bash
python -m pip show fastapi
```

Check FastAPI import:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

## 7. PostgreSQL

Create database:

```bash
createdb online_shop
```

Open PostgreSQL:

```bash
psql postgres
```

Show roles:

```sql
\du
```

Show databases:

```sql
\l
```

Show PostgreSQL port:

```sql
SHOW port;
```

Connect directly to the project database:

```bash
psql online_shop
```

Show tables:

```sql
\dt
```

Describe a table:

```sql
\d users
```

## 8. Environment variables

Create `.env`:

```bash
touch .env
```

Example:

```env
DATABASE_URL=postgresql+asyncpg://YOUR_USER:YOUR_PASSWORD@localhost:5432/online_shop
VERIFICATION_CODE_SECRET=change-this-to-a-long-random-secret
```

Create `.env.example`:

```bash
touch .env.example
```

Example:

```env
DATABASE_URL=
VERIFICATION_CODE_SECRET=
```

## 9. Git ignore

Create `.gitignore`:

```bash
touch .gitignore
```

Recommended content:

```text
.env
venv/
__pycache__/
.pytest_cache/
.idea/
.vscode/
```

## 10. Alembic setup

Initialize Alembic with async template:

```bash
python -m alembic init -t async migrations
```

Check Alembic database connection:

```bash
python -m alembic current
```

Show migration heads:

```bash
python -m alembic heads
```

Show migration history:

```bash
python -m alembic history
```

## 11. Check SQLAlchemy metadata

Check which tables SQLAlchemy currently knows about:

```bash
python -c "from app.database import Base; import app.models; print(Base.metadata.tables.keys())"
```

Expected example:

```text
dict_keys(['users', 'verification_codes'])
```

## 12. Create Alembic migration

Create users migration:

```bash
python -m alembic revision --autogenerate -m "create users table"
```

Create verification codes migration:

```bash
python -m alembic revision --autogenerate -m "create verification codes table"
```

Generic command:

```bash
python -m alembic revision --autogenerate -m "migration description"
```

## 13. Apply migrations

Apply all migrations:

```bash
python -m alembic upgrade head
```

Check current migration:

```bash
python -m alembic current
```

Rollback one migration:

```bash
python -m alembic downgrade -1
```

Rollback all migrations:

```bash
python -m alembic downgrade base
```

## 14. Useful Alembic commands

Show current revision:

```bash
python -m alembic current
```

Show migration history:

```bash
python -m alembic history
```

Show latest migration revision:

```bash
python -m alembic heads
```

Upgrade to latest:

```bash
python -m alembic upgrade head
```

Downgrade one migration:

```bash
python -m alembic downgrade -1
```

## 15. Development server

Run:

```bash
python -m uvicorn app.main:app --reload
```

Run on all network interfaces:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 16. Update dependencies after installing a package

Whenever you install something new:

```bash
python -m pip install PACKAGE_NAME
python -m pip freeze > requirements.txt
```

Example:

```bash
python -m pip install greenlet
python -m pip freeze > requirements.txt
```

## 17. Setup project on another device

Clone repository:

```bash
git clone YOUR_REPOSITORY_URL
cd online-shop-be
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create your `.env` file:

```bash
touch .env
```

Create PostgreSQL database:

```bash
createdb online_shop
```

Apply migrations:

```bash
python -m alembic upgrade head
```

Run backend:

```bash
python -m uvicorn app.main:app --reload
```

## 18. Current project API

Development Swagger:

```text
http://127.0.0.1:8000/docs
```

Current auth endpoints:

```text
POST /api/v1/auth/register
POST /api/v1/auth/verify-email
POST /api/v1/auth/resend-verification-code
```

## 19. Recommended daily workflow

Activate environment:

```bash
source venv/bin/activate
```

Start backend:

```bash
python -m uvicorn app.main:app --reload
```

After model changes:

```bash
python -m alembic revision --autogenerate -m "describe change"
```

Review the generated migration, then:

```bash
python -m alembic upgrade head
```

After adding a Python dependency:

```bash
python -m pip freeze > requirements.txt
```
