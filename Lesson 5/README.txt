LESSON 5 - Choose when to switch
Hoof, Paper, Scissors

FOR THE TEACHER
../Teacher/teacher-book.pdf: one detailed preparation book covering all five lessons.
../Teacher/teacher-class-notes.pdf: all five lesson plans, classroom questions, hints, answers and code.
worksheet_answers.pdf: questions in worksheet order, worked answers, completed tables and full code.
slides.pdf: questions immediately followed by answers; code continuations follow the answer.
teacher-notebook.ipynb: worked answers and completed exercise functions.
solutions.py: all complete classroom functions in one file. Recursive versions are for small inputs: Python stops recursion at about 1,000 nested calls.
solution.py: separate final iterative functions using the same test runner as starter.py.

GIVE STUDENTS
starter.py: function skeletons; run python3 starter.py for small and edge tests.
runner.py and test-cases/: loading, comparisons and small/medium/large datasets.
PRACTICE.txt: all commands, input formats and sizes.
worksheet-printer-friendly.pdf: the student worksheet: illustrated cover, compact question pages and a Colab link.
lesson.ipynb: questions, labelled worked examples and stub cells to complete; Python standard library only.
student-pack.zip contains the worksheet, notebook, starter.py, runner.py, test-cases/ and PRACTICE.txt; it excludes solutions.

OPEN THE NOTEBOOK
Open lesson.ipynb in Jupyter, or upload it to Google Colab. Select Python 3.
Run the setup cell, then proceed top to bottom. Shift+Enter executes a cell.
Exercise functions initially return None; checks say 'Not implemented yet' until completed.
Do not share teacher-notebook.ipynb or the complete folder as the student handout.

EDIT / REBUILD
Classroom PDFs have matching .tex files with common.tex, fonts and assets. The two teacher books and their sources are in ../Teacher/.
Course source/compile_all.py compiles all PDFs into Course source/build/ (outside this folder),
and Course source/publish.py copies the checked PDFs here.
To compile one file by hand, run XeLaTeX twice: xelatex slides.tex
main.tex opens slides.tex by default in the built-in editor.
Course source/build_course.py regenerates all lesson sources from the shared content.
Programs in programs/ include complete judge input/output adapters.

PALETTE
Matched to Distributing Candies: white #FFFFFF; charcoal #252525; muted grey #666666; code paper #F6F6F4. Avenir Next and JetBrains Mono; original partner logos.
