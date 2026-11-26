# ChefDate

ChefDate runs locally with a Django 5.2 booking API and a React/Vite request form. See [CONTRIBUTING.md](CONTRIBUTING.md) for the shared development branch and team setup.

## Run locally on Windows

You need Python 3.14 or later, `uv`, and Node.js 20.19 or later in the 20.x series or Node.js 22.12 or later. To install `uv`, run the following command in PowerShell. Open a new terminal if PowerShell still doesn’t recognize `uv` after installation.

```powershell
winget install --id=astral-sh.uv -e
```

### Prepare the local SQLite database

Run this from the repository root in a checkout configured for local SQLite. The migration command creates `backend/db.sqlite3` if needed and applies pending migrations to it.

```powershell
# Enter the backend directory, where manage.py is located.
Set-Location .\backend

# Stop if the shell or checkout could select a configured PostgreSQL database.
if ((Test-Path Env:DATABASE_URL) -or (Test-Path -LiteralPath .env)) {
    throw 'A database configuration is present. Use the Neon setup below or a fresh checkout for SQLite.'
}

# Install the locked dependencies and check the Django configuration.
uv sync --locked
if ($LASTEXITCODE -ne 0) { throw 'Backend dependency setup failed.' }
uv run --locked python manage.py check --settings=config.settings
if ($LASTEXITCODE -ne 0) { throw 'Django configuration check failed.' }

# Create the local SQLite file and apply the schema migrations.
uv run --locked python manage.py migrate --settings=config.settings
if ($LASTEXITCODE -ne 0) { throw 'Local SQLite migration failed.' }

# Optional: Uncomment to add six cuisines and eighteen fictional chefs after migration.
# uv run --locked python manage.py seed_demo_catalog --settings=config.settings
```

To verify migration and seeding with a temporary database, run this PowerShell block from `backend/`. The `config.settings_test` settings select in-memory SQLite. Both operations run in one Django process so the seed can use the tables created by the migrations. The database is discarded when the process exits.

```powershell
$chefDateCatalogSmokeTest = @'
from django.core.management import call_command

# Create the tables in the in-memory SQLite database.
call_command('migrate', interactive=False)

# Populate the tables with fictional demo records.
call_command('seed_demo_catalog')
'@
uv run --locked python manage.py shell --settings=config.settings_test --command $chefDateCatalogSmokeTest
```

### Start the backend

After preparing the local database, start Django from `backend/`.

```powershell
uv run --locked python manage.py runserver 127.0.0.1:8000 --settings=config.settings
```

### Start the frontend

In another PowerShell terminal at the repository root, install the locked frontend dependencies and start Vite.

```powershell
Set-Location .\frontend
npm.cmd ci
npm.cmd run dev
```

Open the [booking form](http://127.0.0.1:5173/). To review a synthetic booking, create a local development account with `uv run python manage.py createsuperuser` from `backend/` and sign in to [Django Admin](http://127.0.0.1:8000/admin/).

Django generates a temporary secret key for each process during local development. If you need a stable key across restarts, set `DJANGO_SECRET_KEY` in your environment and keep the value private.

## Use Neon PostgreSQL locally

From `backend/`, run `Copy-Item .env.example .env` if `.env` does not already exist. Replace the example `DATABASE_URL` with the direct connection URL for your Neon development branch. Git ignores `.env`. A `DATABASE_URL` set in the process environment takes precedence over the file. Django verifies the server’s TLS certificate and hostname.

Once Django is configured for your development branch, apply and list the initial migrations from `backend/`.

```powershell
uv run python manage.py migrate
uv run python manage.py showmigrations
```

## Change history

See [UPDATES.md](UPDATES.md) for changes, verification results, and pending work.

## Security

Follow [SECURITY_RULES.md](SECURITY_RULES.md) when working on ChefDate.
