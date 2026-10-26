"""Lesson 5: file-based practice. Run with --help for test options."""
BEATS = {'H': 'S', 'P': 'H', 'S': 'P'}

def hps_table(john, budget):
    """Return the greatest number of wins using at most budget changes. First gesture is free."""
    # Write your solution here. Return the answer; do not print it.
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True  # keep the folder free of __pycache__
    from runner import main
    raise SystemExit(main({'hps': hps_table}))
