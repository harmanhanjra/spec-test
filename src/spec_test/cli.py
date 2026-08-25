import asyncio
from pathlib import Path

import click

from .generator import generate_test_cases
from .parser import load_spec
from .reporter import report_json, report_junit, report_markdown
from .runner import run_tests


@click.command()
@click.option("--spec", required=True, type=click.Path(exists=True), help="OpenAPI spec file (YAML/JSON)")
@click.option("--target", required=True, help="Base URL of the API to test")
@click.option("--llm-url", envvar="SPEC_TEST_LLM_URL", help="LLM endpoint URL (OpenAI-compatible)")
@click.option("--llm-api-key", envvar="SPEC_TEST_LLM_API_KEY", help="API key for LLM")
@click.option("--model", default="llama3", help="Model name for LLM")
@click.option("--format", "output_format", type=click.Choice(["json", "markdown", "junit"]), default="markdown")
@click.option("--output", type=click.Path(path_type=Path), help="Output file (default: stdout)")
@click.option("--timeout", default=30, help="HTTP request timeout in seconds")
def main(spec, target, llm_url, llm_api_key, model, output_format, output, timeout):
    """AI-powered API contract testing."""
    try:
        spec_data = load_spec(spec)
    except Exception as e:
        click.echo(f"Error loading spec: {e}", err=True)
        return 1

    # Generate test cases (could be async)
    test_cases = asyncio.run(generate_test_cases(spec_data, llm_url, llm_api_key, model))
    # Run tests
    results = asyncio.run(run_tests(test_cases, target, timeout))

    # Report
    if output_format == "json":
        report = report_json(results)
    elif output_format == "markdown":
        report = report_markdown(results)
    elif output_format == "junit":
        report = report_junit(results)
    else:
        click.echo("Unknown format", err=True)
        return 1

    if output:
        output.write_text(report)
    else:
        click.echo(report)

    # Exit code: 0 if all passed, 1 if any failure
    return 0 if all(r.passed for r in results) else 1

if __name__ == "__main__":
    main()
