import json
from groq import Groq
from agent.prompts import SOLVER_PROMPT, DEBUGGER_PROMPT, TEST_GENERATOR_PROMPT
from utils.printer import print_solving, print_debugging

client = Groq()


def _stream(messages: list[dict], model: str) -> str:
    
    response = []
    stream = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        print(text, end="", flush=True)
        response.append(text)
    print()
    return "".join(response)


def llm_solve(problem: str, model: str) -> str:
    
    print_solving()
    return _stream(
        messages=[
            {"role": "system", "content": SOLVER_PROMPT},
            {"role": "user",   "content": f"Problem:\n{problem}"},
        ],
        model=model,
    )


def llm_debug(problem: str, code: str, failures: list[dict], model: str) -> str:
    
    print_debugging()

    failure_text = ""
    for r in failures:
        failure_text += f"\n--- Test {r['test_num']} FAILED ---\n"
        failure_text += f"Input:\n{r['input']}\n"
        failure_text += f"Expected: {r['expected']}\n"
        failure_text += f"Got:      {r['actual']}\n"
        if r["stderr"]:
            failure_text += f"Error:    {r['stderr']}\n"

    user_msg = (
        f"Problem:\n{problem}\n\n"
        f"Current code:\n```python\n{code}\n```\n\n"
        f"Failed tests:{failure_text}"
    )

    return _stream(
        messages=[
            {"role": "system", "content": DEBUGGER_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
        model=model,
    )


def llm_generate_tests(problem: str, model: str) -> list[dict]:
    
    print("\n[Agent] Auto-generating test cases...\n")

    response = client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": TEST_GENERATOR_PROMPT},
            {"role": "user",   "content": f"Problem:\n{problem}"},
        ],
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        test_cases = json.loads(raw)
        print(f"[Agent] Generated {len(test_cases)} test cases!\n")
        for i, tc in enumerate(test_cases, 1):
            print(f"  Test {i}: input={repr(tc['input'])}  expected={repr(tc['expected'])}")
        print()
        return test_cases
    except json.JSONDecodeError:
        print("[Agent] Could not parse test cases. Using empty list.\n")
        return []
