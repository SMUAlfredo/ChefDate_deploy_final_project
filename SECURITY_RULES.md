# ChefDate Security Rules

Act as an application security professional on every ChefDate task. Apply these rules to design, code, configuration, reviews, testing, and deployment. Review the data and trust boundaries affected by each change, then use the applicable OWASP ASVS requirements to choose and verify controls. Deny access to private data and privileged actions by default.

## Secrets and private data

- Keep credentials, signing keys, tokens, database URLs, `.env` files, and data exports out of Git, client bundles, screenshots, logs, and agent output. Use environment variables or an approved secrets manager. Use placeholders in documentation and synthetic records in tests and demos.
- Collect and return only the data required for the feature. Review API payloads, templates, URLs, logs, analytics, caches, and exports for unintended disclosure. Use explicit field allowlists in API responses and redact sensitive values from diagnostics.
- Keep development, test, and production credentials and data separate. Give each service the minimum permissions it needs. Protect private files and backups with access controls and encryption.
- If you discover an exposed secret, report its location without repeating the value. Treat an active secret as compromised and prioritize revoking or rotating it. Coordinate any repository history cleanup with the owner.

## Application controls

- Enforce authorization on the server for every protected action and resource. Check ownership or role on reads, writes, downloads, and exports. A hidden UI control or a hard-to-guess ID grants no permission.
- Use Django’s authentication, password hashing, CSRF protection, ORM, and template escaping. Validate untrusted input on the server. Use parameterized queries when raw SQL is necessary and escape output for its specific context. Restrict upload types and sizes and serve private uploads through an authorization check.
- Keep authentication cookies `HttpOnly` and use `Secure` over HTTPS with an appropriate `SameSite` policy. Restrict cross-origin access to explicit trusted origins when needed. Rate-limit sensitive flows such as sign-in and password recovery. Return generic public errors and keep sanitized diagnostic detail in restricted logs.

## Deployment

- Keep Django’s development server and debug pages local. Before public deployment, require a production server, `DEBUG=False`, explicit `ALLOWED_HOSTS`, HTTPS, and a production `DJANGO_SECRET_KEY` supplied securely. Fail startup if required production secrets are missing. Use security headers appropriate to the deployment, including CSP and HSTS once HTTPS is verified.
- When connecting PostgreSQL in Neon, use TLS with server identity verification, an application role with only the permissions needed at runtime, and separate credentials for schema changes. Keep the connection string on the server and protect backups.
- Review dependency advisories for changes that add or update packages. Commit dependency lockfiles and use them for reproducible installs.

## Verification before handoff

- Review the relevant diff and staged files for secrets, private data, and weakened security controls. For changes to a protected feature, check that legitimate access works and that unauthenticated users and users without the required permission are denied. Use synthetic data and authorized environments for these checks.
- For Django deployment changes, run `uv run python manage.py check --deploy` against the target settings and review the results. Report security checks performed and any gaps in `UPDATES.md` without exposing sensitive details. Resolve known issues that could expose private data before release.

## References

- [OWASP Application Security Verification Standard](https://asvs.owasp.org/)
- [Django 5.2 deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Neon guidance on PostgreSQL connection security](https://neon.com/blog/postgres-needs-better-connection-security-defaults)
