import json
from typing import List

from .runner import TestResult


def report_json(results: List[TestResult]) -> str:
    data = {
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed)
        },
        "results": [
            {
                "method": r.case["method"],
                "path": r.case["path"],
                "expected_status": r.case.get("expected_status"),
                "actual_status": r.status_code,
                "passed": r.passed,
                "error": r.error
            }
            for r in results
        ]
    }
    return json.dumps(data, indent=2)

def report_markdown(results: List[TestResult]) -> str:
    lines = ["# API Test Results", ""]
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    lines.append(f"**Summary:** {passed} passed, {failed} failed of {total} total")
    lines.append("")
    lines.append("| Method | Path | Expected | Actual | Result |")
    lines.append("|--------|------|----------|--------|--------|")
    for r in results:
        result_mark = "✅" if r.passed else "❌"
        exp = r.case.get("expected_status", "N/A")
        act = r.status_code if r.status_code else "error"
        lines.append(f"| {r.case['method']} | {r.case['path']} | {exp} | {act} | {result_mark} |")
    return "\n".join(lines)

def report_junit(results: List[TestResult]) -> str:
    # Minimal JUnit XML
    import xml.etree.ElementTree as ET
    from xml.dom import minidom
    testsuite = ET.Element("testsuite", name="spec-test")
    for r in results:
        testcase = ET.SubElement(testsuite, "testcase",
            name=f"{r.case['method']} {r.case['path']}",
            classname="API Test")
        if not r.passed:
            failure = ET.SubElement(testcase, "failure")
            failure.text = f"Expected {r.case.get('expected_status')}, got {r.status_code}" if r.status_code else str(r.error)
    rough = ET.tostring(testsuite, "utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ")
