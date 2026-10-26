"""Lesson 3: file-based practice. Run with --help for test options."""
MOD = 1_000_000_007

def tower_table(bosses):
    """Return the fewest points your friend pays. Your friend goes first; each turn takes 1 or 2 bosses."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


def array_rolling(values, m):
    """Count fillings of missing zeros using 1..m, neighbours differing by at most 1; modulo MOD."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True  # keep the folder free of __pycache__
    from runner import main
    raise SystemExit(main({'tower': tower_table, 'array': array_rolling}))
