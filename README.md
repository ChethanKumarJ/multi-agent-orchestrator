# multi-agent-orchestrator

Multi-agent system with LangGraph - researcher, coder, reviewer agents that actually talk to each other.

Got tired of single-agent loops that just spin. Wanted to see if splitting roles helps on real tasks like "add a feature" or "fix this bug".

## Quick start

```bash
pip install -e .
python -m src.graph "add input validation to the login form"
```

## How it works

- `researcher` - explores repo, finds relevant files (currently just LLM guessing, want to plug in codebase-context-mcp here)
- `coder` - writes the change
- `reviewer` - critiques it, sends back if needed. Says `LGTM` when happy.

They pass messages via LangGraph state. Max 3 review rounds, then it gives up (learned that the hard way - infinite loops are expensive).

Added a dumb router: if task looks trivial (typo, rename), skip the reviewer entirely. Saves ~40% tokens on small tasks.

## Cost tracking

See `src/cost.py`. After adding the 3-round cap and router:

- trivial task: ~$0.02, 8s
- medium task (add validation): ~$0.15, 45s
- before caps: had one run hit $12. Never again.

## What I'd do next

- [ ] plug in real code search instead of LLM guessing files
- [ ] parallelize researcher + add a tester agent
- [ ] queue + worker model for scaling (right now it's all in-process)

## Limitations

This is a weekend project. No sandboxing, no real repo understanding, reviewer is pretty naive. Don't point it at prod.
