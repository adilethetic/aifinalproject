# CP Agent 

An agentic AI that automatically solves competitive programming problems using Groq LLM.

## How it works

The agent uses 3 AI calls in a loop:

```
Problem Statement
      ↓
[Test Generator LLM] - auto-generates 5 test cases
      ↓
[Solver LLM] - generates Python solution
      ↓
[Run Tests] - all pass? → ✅ Done
      ↓ (some fail)
[Debugger LLM] - sees failures, fixes code
      ↓
[Run Tests again] - repeat up to max_attempts
```

## Project Structure

```
aiprojectfinal/
├── main.py              - entry point
├── requirements.txt     - dependencies
├── .env                 - API key
├── agent/
│   ├── __init__.py
│   ├── prompts.py       - system prompts for each LLM role
│   ├── llm.py           - Groq API calls with streaming
│   └── solver.py        - main agentic loop
└── utils/
    ├── __init__.py
    ├── executor.py      - code extraction & subprocess execution
    └── printer.py       - terminal output helpers
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/adilethetic/aiprojectfinal.git
cd aiprojectfinal
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free (no credit card needed)
- Create an API key

### 5. Create `.env` file
```
GROQ_API_KEY= key
```

### 6. Run
```bash
python main.py
```

## Usage

1. Run `python main.py`
2. Paste any competitive programming problem
3. Type `END` on a new line when done
4. Press Enter for default max attempts (3)
5. Watch the agent solve it automatically!

## Example

```
Paste your problem (type END on a new line when done):

Given an array of integers nums and an integer target,
return indices of the two numbers that add up to target.
END

[Agent] Auto-generating test cases...
[Agent] Generated 5 test cases!

[Agent] Attempt 1/3
[Agent] Generating solution...

ATTEMPT 1 — TEST RESULTS (3/3 passed)
  [✓] Test 1 — PASS
  [✓] Test 2 — PASS
  [✓] Test 3 — PASS

✓ ALL TESTS PASSED (solved in 1 attempt)
```

## Models

| Model | Speed | Quality |
|---|---|---|
| `llama-3.3-70b-versatile` | Medium | Best (default) |
| `llama-3.1-8b-instant` | Fastest | Good |
| `mixtral-8x7b-32768` | Medium | Long context |

## Tech Stack

- **Groq** — LLM API (fast inference)
- **python-dotenv** — environment variables
- **subprocess** — code execution & testing
