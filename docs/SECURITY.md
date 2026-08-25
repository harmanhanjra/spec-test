# Security

## Threat Model

- **Spec injection**: Untrusted OpenAPI files could contain malicious YAML. We use `openapi-spec-validator` which performs safe parsing and validation; no `eval` or dynamic imports.
- **Network**: Runner makes outbound HTTP requests to `--target`. We enforce timeouts (default 30s) and limit redirects (httpx default). We do not follow unsafe redirects to internal networks.
- **LLM prompts**: User-controlled endpoint descriptions are included in prompts. We do not execute any code from the LLM response; we only parse JSON and treat as test case data. Risks are limited to prompt injection that could cause the LLM to generate unexpected cases, but these are still just HTTP requests.
- **Secrets**: LLM API keys are read from environment variables, never logged or persisted. The CLI does not store any secrets.

## Hardening

- Use `os.environ` for credentials; avoid hardcoded defaults.
- No use of `subprocess` or `shell=True`.
- All file operations use `Path` and safe paths.
- Timeouts on all network operations.
- Input validation: spec is validated against OpenAPI schema.

## Auditing

Run:

```bash
bandit -r src/ -f txt -o bandit-report.txt
ruff check src/ tests/
```

## Accepted Risks

- B603 (subprocess call) is not applicable (we don't use subprocess).
- B607 (start_process_with_a_shell) not applicable.
- Bandit may flag use of `yaml.load()` but we use `yaml.safe_load` implicitly via openapi-spec-validator; we do not call `yaml.load` directly.
- Network requests to external servers are inherently risky; we mitigate with timeouts and user-controlled target.

## Future Improvements

- Add TLS certificate validation (default in httpx).
- Implement rate limiting for outbound requests.
- Add a "dry-run" flag to preview cases without execution.