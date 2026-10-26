from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os, nbformat
from nbclient import NotebookClient
from compile_all import build_dir
ROOT=Path(__file__).resolve().parent.parent
os.environ['JUPYTER_PATH']=str(Path(__file__).resolve().parent/'.qa-jupyter/share/jupyter')
def run(job):
 n,name=job;source=ROOT/f'Lesson {n}/{name}.ipynb'
 nb=nbformat.read(source,as_version=4);nbformat.validate(nb)
 client=NotebookClient(nb,timeout=60,kernel_name='course-qa',resources={'metadata':{'path':str(source.parent)}})
 client.execute()
 output=build_dir(n)/f'{name}-executed.ipynb'
 nbformat.write(nb,output)
 return f'Lesson {n} {name}: schema valid; clean kernel execution passed'
with ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,[(n,name) for n in range(1,6) for name in ['lesson','teacher-notebook']]))
print('\n'.join(results))
(ROOT/'Course source/notebook-verification.txt').write_text('\n'.join(results)+'\n')
