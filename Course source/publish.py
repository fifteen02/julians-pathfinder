from pathlib import Path
import sys
sys.dont_write_bytecode=True
import shutil,zipfile,json,hashlib,re
from content import LESSONS
from compile_all import build_dir, clean_stray, KINDS
from build_teacher_books import NAMES as TEACHER_NAMES, DEST as TEACHER_DEST, OUT as TEACHER_OUT
import programs as P
ROOT=Path(__file__).resolve().parent.parent
HERE=Path(__file__).resolve().parent
# Publish only a complete, clean compiler run.
compiled = json.loads((HERE / 'compile-report.json').read_text())
assert {(r['lesson'], r['kind']) for r in compiled} == {(n, k) for n in range(1, 6) for k in KINDS}
assert all(r['ok'] and not r.get('warnings') for r in compiled), 'Resolve compiler errors and warnings before publishing.'
for n in range(1, 6):
    assert not any((ROOT / f'Lesson {n}' / name).exists() for name in ('worksheet.pdf', 'worksheet.tex')), 'Move retired worksheets to the Trash before publishing.'

# The teacher books must have been compiled from their current sources.
teacher_report=json.loads((HERE/'teacher-books-compile-report.json').read_text())
assert {r['name'] for r in teacher_report} == set(TEACHER_NAMES)
for r in teacher_report:
    assert r['ok'] and not r.get('warnings'), r
    assert r['source_sha256'] == hashlib.sha256((TEACHER_DEST/(r['name']+'.tex')).read_bytes()).hexdigest(), 'Rebuild the teacher books before publishing.'
    shutil.copy2(TEACHER_OUT/(r['name']+'.pdf'), TEACHER_DEST/(r['name']+'.pdf'))
for n in range(1,6):
    assert not any((ROOT/f'Lesson {n}'/f'{kind}.{ext}').exists() for kind in ('tutorial','teacher') for ext in ('pdf','tex')), 'Retire the separate teacher handouts before publishing.'

# Lines of every complete function; a student pack must not contain them.
import inspect
def solution_fragments():
    frags=set()
    for name,fn in vars(P).items():
        if inspect.isfunction(fn):
            body=[l.strip() for l in inspect.getsource(fn).splitlines()[1:] if l.strip()]
            for i in range(len(body)-2): frags.add('\n'.join(body[i:i+3]))
    return frags
FRAGMENTS=solution_fragments()
def leaks(text):
    lines=[l.strip() for l in text.splitlines() if l.strip()]
    return [w for w in ('\n'.join(lines[i:i+3]) for i in range(len(lines)-2)) if w in FRAGMENTS]
for L in LESSONS:
    dest=ROOT/f'Lesson {L["n"]}'
    for kind in KINDS:
        if kind not in ('tutorial','teacher'): shutil.copy2(build_dir(L['n'])/f'{kind}.pdf',dest/f'{kind}.pdf')
    with zipfile.ZipFile(dest/'student-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['worksheet-printer-friendly.pdf','lesson.ipynb','starter.py','runner.py','PRACTICE.txt']: z.write(dest/name,name)
        for path in (dest/'test-cases').rglob('*'):
            if path.is_file(): z.write(path,path.relative_to(dest))
        z.writestr('START-HERE.txt',f'''Lesson {L['n']}: {L['subtitle']}
Print worksheet-printer-friendly.pdf: the questions, with an illustrated cover and a
link to the student notebook in Colab. Use separate paper or the notebook for working.
Open lesson.ipynb in Jupyter or upload it to Google Colab. Choose Python 3.
Run the setup cell first, then work from top to bottom. Shift+Enter runs a cell.
Write-a-program questions have stub cells; complete them yourself.
Their checks report "Not implemented yet" until you replace the starter code.
Cells labelled "Worked example" explain an idea; read them after trying.
The notebook needs no extra data files or Python packages.
For local Python practice, edit starter.py and run python3 starter.py.
PRACTICE.txt explains medium/large tests and selecting an individual problem.
Keep runner.py and test-cases/ beside starter.py. Solutions are not in this pack.
Python stops recursion at about 1,000 nested calls, so recursive versions are for
small inputs and the small and edge files only.
''')
        names=z.namelist()
        assert not any(name in names for name in ['solution.py','solutions.py','teacher-notebook.ipynb'])
        assert not any('__pycache__' in name or name.endswith('.pyc') for name in names)
    with zipfile.ZipFile(dest/'student-pack.zip') as z:
        notebook=json.loads(z.read('lesson.ipynb'))
        code='\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code')
        for name in ['starter.py','runner.py']: code+='\n'+z.read(name).decode()
        # Worked examples are allowed: they are explanations, not exercise answers.
        from build_course import student_mode, codes
        allowed_text='\n'.join(inspect.getsource(getattr(P,fn)) for u in L['units'] for fn in codes(u) if student_mode(L,u,fn)=='example')
        if L['n'] == 1:
            from recursion_intro import PROVIDED_TRACE_FUNCTIONS
            # Students trace these supplied functions; their returned values stay hidden.
            allowed_text += '\n' + '\n'.join(inspect.getsource(getattr(P, fn)) for fn in PROVIDED_TRACE_FUNCTIONS)
        bad=[w for w in leaks(code) if w not in leaks(allowed_text)]
        assert not bad,(L['n'],bad[:3])
        assert 'worksheet.pdf' not in z.namelist()
        assert {'worksheet-printer-friendly.pdf','lesson.ipynb','starter.py','runner.py','PRACTICE.txt','START-HERE.txt'} <= set(z.namelist())
text='''DYNAMIC PROGRAMMING: FROM RECURSION TO EFFICIENT SOLUTIONS
Five complete lessons

Start with Lesson 1. These are the full lesson packs, not the slide preview.
Each lesson has a two-hour route with board work, coding and an exit question.
Timing is a guide. If the group is new to Python, carry unfinished work into
another session. Lesson 1 includes the full staircase and Frog progressions. Use an eight-minute
recursion refresher, finish staircase by minute 60, and teach Frog after the break.
The four refresher exercises remain available; choose one in class if students
already know recursion. L1-21 adds recovering a cheapest Frog path as a 15-20 minute
extension or follow-up, outside the two-hour core. Dice is in Lesson 2.
The optional dice moving-sum exercise can be skipped.

THE COURSE
'''
for L in LESSONS:
    text+=f'Lesson {L["n"]}: {L["subtitle"]}\n  Main idea: {L["title"]}.\n'
text+='''
IN THE TEACHER FOLDER
  teacher-book.pdf: one detailed preparation book covering all five lessons, with reasoning, worked examples, diagrams and complete code.
  teacher-class-notes.pdf: one classroom companion covering all five lessons, with timetables, questions, hints, answers and code.
  Both books have linked contents and continuous page numbering. Their LaTeX sources, fonts and artwork are included.

IN EACH LESSON FOLDER
  worksheet_answers.pdf: worked answers in worksheet order, completed tables and full code.
  worksheet-printer-friendly.pdf: the student worksheet: illustrated cover, compact question pages and a Colab link.
  lesson.ipynb: student notebook, worked examples and unfinished exercises.
  slides.pdf: questions followed immediately by answers; code follows its answer.
  slides.tex: editable LaTeX Beamer source (no PowerPoint needed).
  teacher-notebook.ipynb: completed notebook for the teacher.
  starter.py: student function skeletons with a ready-to-run test harness.
  runner.py: shared file loader and test runner; no solution algorithms.
  solution.py: separate completed iterative solutions using the same tests.
  solutions.py: all classroom variants, including recursive versions.
  test-cases/: small, medium and large inputs, expected outputs and edge cases.
  PRACTICE.txt: commands, formats, dataset sizes and timeout behaviour.
  programs/: complete original-judge input/output programs.
  student-pack.zip: worksheet, notebook, starter, runner and datasets; excludes solutions.

Question IDs such as L1-04 match across all formats.
There is one student worksheet, worksheet-printer-friendly.pdf, with compact question pages;
students use separate paper or the notebook for working. Colab links also appear on
the slides and Teacher Class Notes. Teacher Book has no Colab link.
Teacher Class Notes includes completed trace tables as well as code answers.
Give students student-pack.zip. The complete course ZIP contains the answer keys.
The notebooks are self-contained and need only Python's standard library.
In lesson.ipynb, write-a-program questions have stub cells; the teacher notebook
has the complete code. Python stops recursion at about 1,000 nested calls, so the
recursive versions are for small inputs and the small and edge test files only.

PREPARATION
1. Read the relevant lesson in Teacher/teacher-book.pdf and try its examples.
2. Keep Teacher/teacher-class-notes.pdf open for prompts and expected answers.
3. Print worksheet-printer-friendly.pdf for each student.
4. Open slides.pdf in presentation mode. Advance once to reveal each answer.
5. Share the student pack and test that one notebook cell runs on a student's device.

EDITING
Each PDF has a matching .tex source, with common.tex, fonts/ and assets/ beside it.
Use XeLaTeX. In lesson folders, main.tex opens the slides. In Teacher/, main.tex
opens Teacher Book. Teacher books need three passes to resolve cross-references.
The Python files in Course source/ generate consistent material across formats.
book_l1.py to book_l5.py hold the narrative (assembled by book_content.py), with
figures in book_figures.py and measured numbers in book_kit.py.
book_walkthroughs.py adds the detailed state/value and recursion-to-table examples; build_books.py
generates the lesson preparation chapters; build_teacher_books.py combines them
and the classroom notes into the two volumes in Teacher/.
make_practice.py generates the starter files, completed solutions and test data.
Order: build_course.py regenerates every source, notebook, practice file and
dataset; compile_all.py compiles the classroom PDFs and internal lesson chapters
into Course source/build/, then builds the two teacher books; then run verify.py, verify_practice.py, verify_sheets.py,
verify_answers.py, verify_pdfs.py, verify_starting_points.py, verify_lesson_alignment.py, verify_notebooks.py
and verify_books.py plus verify_teacher_books.py
(the teacher books: counts, Python notes, judge programs, layout), and inspect the
rendered PDFs (render_all.py, render_books.py). publish.py copies the PDFs into
the lesson folders, writes this file and the student packs, builds the course ZIP
and removes __pycache__ folders.
The generator uses the bundled Lesson 1 fonts and each lesson's existing artwork.
Original problem links appear in tutorials and notebooks.
All printed materials and slides follow the Distributing Candies design: white
pages, charcoal headings, Avenir Next, JetBrains Mono and the original partner logos.
The tutor books use a narrow reading column and classroom references in the margin.
candies_style.py is the shared visual template; restyle_course.py rebuilds only
visual sources, preserving notebooks, Python implementations and datasets.

VALIDATION
17 published PDFs: three classroom PDFs per lesson and two combined teacher books.
The ten original teacher chapters remain private build intermediates.
All @PAIRS@ question/answer slide pairs checked.
@CHECKS@ program checks, including independent small-case searches and judge adapters.
All ten notebooks validated and executed in fresh Jupyter kernels.
@PRACTICE@ practice tests passed with independently checked outputs; runner error paths verified.
Reports are in Course source/. Actual classroom pacing has not been tested.

PRESERVED MATERIAL
The older Candies material remains separately in Future lesson - Distributing Candies.
Lesson 0 was distributed across Lessons 1-5 and removed from the active course.
Its recovery copy is Archive/Retired Lesson 0.zip. The original Frog datasets are
in Archive/Legacy Frog datasets (removed from Lesson 1). Slide preview remains separate.
Neither the retired archive nor Slide preview is included in this course ZIP.
'''
checks=re.search(r'PASS: (\d+) checks',(HERE/'verification.txt').read_text()).group(1)
practice=sum(len(json.loads((ROOT/f'Lesson {L["n"]}/test-cases/manifest.json').read_text())) for L in LESSONS)
text=text.replace('@CHECKS@',f'{int(checks):,}').replace('@PRACTICE@',str(practice)).replace('@PAIRS@',str(sum(len(L['units']) for L in LESSONS)))
(ROOT/'START-HERE.txt').write_text(text)
clean_stray()
files=[ROOT/'START-HERE.txt',ROOT/'REVIEW-lessons-1-5.md']
for L in LESSONS:
    directory=ROOT/f'Lesson {L["n"]}'
    files += [p for p in directory.rglob('*') if p.is_file() and not any(x in p.relative_to(directory).parts for x in ['build','__pycache__']) and p.name!='.DS_Store' and not (p.parent==directory and (p.suffix in ('.aux','.log','.out','.toc','.nav','.snm','.vrb','.listing') or p.name.endswith('.synctex.gz'))) and p.suffix!='.pyc']
files += [p for p in TEACHER_DEST.rglob('*') if p.is_file() and p.suffix not in ('.aux','.log','.out','.toc','.pyc') and p.name!='.DS_Store']
source=ROOT/'Course source'
files += [p for p in source.iterdir() if p.is_file() and (p.suffix in ('.py','.json') or p.name.endswith('verification.txt') or p.name=='retirement.txt')]
archive=ROOT/'Lessons 1-5.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(set(files)): z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if n.endswith('.pdf') and '/assets/' not in n])==17
    assert not any('__pycache__' in n or n.endswith('.pyc') or '/build/' in n or 'legacy-frog' in n for n in z.namelist())
    for n in z.namelist():
        if n.endswith('student-pack.zip'):
            import io
            with zipfile.ZipFile(io.BytesIO(z.read(n))) as pack:
                assert not any(x in pack.namelist() for x in ['solution.py','solutions.py','teacher-notebook.ipynb']),n
clean_stray()
print(f'Published 17 PDFs (including two teacher books) and 5 student packs. Complete archive: {archive.stat().st_size/1024/1024:.1f} MB; {len(set(files))} files.')
