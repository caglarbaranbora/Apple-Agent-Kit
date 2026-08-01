# Security Policy

## Supported Versions

Apple Agent Kit is currently in 0.x development. Security patches are applied to the most recently published version.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |
| < 0.1   | ❌        |

## Reporting a Vulnerability

If you find a security vulnerability, **please do not open a public issue.**

Instead:

1. Report it using GitHub's [Private Vulnerability Reporting](https://github.com/caglarbaranbora/Apple-Agent-Kit/security/advisories/new) feature, **or**
2. Send a detailed report to [maintainer email here].

Please try to include:
- A short description of the vulnerability
- The affected file/Skill/Knowledge Contract
- Steps to reproduce (if possible)
- Potential impact

## Response Process

- We aim to acknowledge your report within 48 hours.
- For confirmed vulnerabilities, a remediation timeline will be shared.
- The vulnerability will be publicly disclosed after a fix is released (credit given to the reporter if desired).

## Scope

This repo contains an npm installer (`npx apple-agent-kit`) and a Claude Code plugin marketplace. Pay particular attention to:
- Command execution / file-writing behavior inside `bin/install.js`
- Integrity of the marketplace/plugin manifest against malicious Skill/Knowledge Contract injection
