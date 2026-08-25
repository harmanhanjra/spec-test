import asyncio

import httpx


class TestResult:
    def __init__(self, case, status_code, response_body, error=None):
        self.case = case
        self.status_code = status_code
        self.response_body = response_body
        self.error = error
        self.passed = error is None and status_code == case.get("expected_status", 200)

async def run_one_test(client, case, base_url, timeout):
    method = case["method"]
    path = case["path"]
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    body = case.get("body")
    try:
        if method == "GET":
            resp = await client.get(url, timeout=timeout)
        elif method == "POST":
            resp = await client.post(url, json=body, timeout=timeout)
        elif method == "PUT":
            resp = await client.put(url, json=body, timeout=timeout)
        elif method == "PATCH":
            resp = await client.patch(url, json=body, timeout=timeout)
        elif method == "DELETE":
            resp = await client.delete(url, timeout=timeout)
        else:
            return TestResult(case, None, None, error=f"Unsupported method {method}")
        # Try to parse JSON body
        try:
            resp_body = resp.json()
        except Exception:
            resp_body = resp.text
        return TestResult(case, resp.status_code, resp_body)
    except Exception as e:
        return TestResult(case, None, None, error=str(e))

async def run_tests(test_cases, base_url, timeout=30):
    async with httpx.AsyncClient() as client:
        tasks = [run_one_test(client, case, base_url, timeout) for case in test_cases]
        results = await asyncio.gather(*tasks)
    return results
