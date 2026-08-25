import json

import httpx

from .parser import extract_endpoints


# Simple fallback generator when no LLM
def fallback_generate(endpoint):
    """Generate a few basic test cases without LLM."""
    method, path, operation = endpoint
    cases = []
    # 1. Empty body for POST/PUT
    if method in ["POST", "PUT", "PATCH"]:
        cases.append({
            "method": method,
            "path": path,
            "body": {},
            "expected_status": 200,  # optimistic
            "description": "empty body"
        })
    # 2. Minimal body from schema (if any)
    body_schema = operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    if body_schema:
        # produce a minimal object
        minimal = {}
        props = body_schema.get("properties", {})
        for k, v in props.items():
            if v.get("type") == "string":
                minimal[k] = "test"
            elif v.get("type") == "integer":
                minimal[k] = 0
            elif v.get("type") == "boolean":
                minimal[k] = True
        if minimal:
            cases.append({
                "method": method,
                "path": path,
                "body": minimal,
                "expected_status": 200,
                "description": "minimal body"
            })
    # 3. GET without body
    if method == "GET":
        cases.append({
            "method": "GET",
            "path": path,
            "body": None,
            "expected_status": 200,
            "description": "no body"
        })
    return cases

async def generate_test_cases(spec, llm_url=None, llm_api_key=None, model="llama3"):
    """
    Generate test cases using LLM if available, else fallback.
    Returns list of test_case dicts: {method, path, body, expected_status, description}
    """
    endpoints = list(extract_endpoints(spec))
    all_cases = []
    if llm_url and llm_api_key:
        # Use LLM to generate
        async with httpx.AsyncClient(timeout=60) as client:
            for endpoint in endpoints:
                # Build prompt
                method, path, operation = endpoint
                prompt = f"""Given an API endpoint:
Method: {method}
Path: {path}
Operation description: {operation.get('description', '')}
Request body schema (if any): {json.dumps(operation.get('requestBody', {}), indent=2)}
Generate 3-5 diverse test cases (JSON array) each with:
- method (string)
- path (string)
- body (object or null)
- expected_status (integer)
- description (string)
Return only JSON array, no extra text."""
                try:
                    resp = await client.post(
                        llm_url,
                        headers={"Authorization": f"Bearer {llm_api_key}"},
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.7,
                            "max_tokens": 1000
                        }
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        content = data["choices"][0]["message"]["content"]
                        # Try to extract JSON
                        import re
                        json_match = re.search(r'\[.*\]', content, re.DOTALL)
                        if json_match:
                            cases = json.loads(json_match.group())
                            all_cases.extend(cases)
                        else:
                            # Fallback
                            all_cases.extend(fallback_generate(endpoint))
                    else:
                        all_cases.extend(fallback_generate(endpoint))
                except Exception:
                    all_cases.extend(fallback_generate(endpoint))
    else:
        # Fallback for all endpoints
        for endpoint in endpoints:
            all_cases.extend(fallback_generate(endpoint))
    return all_cases
