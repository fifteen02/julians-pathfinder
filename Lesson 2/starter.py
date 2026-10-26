"""Lesson 2: file-based practice. Run with --help for test options."""
MOD = 1_000_000_007

def dice_table(n):
    """Count ordered sequences of faces 1..6 with total n, modulo MOD."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


def dice_123(n):
    """Count ordered sequences of faces 1..3 with total n, modulo MOD."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


def grid_table(rows):
    """Count top-left to bottom-right paths moving right or down, modulo MOD. A star is blocked."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True  # keep the folder free of __pycache__
    from runner import main
    raise SystemExit(main({'dice': dice_table, 'dice123': dice_123, 'grid': grid_table}))
