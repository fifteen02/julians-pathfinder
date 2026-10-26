"""Shared file loader and test runner; no problem-solving code lives here."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def load_input(problem, path):
    """Translate a plain-text input file into the function's arguments."""
    words = path.read_text().split()
    if problem in ('staircase', 'stride13', 'dice', 'dice123'):
        return (int(words[0]),)
    if problem == 'frog':
        n = int(words[0])
        heights = list(map(int, words[1:]))
        if len(heights) != n:
            raise ValueError('The height count does not match n.')
        return (heights,)
    if problem == 'grid':
        n = int(words[0])
        rows = words[1:]
        if len(rows) != n or any(len(row) != n for row in rows):
            raise ValueError('Expected n rows, each containing n cells.')
        return (rows,)
    if problem == 'tower':
        # Original format: t towers, each with n followed by n boss types.
        t = int(words[0]); cursor = 1; towers = []
        for _ in range(t):
            n = int(words[cursor]); cursor += 1
            towers.append(list(map(int, words[cursor:cursor + n])))
            cursor += n
        if cursor != len(words):
            raise ValueError('Unexpected tower data.')
        return (towers,)
    if problem == 'array':
        n, m = map(int, words[:2])
        values = list(map(int, words[2:]))
        if len(values) != n:
            raise ValueError('The entry count does not match n.')
        return (values, m)
    if problem == 'feast':
        return tuple(map(int, words))
    if problem == 'hps':
        n, budget = map(int, words[:2])
        john = words[2:]
        if len(john) != n:
            raise ValueError('The round count does not match n.')
        return (john, budget)
    raise ValueError('Unknown problem: ' + problem)


def evaluate(function, problem, path):
    args = load_input(problem, path)
    if problem == 'tower':
        return '\n'.join(str(function(bosses)) for bosses in args[0])
    return str(function(*args))


def main(functions):
    parser = argparse.ArgumentParser(description='Run a lesson function on file-based tests.')
    parser.add_argument('--problem', choices=sorted(functions), help='Default: every problem in this lesson')
    parser.add_argument('--size', choices=['small', 'medium', 'large', 'all'], default='small')
    parser.add_argument('--file', type=Path, help='One custom .in file; also specify --problem')
    parser.add_argument('--timeout', type=float, default=30, help='Seconds allowed per test (default 30)')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if args.file and not args.problem:
        parser.error('--file needs --problem')
    if args.worker:
        try:
            print(evaluate(functions[args.problem], args.problem, args.file))
        except NotImplementedError:
            print('NOT IMPLEMENTED: complete the function in starter.py.', file=sys.stderr)
            return 2
        except RecursionError:
            print('RECURSION LIMIT: the call chain is too deep. Python stops at about 1,000 nested calls, '
                  'so recursive versions are for small and edge files; use an iterative loop.', file=sys.stderr)
            return 3
        return 0
    if args.file:
        path = args.file.resolve()
        jobs = [(args.problem, path, path.with_suffix('.out'))]
    else:
        manifest = json.loads((ROOT / 'test-cases' / 'manifest.json').read_text())
        jobs = [(case['problem'], ROOT / 'test-cases' / case['input'], ROOT / 'test-cases' / case['output'])
                for case in manifest if (not args.problem or args.problem == case['problem'])
                and (args.size == 'all' or args.size == case['size'])]
    if not jobs:
        parser.error('No matching test files.')
    failures = 0
    script = str(Path(sys.argv[0]).resolve())
    for problem, path, expected_path in jobs:
        start = time.perf_counter()
        try:
            run = subprocess.run([sys.executable, '-B', script, '--worker', '--problem', problem,
                                  '--file', str(path)], capture_output=True, text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            print(f'TIMEOUT {problem}/{path.name}: exceeded {args.timeout:g}s')
            failures += 1
            continue
        elapsed = time.perf_counter() - start
        if run.returncode:
            print(f'FAIL {problem}/{path.name}: {(run.stderr or run.stdout).strip()}')
            failures += 1
            continue
        actual = run.stdout.strip()
        if not expected_path.exists():
            print(f'OUTPUT {problem}/{path.name}: {actual}')
            print('No matching .out file: this result has not been checked.')
            continue
        expected = expected_path.read_text().strip()
        if actual.split() == expected.split():
            print(f'PASS {problem}/{path.name} ({elapsed:.3f}s including process startup)')
        else:
            print(f'FAIL {problem}/{path.name}: expected {expected[:120]!r}; got {actual[:120]!r}')
            failures += 1
    print(f'{len(jobs)} file(s) run; {failures} failure(s).')
    return 1 if failures else 0
