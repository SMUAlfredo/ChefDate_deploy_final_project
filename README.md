# ChefDate

ChefDate has a starter backend built with Django 5.2 for local development. The Neon PostgreSQL connection, database migrations, frontend, and deployment are pending.

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

Open the [Django welcome page](http://127.0.0.1:8000/). On startup, Django may create `backend/db.sqlite3` and warn about pending migrations. You can still open the welcome page. Run the migrations once the backend is connected to Neon PostgreSQL.

Django generates a temporary secret key for each process during local development. If you need a stable key across restarts, set `DJANGO_SECRET_KEY` in your environment and keep the value private.

## Change history

See [UPDATES.md](UPDATES.md) for changes, verification results, and pending work.
