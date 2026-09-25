# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 1.0.x | Yes |
| < 1.0.0 | No |

## Reporting a vulnerability

Please report suspected vulnerabilities through the private security-reporting mechanism enabled by the repository or organization. Do not publish vulnerabilities, credentials, tokens, personal data, or other sensitive details in public issues.

Include enough information to reproduce and assess the issue, such as the affected component, impact, safe reproduction steps, and a possible mitigation when available. Maintainers will assess the report through the available private channel and coordinate disclosure according to the repository's capabilities.

## Handling secrets

Do not commit passwords, tokens, API keys, `.env` files, browser profiles, or credentials. Use environment variables, a managed secret store, or the CI platform's secret mechanism for sensitive configuration. If a secret is exposed, revoke or rotate it through its owner before reporting the incident.
