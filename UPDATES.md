# Change history

Entries are listed newest first. Each entry summarizes the change, the relevant files, the checks performed, and any remaining work.

## 2026-11-22 · Security rules for contributors and agents

- Added `SECURITY_RULES.md` with requirements for secrets, private data, access control, secure deployment, and verification.
- Made the rules required reading in `AGENTS.md` and linked them from `README.md`.
- Reviewed the guidance against OWASP ASVS and the Django 5.2 deployment checklist. Verified local documentation links and checked the staged diff for whitespace errors.

## 2026-11-22 · Versioned documentation and local secret handling

- Added `README.md`, `AGENTS.md`, and `UPDATES.md` to the checkout that tracks `origin/main`.
- Updated `backend/config/settings.py` to use `DJANGO_SECRET_KEY` when set and generate a temporary key for local development otherwise.
- Django’s system check passed. Verified both secret key paths, the welcome page’s HTTP 200 response in Django’s test client, and Git’s ignore rules for local files.

## 2026-11-22 · English documentation

- Translated `README.md`, `UPDATES.md`, and `AGENTS.md` into English, including earlier entries in the change history.
- Verified that the README commands and link targets were preserved.

## 2026-11-22 · Documentation and change tracking

- Created `README.md` with the requirements, local startup commands for PowerShell, and migration status.
- Created `UPDATES.md` and `AGENTS.md` to record project context and guide future reviews.
- Checked the README’s internal link and the PowerShell command syntax.

## 2026-11-22 · Initial backend

- Created `backend/` with Django 5.2.19, `manage.py`, and the initial configuration in `backend/config/`. `backend/pyproject.toml` requires Python 3.14 or later, and `backend/uv.lock` pins the dependencies.
- Created `.gitignore` to exclude `.env`, `.venv/`, `__pycache__/`, and `db.sqlite3`.
- `uv run python manage.py check` passed. The Django welcome page returned HTTP 200 at `http://127.0.0.1:8000/`. Git confirmed all four ignore rules.
- The Neon PostgreSQL connection, database migrations, frontend, and deployment are pending.
