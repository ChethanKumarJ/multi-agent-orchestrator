"""Multi-agent graph - v1, roles are pretty dumb but work."""
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

class State(TypedDict):
    task: str
    files: List[str]
    code: str
    review: str
    rounds: int

def researcher(state: State) -> State:
    # TODO: actually use the codebase-context-mcp here instead of guessing
    prompt = f"You are a researcher. Task: {state['task']}\nList 3-5 files that are likely relevant. Just list paths."
    resp = llm.invoke(prompt)
    # naive parse - works ok for now
    files = [line.strip("- ").strip() for line in resp.content.split("\n") if line.strip()]
    return {**state, "files": files[:5]}

def coder(state: State) -> State:
    prompt = f"""You are a coder. Task: {state['task']}
Relevant files: {state['files']}
Previous review (if any): {state.get('review', 'none')}

Write the code change. Be concise, just the diff / new code."""
    resp = llm.invoke(prompt)
    return {**state, "code": resp.content}

def reviewer(state: State) -> State:
    prompt = f"""You are a reviewer. Task: {state['task']}
Proposed code:
{state['code']}

Critique it. If it's good, say 'LGTM'. Otherwise list issues."""
    resp = llm.invoke(prompt)
    rounds = state.get("rounds", 0) + 1
    return {**state, "review": resp.content, "rounds": rounds}

def should_continue(state: State) -> str:
    # stop after 3 rounds or if reviewer is happy
    # learned this after a $12 infinite loop lol
    if state.get("rounds", 0) >= 3:
        return END
    if "LGTM" in state.get("review", ""):
        return END
    return "coder"

def build_graph():
    g = StateGraph(State)
    g.add_node("researcher", researcher)
    g.add_node("coder", coder)
    g.add_node("reviewer", reviewer)

    g.set_entry_point("researcher")
    g.add_edge("researcher", "coder")
    g.add_edge("coder", "reviewer")
    g.add_conditional_edges("reviewer", should_continue, {"coder": "coder", END: END})
    return g.compile()

if __name__ == "__main__":
    import sys
    task = sys.argv[1] if len(sys.argv) > 1 else "add hello world"
    graph = build_graph()
    result = graph.invoke({"task": task, "files": [], "code": "", "review": "", "rounds": 0})
    print("=== CODE ===")
    print(result["code"])
    print("\n=== REVIEW ===")
    print(result["review"])
