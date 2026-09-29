"""Cost tracking - added after I burned $12 on an infinite review loop."""
import time
from dataclasses import dataclass, field

# rough pricing for gpt-4o-mini as of Sep 2026, update if it changes
INPUT_PER_1K = 0.00015
OUTPUT_PER_1K = 0.0006

@dataclass
class RunCost:
    input_tokens: int = 0
    output_tokens: int = 0
    start: float = field(default_factory=time.time)

    def add(self, inp: int, out: int):
        self.input_tokens += inp
        self.output_tokens += out

    @property
    def total_usd(self) -> float:
        return (self.input_tokens / 1000 * INPUT_PER_1K +
                self.output_tokens / 1000 * OUTPUT_PER_1K)

    def summary(self) -> str:
        elapsed = time.time() - self.start
        return (f"tokens: {self.input_tokens} in / {self.output_tokens} out, "
                f"cost: ${self.total_usd:.4f}, time: {elapsed:.1f}s")

# global for simplicity, don't judge
_current = RunCost()

def get_cost() -> RunCost:
    return _current

def reset():
    global _current
    _current = RunCost()
