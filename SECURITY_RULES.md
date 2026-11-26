# ChefDate Security Rules

Act as an application security professional on every ChefDate task. Apply these rules to design, code, configuration, reviews, testing, and deployment. Review the data and trust boundaries affected by each change, then use the applicable OWASP ASVS requirements to choose and verify controls. Deny access to private data and privileged actions by default.

## Scope and shared infrastructure

- Follow [AGENTS.md](AGENTS.md) for story scope and baseline protection. Preserve the security controls in the verified booking flow. When an assigned story requires an edit to that baseline, describe the smallest change and the regression checks before seeking authorization.
- Verify the authorized target before changing shared services, DNS, repository access, deployment settings, or database state. For a migration or data write, check the environment, database engine, and database or branch without printing the connection string. Review the migration and identify how to recover before applying it. Keep applied migrations intact and make schema changes through new migrations.
- Use isolated local settings and synthetic records for routine testing. Keep local development, the hosted demo, and production separate. Use the dedicated Neon demo database for US-10 and restrict its runtime credentials to the permissions the service needs.

## Secrets and private data

- Keep credentials, signing keys, tokens, database URLs, `.env` files, and data exports out of Git, client bundles, screenshots, logs, and agent output. Use environment variables or an approved secrets manager. Use placeholders in documentation and synthetic records in tests and demos.
- Collect and return only the data required for the feature. Review API payloads, templates, URLs, logs, analytics, caches, and exports for unintended disclosure. Use explicit field allowlists in API responses and redact sensitive values from diagnostics.
- Keep development, test, and production credentials and data separate. Give each service the minimum permissions it needs. Protect private files and backups with access controls and encryption.
- If you discover an exposed secret, report its location without repeating the value. Treat an active secret as compromised and prioritize revoking or rotating it. Coordinate any repository history cleanup with the owner.
- For shared Git work, stage only the files for the assigned story and inspect the staged diff before committing. Preserve shared history and coordinate any authorized rewrite with the repository owner. Keep booking contact data, payment values collected during test runs, and database files out of commits and review artifacts. Use documented fictitious fixtures for tests.

## Application controls

- Enforce authorization on the server for every protected action and resource. Check ownership or role on reads, writes, downloads, and exports. A hidden UI control or a hard-to-guess ID grants no permission.
- Use Django’s authentication, password hashing, CSRF protection, ORM, and template escaping. Validate untrusted input on the server. Use parameterized queries when raw SQL is necessary and escape output for its specific context. Restrict upload types and sizes and serve private uploads through an authorization check.
- Keep authentication cookies `HttpOnly` and use `Secure` over HTTPS with an appropriate `SameSite` policy. Restrict cross-origin access to explicit trusted origins when needed. Rate-limit sensitive flows such as sign-in and password recovery. Return generic public errors and keep sanitized diagnostic detail in restricted logs.

## Controls for the remaining booking stories

| Story | Security control to verify |
| --- | --- |
| US-05 | Keep draft booking data in form state. Returning to edit preserves values and makes no booking write. Validate again in Django when the user confirms. |
| US-06 | Require the Django permissions needed to assign a chef or confirm a booking. Test the allowed staff action and denial for anonymous users and staff with view-only permissions. Limit access to booking contact and allergy data to authorized users. |
| US-07 | Calculate the amount on the server from validated inputs. Treat a total supplied by the browser as untrusted. |
| US-08 | Keep checkout in simulation mode and accept only documented fictitious test inputs. Store the outcome and the booking reference. Keep raw card type, number, expiry, and other payment inputs out of storage, responses, logs, and analytics. |
| US-09 | Enforce contact, location, fictitious payment, and event-date rules on the server. Return field-level errors without echoing sensitive values. Reject invalid submissions before writing records. |
| US-10 | Keep Django and database secrets on the server and out of the React build. Verify the intended frontend origin, CSRF flow, secure cookies, and that requests from an untrusted origin are denied. |

## Deployment

- Keep Django’s development server and debug pages local. Before public deployment, require a production server, `DEBUG=False`, explicit `ALLOWED_HOSTS`, HTTPS, and a production `DJANGO_SECRET_KEY` supplied securely. Fail startup if required production secrets are missing. Use security headers appropriate to the deployment, including CSP and HSTS once HTTPS is verified.
- When connecting PostgreSQL in Neon, use TLS with server identity verification, an application role with only the permissions needed at runtime, and separate credentials for schema changes. Keep the connection string on the server and protect backups.
- Review dependency advisories for changes that add or update packages. Commit dependency lockfiles and use them for reproducible installs.

## Verification before handoff

- Review the relevant diff and staged files for secrets, private data, and weakened security controls. For changes to a protected feature, check that legitimate access works and that unauthenticated users and users without the required permission are denied. Use synthetic data and authorized environments for these checks.
- Run the affected story checks and exercise the relevant parts of the verified booking flow. Use `config.settings_test` for routine Django tests. Check migration consistency when model code changes.
- For Django deployment changes, run `uv run --locked python manage.py check --deploy` against the target settings and review the results. Test over the actual HTTPS routes before exposing the demo. Resolve known issues that could expose private data before release.
- Report in [UPDATES.md](UPDATES.md) which checks ran, the environment used, the results, and remaining gaps. Keep credentials, private data, and sensitive diagnostics out of the entry.

## References

- [OWASP Application Security Verification Standard](https://asvs.owasp.org/)
- [Django 5.2 deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Neon guidance on PostgreSQL connection security](https://neon.com/blog/postgres-needs-better-connection-security-defaults)
