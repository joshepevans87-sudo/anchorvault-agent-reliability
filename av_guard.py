
"""
AnchorVault Agent Reliability Framework
AV-Guard v0.1.0

Offline authorization policy evaluator.
No API keys, external dependencies or network calls.
"""

from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REVIEW = "REVIEW"


@dataclass(frozen=True)
class Action:
    agent: str
    operation: str
    target: str


POLICY = {
    ("research", "read", "public_data"): Decision.ALLOW,
    ("research", "write", "customer_data"): Decision.DENY,
    ("moderator", "read", "chat"): Decision.ALLOW,
    ("moderator", "ban", "viewer"): Decision.REVIEW,
    ("moderator", "delete", "message"): Decision.REVIEW,
    ("sales", "read", "inventory"): Decision.ALLOW,
    ("sales", "update", "price"): Decision.REVIEW,
    ("sales", "transfer", "funds"): Decision.DENY,
}


def evaluate(action: Action) -> Decision:
    """Evaluate an action against an explicit policy."""
    key = (action.agent, action.operation, action.target)
    return POLICY.get(key, Decision.DENY)


def run_benchmark():
    """Run deterministic authorization test cases."""

    cases = [
        (Action("research", "read", "public_data"),
         Decision.ALLOW),
        (Action("research", "write", "customer_data"),
         Decision.DENY),
        (Action("moderator", "read", "chat"),
         Decision.ALLOW),
        (Action("moderator", "ban", "viewer"),
         Decision.REVIEW),
        (Action("moderator", "delete", "message"),
         Decision.REVIEW),
        (Action("sales", "read", "inventory"),
         Decision.ALLOW),
        (Action("sales", "update", "price"),
         Decision.REVIEW),
        (Action("sales", "transfer", "funds"),
         Decision.DENY),
        (Action("unknown", "read", "inventory"),
         Decision.DENY),
        (Action("research", "execute", "shell"),
         Decision.DENY),
    ]

    passed = 0

    print("AVARF | AV-Guard v0.1.0")
    print("=" * 60)

    for action, expected in cases:
        actual = evaluate(action)
        success = actual == expected
        passed += int(success)

        print(
            f"[{'PASS' if success else 'FAIL'}] "
            f"{action.agent}: {action.operation} "
            f"{action.target} -> {actual.value}"
        )

    total = len(cases)

    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {passed / total * 100:.1f}%")

    return passed == total


if __name__ == "__main__":
    raise SystemExit(0 if run_benchmark() else 1)
