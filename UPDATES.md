# Change history

Entries are listed newest first. Each entry summarizes the change, the relevant files, the checks performed, and any remaining work.

## 2026-11-24 · Source file comments

- Added a final comment to all 24 tracked Python, JavaScript, JSX, CSS, and HTML files under `backend/` and `frontend/`.
- Verified the final line of each file and reviewed the diff. All six Django tests passed on in-memory SQLite, and the Vite build passed.

## 2026-11-24 · Separate shared, local, and test Django settings

- Moved shared Django settings to `backend/config/settings_base.py`. Local settings still configure PostgreSQL or the SQLite fallback. Test settings now select in-memory SQLite directly without patching the environment or loading local database settings.
- All six Django tests passed. The migration dry run found no changes. Synthetic configuration checks verified URL precedence, invalid URL handling, SQLite fallback, PostgreSQL certificate and hostname verification settings, and test isolation without connecting to Neon.

## 2026-11-24 · Group booking routes and form validation

- Moved booking routes to `backend/bookings/urls.py` and kept the project URL configuration focused on routing by app. Moved field validation and error-code formatting to `backend/bookings/forms.py`. The view still handles the JSON request and response.
- All six booking tests passed on in-memory SQLite, covering CSRF, Admin permissions, malformed input, and successful creation. The diff passed the whitespace check.

## 2026-11-24 · Separate frontend booking responsibilities

- Kept the React entry point in `frontend/src/main.jsx` and moved form behavior, grouped fields, and API calls to `frontend/src/bookings/`. Both field groups now share the same rendering logic.
- The production build passed. A Node smoke check with synthetic responses verified the CSRF request, booking POST, success, field and generic errors, and request failure handling. Browser interaction was not rerun.

## 2026-11-24 · Code structure and commit conventions

- Updated `AGENTS.md` to require focused modules, readable code, and one verified commit per coherent change.
- Reviewed the instructions and checked the documentation diff for whitespace errors. The backend and frontend refactors follow in separate commits.

## 2026-11-22 · Local booking request form

- Added a minimal React/Vite form for the existing booking API. It disables submission while sending, displays the ID on `201`, and shows field errors on `400` while preserving the entered values.
- Added a non-cacheable Django CSRF token route. Vite proxies `/api/` on loopback and preserves the browser's host for Django's origin check.
- The frontend build, npm dependency audit, and six backend tests passed. Chrome verified `201` with a visible ID, `400` with retained values, and the disabled button. The isolated SQLite database contained only the valid booking. An initial run reached an existing server on port 8000 and created a synthetic booking in Neon development. With the owner's approval, the record was matched field by field and removed. The successful run used dedicated ports and verified the SQLite target before sending.
- For local development, start Django on `127.0.0.1:8000`, then run `npm ci` and `npm run dev` from `frontend/`. Production hosting, payments, and account integration remain pending.

## 2026-11-22 · Booking creation endpoint

- Added `POST /api/bookings/` with JSON input and the existing Django CSRF protection. It reuses the `Booking` model's validation through a `ModelForm`, creates bookings as `pending`, returns only the ID with `201`, and rejects invalid requests with `400` before saving.
- Added tests with synthetic data and an in-memory SQLite configuration. The tests cover a saved booking in Django Admin, missing and invalid fields, optional allergy notes, and the endpoint's access protections. The migration dry run found no model changes, and Neon was untouched.
- Run the tests from `backend/` with `uv run python manage.py test bookings --settings=config.settings_test`. Client integration is pending.

## 2026-11-22 · Initial booking model and admin

- Added `backend/bookings/` and registered it in `backend/config/settings.py`. The model uses the requested fallback fields, defaults to `Pending`, and also supports `Confirmed`.
- Registered `Booking` in Django Admin with the client name, event date and time, guest count, and status in the list.
- Applied `bookings.0001_initial` on Neon development and confirmed it appears as `[X]`. Verified that a synthetic booking can be saved and reloaded, PostgreSQL rejects invalid guest counts and statuses, and Admin enforces booking permissions. Rolled back all synthetic records.

## 2026-11-22 - Initial migrations on Neon development

- Applied Django's initial migrations to the configured Neon development database with `uv run python manage.py migrate`.
- `uv run python manage.py showmigrations` showed all 18 migrations as `[X]` across `admin`, `auth`, `contenttypes`, and `sessions`. None remain pending.

## 2026-11-22 · Local Neon PostgreSQL configuration

- Added PostgreSQL dependencies with `uv` and configured `backend/config/settings.py` to prefer the environment’s `DATABASE_URL`, then read `backend/.env`. PostgreSQL connections verify the server certificate and hostname.
- Added `backend/.env.example` with a fictitious URL and documented local setup in `README.md`. Git confirmed that `backend/.env` is ignored and untracked.
- Django’s system check passed. Verified configuration precedence, invalid URL handling, TLS options, and the SQLite fallback with dummy inputs.
- `uv audit --locked` found no known vulnerabilities or adverse project statuses in the nine installed packages.
- Live connection and initial migrations are pending confirmation that the direct development branch URL has been saved locally.

## 2026-11-22 · Security rules for contributors and agents

- Added `SECURITY_RULES.md` with requirements for secrets, private data, access control, secure deployment, and verification.
- Made the rules required reading in `AGENTS.md` and linked them from `README.md`.
- Reviewed the guidance against OWASP ASVS and the Django 5.2 deployment checklist. Verified local documentation links and checked the staged diff for whitespace errors.

## 2026-11-22 · Versioned documentation and local secret handling

- Added `README.md`, `AGENTS.md`, and `UPDATES.md` to the checkout that tracks `origin/main`.
- Updated `backend/config/settings.py` to use `DJANGO_SECRET_KEY` when set and generate a temporary key for local development otherwise.
- Django’s system check passed. Verified both secret key paths, the welcome page’s HTTP 200 response in Django’s test client, and Git’s ignore rules for local files.


## 2026-11-22 · Documentation and change tracking

- Created `README.md` with the requirements, local startup commands for PowerShell, and migration status.
- Created `UPDATES.md` and `AGENTS.md` to record project context and guide future reviews.
- Checked the README’s internal link and the PowerShell command syntax.

## 2026-11-22 · Initial backend

- Created `backend/` with Django 5.2.19, `manage.py`, and the initial configuration in `backend/config/`. `backend/pyproject.toml` requires Python 3.14 or later, and `backend/uv.lock` pins the dependencies.
- Created `.gitignore` to exclude `.env`, `.venv/`, `__pycache__/`, and `db.sqlite3`.
- `uv run python manage.py check` passed. The Django welcome page returned HTTP 200 at `http://127.0.0.1:8000/`. Git confirmed all four ignore rules.
- The Neon PostgreSQL connection, database migrations, frontend, and deployment are pending.
