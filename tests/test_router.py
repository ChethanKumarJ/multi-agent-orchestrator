"""test the trivial-task router - I kept over-engineering this"""
def is_trivial(task: str) -> bool:
    # v1 heuristic, probably too dumb but works for now
    trivial_keywords = ["typo", "rename", "format", "comment"]
    t = task.lower()
    return any(k in t for k in trivial_keywords) and len(t.split()) < 10

def test_trivial():
    assert is_trivial("fix typo in README")
    assert is_trivial("rename variable foo to bar")

def test_not_trivial():
    assert not is_trivial("add input validation to the login form with rate limiting")
    assert not is_trivial("refactor the auth module to use JWT")
