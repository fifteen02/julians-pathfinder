# Dynamic Programming

## From Recursion to Efficient Solutions

A course built around tracing examples, finding repeated work, and writing recursive and iterative solutions.

## Teacher books

- [Teacher Book](Teacher/teacher-book.pdf): the detailed tutorial for all five lessons, with explanations, diagrams, step-by-step worked examples and complete code (120 pages).
- [Teacher Class Notes](Teacher/teacher-class-notes.pdf): lesson plans, classroom questions, hints, answers and code (56 pages).

Both books have linked contents and continuous page numbers. Their editable LaTeX sources are in `Teacher/`.

## Lessons

| Lesson | Problems | Student notebook |
| --- | --- | --- |
| [Lesson 1](Lesson%201/) | Staircase and Frog | [Open in Colab](https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%201/lesson.ipynb) |
| [Lesson 2](Lesson%202/) | Dice Combinations and Grid Paths | [Open in Colab](https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%202/lesson.ipynb) |
| [Lesson 3](Lesson%203/) | Mortal Kombat Tower and Array Description | [Open in Colab](https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%203/lesson.ipynb) |
| [Lesson 4](Lesson%204/) | Fruit Feast | [Open in Colab](https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%204/lesson.ipynb) |
| [Lesson 5](Lesson%205/) | Hoof, Paper, Scissors | [Open in Colab](https://colab.research.google.com/github/fifteen02/julians-pathfinder/blob/main/Lesson%205/lesson.ipynb) |

Lesson 1 includes an optional Frog extension: view legal jumps as a graph, record the chosen predecessors, and recover a cheapest path (L1-21). Allow another 15-20 minutes or use it as a follow-up.

Lesson 2 explains the Dice memory improvement in L2-08: a full table, a six-slot circular buffer, then a saved running sum. The six-slot versions use O(n) time and O(1) extra memory.

Each folder includes slides, a printer-friendly worksheet, worksheet answers, student and completed teacher notebooks, Python starters and solutions, and small, medium and large test cases.

**Share `student-pack.zip` with students.** The complete lesson folders also contain solutions. Exercise IDs match across the worksheets, slides, notebooks and teacher books.

## Editing and rebuilding

The PDFs use XeLaTeX. The Python generators in `Course source/` keep the formats consistent; change those sources and rebuild. See [START-HERE.txt](START-HERE.txt) for the build and verification steps.
