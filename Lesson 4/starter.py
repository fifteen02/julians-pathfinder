"""Lesson 4: file-based practice. Run with --help for test options."""

def feast_table(limit, a, b):
    """Return the greatest reachable fullness, eating a or b and drinking water at most once."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True  # keep the folder free of __pycache__
    from runner import main
    raise SystemExit(main({'feast': feast_table}))
