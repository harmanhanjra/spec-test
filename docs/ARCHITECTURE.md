# Architecture

SpecTest is a modular CLI tool with four core components:

## Components

### 1. Parser (`parser.py`)
- Loads and validates OpenAPI v3 specs using `openapi-spec-validator`.
- Extracts endpoints (method, path, operation object).
- Simple and synchronous.

### 2. Generator (`generator.py`)
- Produces test cases for each endpoint.
- Two modes:
  - **LLM mode**: Calls an OpenAI-compatible endpoint with a prompt describing the endpoint; expects JSON array of test cases.
  - **Fallback mode**: Generates minimal cases (empty body, minimal body from schema, GET with no body).
- Asynchronous (uses `httpx.AsyncClient`).

### 3. Runner (`runner.py`)
- Executes HTTP requests for each test case against a target base URL.
- Uses `httpx.AsyncClient` with configurable timeout.
- Returns `TestResult` objects with status, body, and pass/fail status.

### 4. Reporter (`reporter.py`)
- Converts results to JSON, Markdown, or JUnit XML.
- Uses `jinja2` for potential templating (currently not used, but installed).

## Data Flow
1. User invokes CLI with `--spec` and `--target`.
2. Parser loads and validates spec.
3. Generator produces test cases (async).
4. Runner executes all cases concurrently.
5. Reporter formats and outputs.

## Design Decisions
- Asynchronous I/O for network-bound tasks (LLM calls and HTTP requests) to improve performance.
- Fallback generator ensures the tool works without LLM credentials.
- Test results are immutable dataclasses for predictable handling.
- Configuration via CLI flags and environment variables (for secrets).

## Future Extensibility
- Add support for more OpenAPI versions.
- Add authentication plugins (OAuth, API keys).
- Generate more sophisticated test cases with property-based testing.
- Add a server mode for continuous testing.