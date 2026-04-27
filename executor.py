import re
import subprocess
import sys
import tempfile
import os


def extract_code(text: str) -> str | None:
    """Extract the first ```python ... ``` block from LLM response."""
    match = re.search(r"```python\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def run_code(code: str, stdin_input: str = "", timeout: int = 10) -> dict:
    """
    Execute Python code in a subprocess with optional stdin.

    Returns:
        dict with keys: stdout, stderr, exit_code, timed_out
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name

    try:
        res = subprocess.run(
            [sys.executable, path],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout":    res.stdout.strip(),
            "stderr":    res.stderr.strip(),
            "exit_code": res.returncode,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout":    "",
            "stderr":    "Time Limit Exceeded",
            "exit_code": -1,
            "timed_out": True,
        }
    finally:
        os.unlink(path)


def run_tests(code: str, test_cases: list[dict]) -> tuple[list[dict], bool]:
    """
    Run code against all test cases.

    Args:
        code:       Python source code string
        test_cases: List of {"input": str, "expected": str}

    Returns:
        (results, all_passed)
    """
    results = []
    for i, tc in enumerate(test_cases, 1):
        res      = run_code(code, stdin_input=tc.get("input", ""))
        actual   = res["stdout"]
        expected = tc.get("expected", "").strip()
        passed   = (actual == expected) if expected else not res["stderr"]

        results.append({
            "test_num":  i,
            "input":     tc.get("input", ""),
            "expected":  expected,
            "actual":    actual,
            "stderr":    res["stderr"],
            "passed":    passed,
            "timed_out": res["timed_out"],
        })

    all_passed = all(r["passed"] for r in results)
    return results, all_passed
