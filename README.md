# multi-agent-orchestrator

Multi-agent system with LangGraph - researcher, coder, reviewer agents that actually talk to each other.

Got tired of single-agent loops that just spin. Wanted to see if splitting roles helps on real tasks like "add a feature" or "fix this bug".

## Quick start

```bash
pip install -e .
python -m src.main "add input validation to the login form"
```

## How it works

- `researcher` - explores repo, finds relevant files
- `coder` - writes the change
- `reviewer` - critiques it, sends back if needed

They pass messages via LangGraph state. Max 3 review rounds, then it gives up (learned that the hard way - infinite loops are expensive).

## What I learned

Splitting roles helps for bigger tasks, but for small ones it's overkill and just burns tokens. Added a simple router to skip reviewer for trivial changes.

Cost tracking was eye-opening - see `src/cost.py`.
