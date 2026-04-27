from agent.llm import llm_solve, llm_debug
from utils.executor import extract_code, run_tests
from utils.printer import (
    print_header,
    print_attempt,
    print_test_results,
    print_final,
    print_no_code_warning,
)


def run_agent(
    problem: str,
    test_cases: list[dict],
    max_attempts: int = 3,
    model: str = "llama-3.3-70b-versatile",
) -> dict:
    
    print_header(model, max_attempts)

    code         = None
    last_results = []
    history      = []

    for attempt in range(1, max_attempts + 1):
        print_attempt(attempt, max_attempts)

        
        if attempt == 1:
            response = llm_solve(problem, model)
        else:
            failures = [r for r in last_results if not r["passed"]]
            response = llm_debug(problem, code, failures, model)

        
        new_code = extract_code(response)
        if not new_code:
            print_no_code_warning()
            history.append({"attempt": attempt, "response": response, "code": None, "results": []})
            continue
        code = new_code

        
        results, all_passed = run_tests(code, test_cases)
        last_results = results
        print_test_results(results, attempt)
        history.append({"attempt": attempt, "response": response, "code": code, "results": results})

        if all_passed:
            print_final(True, attempt)
            return {"code": code, "passed": True, "attempts": attempt, "history": history}

    print_final(False, max_attempts)
    return {"code": code, "passed": False, "attempts": max_attempts, "history": history}
