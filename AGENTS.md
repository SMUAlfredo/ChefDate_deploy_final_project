# Working on ChefDate

- At the start of every ChefDate task, read [SECURITY_RULES.md](SECURITY_RULES.md) and [UPDATES.md](UPDATES.md), and check Git status. Use `SECURITY_RULES.md` as the source for security requirements throughout design, implementation, review, and verification. Use `UPDATES.md` to understand the current state of the project and Git status to identify work in progress.
- Use the history to locate the relevant files. Expand your review when dependencies, verification, or a discrepancy with the history calls for it.

## Scope and the verified baseline

- Treat the tested US-01 through US-04 implementation as the baseline. It includes the booking model and migration, the JSON booking endpoint, the React form and acknowledgement, and staff review in Django Admin. REQ-07 still needs each collaborator's setup confirmation. Record their confirmation only after they provide it.
- Identify the assigned story or mini-task and its acceptance criteria before editing. Keep each change focused on one mini-task and the integrations it requires. Use `refactor/chefdate-structure` as the shared starting point for the remaining Sprint One work while it is the team's designated base.
- Add new functionality in focused modules. Keep previously validated source files intact unless the user explicitly authorizes edits to them. When a story needs an existing integration point, explain the smallest edit needed, its impact on current callers, and how you will verify it before editing the baseline. Carry on with independent work while that decision is pending.
- Preserve existing work by other contributors, including uncommitted changes. Keep unrelated cleanup, renames, reformatting, dependency upgrades, and generated files out of the change. Keep released migrations intact and use new migrations for approved schema changes.

### Remaining Sprint One stories

| Story | Expected result |
| --- | --- |
| US-05 | Show an editable booking summary. Returning to edit preserves the entered values and creates a booking only after confirmation. |
| US-06 | Staff can manually assign a chef and confirm a booking in Django Admin. Verify permissions and use synthetic sample assignments. |
| US-07 | Calculate the basic price on the server, show the total in the review step, and test the pricing rule. |
| US-08 | Provide one simulated checkout path, store its outcome, and show the result. Use fictitious payment data and keep raw payment inputs out of storage and logs. |
| US-09 | Validate email, phone, country, postal or ZIP code, and fictitious card type, number, and expiry. Reject past events. Enforce these checks on the server and return field-level feedback. |
| US-10 | Prepare the Django Render service, React Netlify site, and isolated Neon demo database. Verify CSRF across the intended routes. |

## Code structure

- Follow the existing project structure and give each new module one responsibility. Keep entry points focused on wiring. Keep request handling, validation, persistence, business rules, and rendering in the components that own them.
- Keep functions short enough to follow in one pass. Use descriptive names, straightforward control flow, and small components organized by feature. Reuse existing logic, including tested helpers. Add a function or module when it makes the code easier to understand or maintain, and split files that accumulate unrelated responsibilities. Avoid unused code, duplication, unnecessary dependencies, and unrelated refactoring.
- Write new or edited project content in English, including identifiers, source filenames, comments, docstrings, tests, UI text, validation messages, documentation, `UPDATES.md` entries, and commit messages. Keep the supplied filenames in `images/` and map them to English cuisine names when implementing the frontend.
- Preserve the public API, booking statuses, data compatibility, and permission checks relied on by existing callers. When a story requires a contract change, include the affected clients, existing records, and migration or rollback implications in the review.

## Security and infrastructure

- Enforce validation and permissions in Django for each protected action. Keep CSRF protection, template escaping, parameterized ORM access, and explicit response fields. Configure only the trusted hosts and origins needed for the feature. Keep secrets and private data out of source files, logs, screenshots, and frontend builds.
- Use synthetic data and isolated local settings for routine tests. Before any migration or data write, confirm the environment, database engine, and intended database or branch without displaying the connection string. Use a dedicated Neon demo database for US-10. Use the least-privileged runtime role and separate credentials for schema changes.
- Treat changes to shared services, database schemas or data, deployment settings, credentials, DNS, and GitHub access as separate operations. Use the target and operation the user authorized. Before an authorized shared change, identify its impact, how to roll it back, and how to verify the result. Prepare and test unrelated work locally while a shared change is pending.
- Follow the production settings in `SECURITY_RULES.md` for public hosting. Keep deployment secrets on the server. Verify HTTPS, hosts, cookies, and CSRF routing in the intended environment and run Django's deployment check against its settings. Keep the local development entry points usable.

## Verification and traceability

- Run the relevant baseline and story checks before committing. For backend changes, use `uv run --locked python manage.py test --settings=config.settings_test` from `backend/`. Check migration consistency with `makemigrations --check --dry-run` using the same settings when model code changes. For frontend changes, run `npm ci` and `npm run build` from `frontend/` and exercise the affected flow. For protected features, verify that authorized actions succeed and that unauthorized actions are denied.
- Work on a dedicated branch for the story. Review the diff and staged files for scope, credentials, private data, and weakened controls. Preserve shared history and use ordinary pushes when publication is authorized. Coordinate any requested rewrite, deletion, or forced update with the repository owner.
- Before handoff, review the diff, run the relevant checks, and add an entry at the top of `UPDATES.md` with the date, changed files, what changed, checks actually run and their results, and remaining work. Reference the entry in the handoff.
- Prepare one focused Git commit per mini-task. Provide exact Git staging commands that stage only the files and `UPDATES.md` entry for that change, and provide an English commit message. Identify the story or requirement in the message when applicable. Alfredo makes the commits and pushes.
