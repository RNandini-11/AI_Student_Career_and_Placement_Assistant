@'
# Contributing Guide

## Branching Strategy

Create a separate branch for every task. Do not directly modify the main branch.

Branch naming examples:
- feature/feature-name
- fix/bug-name
- docs/documentation-name

## Development Workflow

1. Synchronize your local main branch with origin/main.
2. Create a feature branch.
3. Implement your changes.
4. Test your changes.
5. Review your changes using git diff.
6. Commit your changes with a meaningful message.
7. Push your feature branch to GitHub.
8. Open a Pull Request against main.
9. Address review feedback.
10. Merge only after the required review and checks.

## Commit Messages

Use descriptive commit messages.

Examples:
- docs: add contributor workflow guide
- fix: correct placement prediction validation
- feat: add student profile endpoint

## Pull Request Guidelines

- Explain what the change does.
- Describe how it was tested.
- Keep changes focused.
- Do not commit API keys, credentials, or secrets.
- Request review before merging into main.
'@ | Set-Content CONTRIBUTING.md