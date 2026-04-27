def print_header(model: str, max_attempts: int):
    print("=" * 60)
    print("  Competitive Programming Agent")
    print(f"  Model: {model}  |  Max attempts: {max_attempts}")
    print("=" * 60)


def print_attempt(attempt: int, max_attempts: int):
    print(f"\n[Agent] ── Attempt {attempt}/{max_attempts} ──")


def print_test_results(results: list[dict], attempt: int):
    passed = sum(1 for r in results if r["passed"])
    total  = len(results)

    print(f"\n{'='*60}")
    print(f"  ATTEMPT {attempt} — TEST RESULTS  ({passed}/{total} passed)")
    print(f"{'='*60}")

    for r in results:
        icon   = "✓" if r["passed"] else "✗"
        status = "PASS" if r["passed"] else ("TLE" if r["timed_out"] else "FAIL")

        print(f"\n  [{icon}] Test {r['test_num']} — {status}")
        if r["input"]:
            print(f"       Input:    {r['input'].strip()}")
        if r["expected"]:
            print(f"       Expected: {r['expected']}")
        print(f"       Got:      {r['actual'] or '(no output)'}")
        if r["stderr"]:
            print(f"       Error:    {r['stderr'][:150]}")

    print(f"\n{'='*60}\n")


def print_final(passed: bool, attempts: int):
    print("=" * 60)
    if passed:
        print(f"  ✓ ALL TESTS PASSED  (solved in {attempts} attempt(s))")
    else:
        print(f"  ✗ COULD NOT SOLVE after {attempts} attempt(s)")
    print("=" * 60)


def print_no_code_warning():
    print("[Agent] No code block found in response. Retrying...")


def print_solving():
    print("\n[Agent] Generating solution...\n")


def print_debugging():
    print("\n[Agent] Debugging failures...\n")
