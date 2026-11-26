# Change history

Entries are listed newest first. Each entry summarizes the change, the relevant files, the checks performed, and any remaining work.

## 2026-11-26 · Verify the read-only add-on catalog

- Reviewed the existing catalog implementation in `backend/catalog/add_ons.py`, `backend/catalog/add_on_views.py`, `backend/catalog/urls.py`, and `backend/catalog/test_add_ons.py`. `GET /api/catalog/add-ons/` returns `cleaning` at CAD 50.00 and `waitstaff` at CAD 80.00 with two-decimal price strings. The fixed prices are reusable by future server-side pricing.
- Ran `uv run --locked python manage.py test --settings=config.settings_test` from `backend/`. All 21 tests passed on in-memory SQLite, including the add-on response and POST rejection, the existing cuisine catalog, and booking submission. Server-side pricing remains pending.

## 2026-11-26 · Set add-on quantities by guest count

- Updated `frontend/src/bookings/BookingAddOns.jsx`, `frontend/src/bookings/bookingAddOns.css`, and `frontend/src/bookings/BookingForm.jsx` to show the five-guest coverage and unit price and let users increase or decrease Cleaning and Waitstaff independently. Each add-on is optional and its maximum rounds the guest count up to the next group of five. Reducing the guest count caps existing selections at the new maximum.
- Passed `npm ci --offline` and `npm run build` in an isolated frontend copy. In Chrome at 375 pixels with Django on in-memory SQLite, verified the limits for 5, 6, and 11 guests, quantity controls, return from chef selection, HTTP 201 for a booking with a preferred chef, reset after success, and catalog failure handling. Also verified that Vite serves the updated selector and catalog in the local demo.
- The quantities are stored in the draft. Booking persistence and server-side totals remain pending.

## 2026-11-26 · Restore the local demo catalog

- Found that Vite on port 5173 returned HTTP 502 for the chef and add-on catalogs because Django was stopped on port 8000. A read-only check of the local SQLite demo found six cuisines, 18 chefs, and six cuisine photos. The add-on catalog uses fixed prices in Django.
- With approval, backed up the local demo database, rehearsed `bookings.0002_preferred_chef` on a copy, and applied it to the demo database using `config.settings_demo`. Verified the new column, preserved booking IDs, checked SQLite foreign keys, and confirmed both booking migrations were applied.
- Started Django on `127.0.0.1:8000`. Verified HTTP 200 through Vite for the form, both catalog routes, a sample photo, and the booking CSRF route. The catalog returned 18 chefs and both add-ons. Verification covered the local demo. Hosted verification remains pending.

## 2026-11-26 · Optional add-ons in the booking draft

- Added `frontend/src/bookings/BookingAddOns.jsx` and `frontend/src/bookings/bookingAddOns.css`. Mounted the selector in `frontend/src/bookings/BookingForm.jsx`. Cleaning and Waitstaff display their CAD prices from the catalog. Selections stay in the draft when browsing cuisines and reset after a successful booking.
- Passed `npm ci --offline` and `npm run build` in an isolated frontend copy and all 21 Django tests with `config.settings_test` on in-memory SQLite. In Chrome at 375 pixels against the same settings, verified the two catalog prices, selection retention through cuisine and chef navigation, booking creation with HTTP 201 and a preferred chef, checkbox reset, and continued form availability when the catalog request was blocked.
- Saving add-ons with the booking and calculating the total on the server remain pending.

## 2026-11-25 · Read-only demo add-on catalog

- Defined Cleaning at CAD 50.00 and Waitstaff at CAD 80.00 per booking as reusable `Decimal` prices in `backend/catalog/add_ons.py`. Registered `GET /api/catalog/add-ons/` in `backend/catalog/urls.py` and added `backend/catalog/add_on_views.py` to return each slug, display name, and two-decimal price string.
- Added `backend/catalog/test_add_ons.py` to verify both options and prices and check that POST returns `405`. All 21 Django tests passed under `config.settings_test` on in-memory SQLite, including the existing catalog and booking tests. Booking selection and server-side price calculation remain pending.

## 2026-11-25 · Submit the selected chef from React

- Updated `frontend/src/App.jsx` and `frontend/src/bookings/BookingForm.jsx` to send the selected `preferred_chef_slug` through the existing booking client. `cuisine_type` still carries the cuisine display name. Changing cuisines clears an incompatible chef, and requests without a selection omit the slug.
- Updated `frontend/src/bookings/BookingFields.jsx` to display chef field errors beside the picker. Correcting the selection clears the previous chef error, while a successful submission still displays the returned booking ID.
- Passed `npm ci --offline` and `npm run build` in an isolated frontend copy. In Chrome with seeded Django and in-memory SQLite, verified that the returned booking ID referred to a row with the selected chef, that an omitted slug saved a booking with no preference, and that a stale selection produced a real `400` with no booking write. The draft survived the error and resubmission with another chef succeeded. Hosted verification remains pending.

## 2026-11-25 · Save an optional preferred chef in Django

- Added a nullable `Booking.preferred_chef` relation in `backend/bookings/models.py` and migration `backend/bookings/migrations/0002_preferred_chef.py`. The migration depends on the catalog migration that creates chefs. Removing a chef clears the preference and preserves the booking.
- Updated `backend/bookings/forms.py` to accept `preferred_chef_slug` and resolve it against the catalog. React sends the cuisine display name in `cuisine_type`, so the form compares display names case-insensitively. Unknown slugs and cuisine mismatches return field-level errors. The Pending default, existing `201` response, and booking requests without a chef preference were preserved.
- Added API coverage in `backend/bookings/test_preferred_chef.py`. With `config.settings_test` on in-memory SQLite, all 19 tests passed, the migration check found no missing migrations, and apply, rollback, and reapply preserved an existing booking. Sending the slug from React and applying the migration outside the test environment remain pending.
- Rechecked the endpoint from PowerShell using the Django test client with CSRF enforcement and the seeded in-memory catalog. A matching chef and an omitted preference returned `201`, unknown and mismatched chefs returned `400`, and a request without CSRF returned `403`. Rejected requests created no bookings.

## 2026-11-25 · Preferred chef in the booking draft

- Updated `frontend/src/App.jsx` and `frontend/src/cuisines/CuisinesPage.jsx` to open each cuisine's chefs from the nested catalog response. Added `CuisineChefs.jsx` and `chefs.css` under `frontend/src/cuisines/` to show each chef's name, CAD base price per booking, demo rating, and Select chef button.
- Updated `frontend/src/bookings/BookingForm.jsx` and `BookingFields.jsx` to display the cuisine and draft-only chef preference. Switching cuisines clears the previous chef. The booking request keeps its existing payload. Saving the preference in Django remains pending.
- Passed `npm ci --offline` and `npm run build` in an isolated frontend copy. In Chrome with Vite preview and seeded Django on in-memory SQLite, verified all six database photos and all 18 matching chefs with prices and ratings, returning to the cuisine list, draft retention, clearing an incompatible chef, the 375-pixel layout, and a successful booking with the original request fields.

## 2026-11-25 · Cuisine picker and catalog photos

- Added `frontend/src/App.jsx` and the cuisine page and styles under `frontend/src/cuisines/`. Updated `main.jsx`, `BookingForm.jsx`, and `BookingFields.jsx` to open `/#/cuisines` from the Preferred cuisine button. Choosing a cuisine returns to the existing booking draft and supplies `cuisine_type` to the booking API. The six bundled photos remain available if the live catalog cannot load.
- Added six JPEG copies in `frontend/src/cuisines/assets/`. The Mexican, Italian, Indian, Canadian, French, and Spanish copies come from `mexicana.jpg`, `italian.jpg`, `india.jpg`, `canada.jfif`, `francia.jpg`, and `españa.jpg`, respectively. The originals in `images/` were preserved byte for byte.
- Added `CuisinePhoto`, migration `0003_cuisine_photo.py`, the read-only photo route, `load_cuisine_photos`, and backend tests. Added `config/settings_demo.py` for the persistent local SQLite demo and verified six stored JPEGs against the source bytes. The existing Vite instance returned all six JPEGs after Django started on port 8000.
- Passed `npm ci --offline`, `npm run build`, the migration consistency check, and all 15 Django tests. In Chrome with Vite preview and isolated Django, verified all six database photos, six bundled fallbacks, the required cuisine selection, draft preservation through all three return paths, a 375-pixel layout, and a successful booking submission. Neon loading and chef selection remain pending.

## 2026-11-25 · Shared React navigation

- Added `frontend/src/SiteHeader.jsx` and mounted it above the booking form from `frontend/src/main.jsx`. Moved the ChefDate label out of `frontend/src/bookings/BookingForm.jsx` and added header styles in `frontend/src/styles.css`. Book links to the form and is marked current. Profile and Booking Status display as unavailable.
- `npm ci` and `npm run build` passed in an isolated copy after a locked dependency interrupted the checkout install. Restored the missing dependency files, and the checkout build also passed. In local Chrome at desktop and 375-pixel widths, verified the header, Book link, and draft preservation. With synthetic mock API responses, verified required-field validation, retained input on a field error, and confirmation with form reset after success.
- Rebuilt the checkout and repeated the Chrome check against Django on isolated in-memory SQLite. The real booking endpoint returned a field error with `400`, accepted the corrected synthetic request with `201`, and the form displayed the booking ID and reset.
- Profile and Booking Status destinations, cuisine browsing, image mapping, and chef selection remain pending.

## 2026-11-25 · Read-only catalog API

- Added `GET /api/catalog/` in `backend/catalog/views.py` and `backend/catalog/urls.py`, with a route in `backend/config/urls.py`. The response groups chefs by cuisine, orders both levels by slug, and returns CAD prices as two-decimal strings and demo ratings as numbers.
- Added endpoint tests in `backend/catalog/tests.py`. With `config.settings_test` on in-memory SQLite, the seeded response contained six cuisines with three chefs each, the empty response was `[]`, and POST returned `405` without writing records. All three catalog tests and all ten existing booking tests passed.
- Frontend integration and hosted verification remain pending.

## 2026-11-25 · Consolidate the initial catalog migrations

- Added `backend/catalog/migrations/0001_initial_catalog.py`. New databases create `Cuisine` and `Chef` in one migration. Kept both original catalog migrations for existing databases and retained the booking migration in its own app.
- Verified fresh, partially migrated, and fully migrated histories in isolated SQLite with `config.settings_test`. Existing rows were preserved, the fresh catalog seeded six cuisines and 18 chefs, Django found no missing migrations, and all ten booking tests passed. Verification on a shared database remains pending.

## 2026-11-25 · Local SQLite setup instructions

- Organized `README.md` into a local SQLite setup section and a separate Django startup section. Added comments explaining the database guard, dependency setup, migrations, and optional demo seed. Included a temporary SQLite example that migrates and seeds in one Django process.
- Ran the documented in-memory example and verified it created six cuisines and 18 chefs. Verified that the persistent setup stops when a PostgreSQL URL is configured. The seed command must be present in the checkout to run either seed example.

## 2026-11-25 · Demo catalog seed command

- Added `seed_demo_catalog.py` under `backend/catalog/management/commands/` and the two management command package markers. The command seeds six cuisines and three fictional chefs per cuisine using stable slugs and decimal prices and ratings. Matching records are reused, and a conflicting slug aborts the entire transaction.
- Verified on in-memory SQLite with `config.settings_test` that the first run created six cuisines and 18 chefs, the second created zero records, and late conflicts on both cuisine and chef slugs rolled back earlier inserts. Unrelated catalog records, bookings, and users were preserved. All ten booking tests passed.
- The catalog endpoint, React integration, and Neon verification remain pending.

## 2026-11-25 · Chef catalog model

- Added `Chef` in `backend/catalog/models.py` and generated `backend/catalog/migrations/0002_chef.py`. Each chef has a display name, a unique slug, a required cuisine, a decimal base price in CAD per booking, and a decimal demo rating. Django protects cuisines referenced by chefs from deletion.
- Verified with `config.settings_test` on in-memory SQLite that a chef saves with a cuisine and retains its slug after a display name edit. The database accepted a zero price and ratings of 1.0 and 5.0, and rejected duplicate slugs, negative prices, ratings outside that range, and missing cuisines. Applying, rolling back, and reapplying the Chef migration preserved the existing cuisine row.
- All ten booking tests passed, and the migration consistency check found no pending model changes. Fictional catalog records, the catalog endpoint, frontend integration, and Neon verification remain pending.

## 2026-11-25 · Cuisine catalog model

- Added `Cuisine` in `backend/catalog/models.py` with a display name and a unique slug. Registered the app in `backend/config/settings_base.py` and generated `backend/catalog/migrations/0001_initial.py`.
- On in-memory SQLite with `config.settings_test`, verified migration apply, rollback, and reapply, an empty initial catalog, and database rejection of duplicate slugs. Django found no pending model changes. All ten existing booking tests passed.
- The later seed task uses Mexican (`mexican`), Italian (`italian`), Indian (`indian`), Canadian (`canadian`), French (`french`), and Spanish (`spanish`). Chef, seed data, the catalog endpoint, React integration, and Neon verification remain pending.

## 2026-11-25 · ChefDate coding conventions

- Updated `AGENTS.md` to record required reading, mini-task scope, code organization and reuse, English project content, and preservation of supplied image filenames.
- Defined the handoff requirements for checks, `UPDATES.md`, and exact staging commands. Alfredo makes commits and pushes. Reviewed the documentation diff and checked local links and whitespace.
- Publication remains pending.

## 2026-11-24 · Security rules for the remaining Sprint One work

- Aligned `SECURITY_RULES.md` with `AGENTS.md` on the verified baseline, authorized infrastructure changes, safe migration targets, isolated tests, and Git review.
- Added security controls for US-05 through US-10, including draft behavior, staff permissions, server-side pricing and validation, simulated payment data, and hosted CSRF verification. Checked local links, story coverage, and the documentation diff.
- Implementation and security verification of the remaining stories are pending.

## 2026-11-24 · Agent rules for the remaining Sprint One work

- Expanded `AGENTS.md` to protect the verified booking baseline, focus work on the assigned story, keep new modules small, and document the acceptance criteria for US-05 through US-10.
- Defined safeguards for shared infrastructure and migration targets, isolated testing, security checks, scoped commits, and handoff records. Reviewed the documentation diff, references, and story list.
- The remaining stories and the collaborator setup confirmations for REQ-07 are pending.

## 2026-11-24 · Clarify the scope of the assigned tasks

- Corrected the scope labels in `README.md`, `CONTRIBUTING.md`, and the previous `UPDATES.md` entry. The seven reviewed subtasks are an individual assignment. The team still needs to confirm local setup on each collaborator's machine for REQ-07.
- Reviewed the documentation diff and checked the PowerShell examples.

## 2026-11-24 · Onboarding and verification of assigned subtasks

- Updated `README.md` and `CONTRIBUTING.md` with the shared development branch, locked installs, local SQLite and Neon setup, Vite startup, and the booking review steps.
- Verified a fresh clone from the private repository, both locked installs, SQLite migrations, ten Django tests, and the Vite build. In Chrome, a server field error preserved the input, a valid request displayed its ID and cleared the form, and an authorized staff account opened the single Pending request in Admin. Browser checks used synthetic data and isolated SQLite.
- GitHub reported two direct collaborators besides the owner and no pending invitations. Each collaborator still needs to confirm setup on their own machine. Neon development migration evidence comes from the November 22 entry.

## 2026-11-24 · GitHub purge follow-up

- Verified through GitHub's public API that the original affected commit still returned HTTP 200. The repository reported zero forks and no pull requests.
- Opened the GitHub Support portal for the server-side purge. Submission requires an authenticated account and remains pending.

## 2026-11-24 · Publish and verify Git history cleanup

- Rewrote the historical Django settings and published the cleaned `main` at `0512242`. That commit also applies the environment and SQLite ignore rules to `main`. Rewrote the local refactor branch while preserving its application tree and restored tracking of the new `origin/main`.
- Scanned 196 local Git objects for credential patterns, confirmed the original affected commit is absent locally, ran `git fsck --full`, and passed all ten Django tests on in-memory SQLite.
- GitHub still returned HTTP 200 for the old commit by hash after the branch update. GitHub Support must handle any remaining server-side references or cached views. External key reuse and other clones remain outside the verified scope.

## 2026-11-24 · Internal booking security verification

- Added checks in `backend/bookings/tests.py` that observe the ORM's parameterized INSERT, confirm Admin escapes displayed customer input, and confirm view-only staff cannot edit a booking. All ten tests passed on in-memory SQLite, including the existing CSRF and Admin permission checks.
- The locked Python and npm audits reported no known dependency vulnerabilities. A credential-pattern scan of the compiled frontend found no matches.
- Django's deployment check on isolated development-style settings reported six warnings covering HSTS, HTTPS redirection, secure session and CSRF cookies, debug mode, and allowed hosts. Production settings, login and booking abuse limits, and verification against the target environment remain pending. Neon was not used.

## 2026-11-24 · Booking input limits and date validation

- Capped JSON booking requests at 32 KiB or Django's lower configured limit in `backend/bookings/views.py`. Oversized bodies are rejected with HTTP 413 before JSON decoding.
- Limited allergy notes to 1,000 characters in `backend/bookings/forms.py` and `frontend/src/bookings/BookingFields.jsx`. The booking form now validates that dates can be represented in UTC before saving. Existing records and the schema require no migration.
- Added regressions in `backend/bookings/tests.py`. All eight Django tests on in-memory SQLite, the migration dry run, and the Vite build passed.

## 2026-11-24 · Git credential review and local file exclusions

- Reviewed 22 commits reachable from local refs, including the local `origin/main` reference, and 87 unique blobs for common credential patterns and sensitive paths. A historical Django signing key appears in `backend/config/settings.py` at `dd9f0ef`. It is absent from the current source and the current shell has no configured key. No other credential matches were found. External reuse was not verified.
- Updated `.gitignore` to exclude environment variants and SQLite sidecar files. Verified the ignore rules, the environment template exception, and the absence of the tested sensitive paths from the index.
- If the historical key was reused elsewhere, rotate it and remove it from any signing fallback list. Any history rewrite requires coordination with the repository owner.

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
