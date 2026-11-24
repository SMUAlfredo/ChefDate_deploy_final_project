# Contributing to ChefDate

These instructions use PowerShell on Windows. You need Git, access to the private ChefDate repository, and a Neon development branch for PostgreSQL work. Follow [SECURITY_RULES.md](SECURITY_RULES.md) and read [UPDATES.md](UPDATES.md) for recent changes. The [README](README.md) also covers a local SQLite setup.

## 1. Clone and open the project

Sign in to GitHub with the account that has repository access. For Sprint One, run these commands from the folder where you keep your projects.

```powershell
git clone --branch refactor/chefdate-structure https://github.com/SMUAlfredo/ChefDate_deploy_final_project.git
Set-Location .\ChefDate_deploy_final_project
```

If you cloned before the Git history cleanup, use a fresh clone for Sprint One and keep the older checkout until you have recovered any local work. Open the new checkout in your editor. The Django entry point is `backend/manage.py`.

## 2. Set up the backend

Install `uv` if PowerShell cannot find it. If it still isn't recognized after installation, reopen PowerShell and return to the repository root.

```powershell
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    winget install --id=astral-sh.uv -e
}
uv --version
```

The backend requires Python 3.14 or later. From the repository root, use `uv` to create the virtual environment and install the versions pinned in `backend/uv.lock`.

```powershell
Set-Location .\backend
uv sync --locked
```

If `uv` cannot find a compatible interpreter, run `uv python install 3.14` and retry `uv sync --locked`.

## 3. Configure a Neon development database

In the Neon Console, select the ChefDate project and click **Connect**. Select your development branch, database, and role. Turn off **Connection pooling** and copy the complete direct connection URL. Use a development branch for local work and apply schema changes with the team's development migration role. [Neon connection guide](https://neon.com/docs/connect/connect-from-any-app#get-a-connection-string-from-the-neon-console)

From `backend/`, create `.env` from the tracked example if it doesn't exist, then open it in VS Code.

```powershell
if (-not (Test-Path -LiteralPath .env)) {
    Copy-Item -LiteralPath .env.example -Destination .env
}
```

Open `backend/.env` in your editor, set `DATABASE_URL`, and save the file. Replace the entire fictitious value below with the URL you copied. Keep the actual URL and credentials out of commits, pull requests, and shared logs.

```dotenv
DATABASE_URL=postgresql://example_user:example_password@example.invalid/example_db?sslmode=verify-full
```

From `backend/`, confirm the first command reports an ignore rule and the second prints nothing. A `DATABASE_URL` defined in the PowerShell process takes precedence over `.env`. If an old process value is overriding the file, run `Remove-Item Env:DATABASE_URL` in that shell.

```powershell
git check-ignore -v -- .env
git ls-files -- .env
```

## 4. Verify PostgreSQL, migrate, and run Django

From `backend/`, check the database engine and run `SELECT 1`. Expect `postgresql: SELECT 1 returned 1`. Stop if the check fails. Django falls back to SQLite when `DATABASE_URL` is absent.

```powershell
uv run python manage.py shell -c "from django.db import connection; assert connection.vendor == 'postgresql', 'Expected PostgreSQL'; cursor = connection.cursor(); cursor.execute('SELECT 1'); print(f'{connection.vendor}: SELECT 1 returned {cursor.fetchone()[0]}'); cursor.close()"
```

Confirm the URL points to your development branch before applying migrations. An `[X]` marks an applied migration.

```powershell
uv run python manage.py check
uv run python manage.py migrate
uv run python manage.py showmigrations
```

Switch back to your development runtime credentials after applying migrations. If you need to test Django Admin and don't have an account on that branch, run `uv run python manage.py createsuperuser` from `backend/` and follow the interactive prompts.

```powershell
uv run python manage.py runserver 127.0.0.1:8000
```

Open [Django Admin](http://127.0.0.1:8000/admin/) and sign in with your development account. Use synthetic data when testing. Press `Ctrl+C` to stop the server.

## 5. Start the booking frontend

Keep Django running on port 8000. In a second PowerShell terminal, follow the [Vite setup](README.md#start-the-frontend). Open the booking form on port 5173 and submit a synthetic request. Check that the confirmation shows a booking ID and that the request appears as Pending in Django Admin.

## 6. Open your first pull request

Before editing, return to the repository root with `Set-Location ..` if you're still in `backend/` or `frontend/`. Check for existing work with `git status --short`. Once the tree is clean, update the shared Sprint One branch and create a branch that describes your change.

```powershell
git switch refactor/chefdate-structure
if ($LASTEXITCODE -ne 0) { throw 'Could not switch to the Sprint One branch.' }
git pull --ff-only origin refactor/chefdate-structure
if ($LASTEXITCODE -ne 0) { throw 'Could not fast-forward the Sprint One branch.' }
git switch -c feature/first-change
```

If you change a Django model, generate the migration and review it before applying it to your Neon development branch. Start from the repository root. Stage the generated migration under `backend/<app>/migrations/` with the model change.

```powershell
Set-Location .\backend
uv run python manage.py makemigrations
git status --short
```

After reviewing the generated file, verify the PostgreSQL connection as in step 4, then apply and check the migration. The last command returns you to the repository root.

```powershell
uv run python manage.py migrate
uv run python manage.py showmigrations
uv run python manage.py makemigrations --check --dry-run
Set-Location ..
```

From the repository root, review the changes and stage only files for this pull request. Run the last two lines once for each file, including any new migration. If Git asks for an author identity, set `user.name` and `user.email` with `git config --local` using your preferred Git author details.

```powershell
git status --short
git diff --check
git diff
$fileToStage = Read-Host 'Enter one repository-relative file to stage'
git add -- $fileToStage
```

Check the staged diff before committing. Make sure it contains only the intended changes and no credentials or local data.

```powershell
git diff --cached --check
git diff --cached
```

Replace the example commit message with a description of your change, then push your branch.

```powershell
git commit -m "Describe the ChefDate change"
if ($LASTEXITCODE -ne 0) { throw 'Could not commit the staged changes.' }
git push --set-upstream origin HEAD
```

Open the repository's pull requests page.

```powershell
Start-Process 'https://github.com/SMUAlfredo/ChefDate_deploy_final_project/pulls'
```

Select **New pull request**, set the base branch to `refactor/chefdate-structure` for Sprint One and the compare branch to your feature branch. Review the changed files, then describe what changed, what you verified, and any migrations before submitting. [GitHub pull request guide](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
