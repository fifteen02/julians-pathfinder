from pathlib import Path
import subprocess,sys,tempfile,shutil,json
ROOT=Path(__file__).resolve().parent.parent
report=[]
for n in range(1,6):
    folder=ROOT/f'Lesson {n}'
    result=subprocess.run([sys.executable,'-B',str(folder/'solution.py'),'--size','all'],cwd='/tmp',capture_output=True,text=True,timeout=240)
    assert result.returncode==0,result.stdout+result.stderr
    cases=json.loads((folder/'test-cases/manifest.json').read_text())
    assert result.stdout.count('PASS ')==len(cases),result.stdout
    for problem in {x['problem'] for x in cases}:
        assert {'small','medium','large'}<={c['size'] for c in cases if c['problem']==problem}
    starter=subprocess.run([sys.executable,'-B',str(folder/'starter.py')],cwd='/tmp',capture_output=True,text=True)
    assert starter.returncode==1 and 'NOT IMPLEMENTED' in starter.stdout and 'PASS ' not in starter.stdout
    report.append(f'Lesson {n}: {len(cases)} solution tests passed from another working directory; unfinished starter correctly fails.')
    print(report[-1],flush=True)
with tempfile.TemporaryDirectory() as tmp:
    tmp=Path(tmp)
    shutil.copy2(ROOT/'Lesson 1/runner.py',tmp/'runner.py')
    shutil.copytree(ROOT/'Lesson 1/test-cases',tmp/'test-cases')
    for body,needle in [('return -1','expected'),('raise RecursionError','RECURSION LIMIT'),('while True: pass','TIMEOUT')]:
        (tmp/'sample.py').write_text('def solve(n):\n    '+body+'\nif __name__ == "__main__":\n    from runner import main\n    raise SystemExit(main({"staircase": solve}))\n')
        r=subprocess.run([sys.executable,'-B',str(tmp/'sample.py'),'--problem','staircase','--file',str(tmp/'test-cases/staircase/small.in'),'--timeout','0.3'],cwd='/tmp',capture_output=True,text=True)
        assert r.returncode==1 and needle in r.stdout,(needle,r.stdout,r.stderr)
    (tmp/'sample.py').write_text('def solve(n):\n    return 8\nif __name__ == "__main__":\n    from runner import main\n    raise SystemExit(main({"staircase": solve}))\n')
    r=subprocess.run([sys.executable,'-B',str(tmp/'sample.py'),'--problem','staircase','--file',str(tmp/'test-cases/staircase/small.in')],cwd='/tmp',capture_output=True,text=True)
    assert r.returncode==0 and 'PASS' in r.stdout
report.append('Runner checks passed: wrong answer, recursion error, timeout, custom file and completed starter function.')
(ROOT/'Course source/practice-verification.txt').write_text('\n'.join(report)+'\n')
print(report[-1])
