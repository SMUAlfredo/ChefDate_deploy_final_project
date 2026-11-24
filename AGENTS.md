# Working on ChefDate

- Before starting any ChefDate task, read and follow [SECURITY_RULES.md](SECURITY_RULES.md). Apply it throughout design, implementation, review, and verification.
- Before starting a change, read `UPDATES.md` and check Git status for project context and work in progress.
- Use the history to locate the relevant files. Expand your review when dependencies, verification, or a discrepancy with the history calls for it.
- After each change, add an entry at the top of `UPDATES.md` with the date, a summary, the relevant files, the checks performed, and any remaining work.
- Mention the `UPDATES.md` entry in your summary to the user.

## Code structure and commits

- Group related functions in modules with a clear responsibility. Keep entry points focused on wiring, and keep validation, data access, and presentation in the components that own them.
- Prefer short, readable functions and descriptive names. Remove dead code and unnecessary duplication after checking their callers. Introduce a module or abstraction when it makes the code easier to understand and maintain.
- Preserve existing behavior and public contracts during refactoring unless the task calls for a behavior change.
- Make one focused Git commit per coherent change, including its `UPDATES.md` entry. Run the relevant checks, review the staged diff, and use a commit message that describes the change. Stage only files that belong to that change.
