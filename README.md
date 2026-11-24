# ChefDate

ChefDate runs locally with a Django 5.2 booking API and a React/Vite request form. See [CONTRIBUTING.md](CONTRIBUTING.md) for the Sprint One checkout and team setup.

## Run locally on Windows

You need Python 3.14 or later, `uv`, and Node.js 20.19 or later in the 20.x series or Node.js 22.12 or later. To install `uv`, run the following command in PowerShell. Open a new terminal if PowerShell still doesn’t recognize `uv` after installation.

```powershell
winget install --id=astral-sh.uv -e
```

For a local SQLite checkout, run this from the repository root. The check stops the setup if a database URL or local environment file is present.

```powershell
Set-Location .\backend
if ((Test-Path Env:DATABASE_URL) -or (Test-Path -LiteralPath .env)) {
    throw 'A database configuration is present. Use the Neon setup below or a fresh checkout for SQLite.'
}
uv sync --locked
uv run python manage.py check
uv run python manage.py migrate
uv run python manage.py runserver 127.0.0.1:8000
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
