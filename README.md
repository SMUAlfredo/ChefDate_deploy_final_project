# ChefDate

ChefDate has a starter backend built with Django 5.2 for local development. The frontend and deployment are pending.

## Run locally on Windows

You need Python 3.14 or later and `uv`. To install `uv`, run the following command in PowerShell. Open a new terminal if PowerShell still doesn’t recognize `uv` after installation.

```powershell
winget install --id=astral-sh.uv -e
```

From the repository root, run the following commands. `uv sync --locked` sets up the virtual environment and installs the dependencies pinned in `backend/uv.lock`.

```powershell
Set-Location .\backend
uv sync --locked
uv run python manage.py check
uv run python manage.py runserver 127.0.0.1:8000
```

Open the [Django welcome page](http://127.0.0.1:8000/). When `DATABASE_URL` is unset and absent from `backend/.env`, Django uses local SQLite and may show a pending migrations warning.

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
