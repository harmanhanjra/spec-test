# SpecTest

AI-powered API contract testing.

## Overview

SpecTest ingests an OpenAPI specification, generates diverse test cases (using LLM or fallback), runs them against a live API, and produces a structured report.

## Features

- Parse OpenAPI v3 specifications
- Generate test cases with LLM (OpenAI-compatible) or fallback heuristics
- Execute requests and compare responses
- Output JSON, Markdown, or JUnit XML reports
- Configurable timeout, output, and LLM settings

## Installation

```bash
uv venv .venv
uv pip install -e ".[test]"
```

## Usage

```bash
spec-test --spec openapi.yaml --target https://api.example.com
```

Options:
- `--spec` : OpenAPI spec file (YAML/JSON)
- `--target` : Base URL of the API to test
- `--llm-url` : LLM endpoint (env: SPEC_TEST_LLM_URL)
- `--llm-api-key` : LLM API key (env: SPEC_TEST_LLM_API_KEY)
- `--model` : Model name (default: llama3)
- `--format` : Output format (json, markdown, junit)
- `--output` : Output file path
- `--timeout` : HTTP request timeout (seconds)

## Testing

```bash
pytest tests -q
```

## License

MIT