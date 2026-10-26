"""Lesson 1: file-based practice. Run with --help for test options."""

def stairs_table(n):
    """Return the exact number of ordered routes to step n using jumps 1 or 2."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


def stairs_13(n):
    """Return the exact number of ordered routes to step n using jumps 1 or 3."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


def frog_table(heights):
    """Return the minimum total height-difference cost to the last stone."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


def frog_path(heights):
    """Return (cost, path), with stone indices from start to finish. On equal candidate costs keep predecessor i - 1."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True  # keep the folder free of __pycache__
    from runner import main
    raise SystemExit(main({'staircase': stairs_table, 'stride13': stairs_13, 'frog': frog_table, 'frog-path': frog_path}))
