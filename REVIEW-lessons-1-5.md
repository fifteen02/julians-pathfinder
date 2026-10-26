# Review of Lessons 1–5 — what to fix

Page-by-page review of all five PDFs in every lesson (tutorial, teacher, worksheet, worksheet answers, slides: about 460 pages), plus notebooks, starter/solution code, programs and test data. Nothing was changed.

**What is already right, in every lesson:** every number in every table, answer and slide is correct (re-computed by brute force); the code printed in the PDFs is identical to solution.py / solutions.py / programs/; `starter.py` shows NOT IMPLEMENTED and `solution.py` passes all tests; question IDs match across all formats; the overlap checker finds no covered notes or overlapping text in any PDF.

---

## A. Course-wide (fix once in `Course source/` — affects all five lessons)

### Must fix
1. **Command flags print as dashes.** Tutorial §4.2/§4.3 shows "–file" and "–timeout 60" (LaTeX turns `--` into an en dash); a copied command fails. Use `\texttt{-{}-file}` / `\texttt{-{}-timeout 60}` in the tutorial template. (All lessons.)
2. **Text copied from other lessons.** Tutorial §4.2–4.3 says "staircase and the restricted-face exercises use one target integer", "a blocked cell or an unavailable move", "Do not begin an uncached recursive experiment", "Medium cases make repeated recursive work visible". Make this section lesson-specific: the real input formats and what each edge file tests. (All lessons.)
3. **`PRACTICE.txt` (in the student pack) describes every lesson's formats.** Keep only the current lesson's problems. (Lessons 1–5.)
4. **Dead code in student and tutor code.** `MOD = 1_000_000_007` and `BEATS = {"H": "S", …}` (and an unused `lru_cache` import in Lesson 1) appear in starter.py, solution.py, solutions.py and the setup cell of both notebooks in lessons that never use them. Emit only what each lesson needs.
5. **The student notebook gives the exercises away.** `lesson.ipynb` (in the student pack, which promises "excludes solutions") prints the complete answer code straight after "Write…/Implement…" questions, and the final `my_…` exercise is then a copy of code shown a few cells earlier. Turn those cells into stubs (signature, docstring, `return None`), or move the full code behind a clearly labelled "worked example — read after trying" heading.
6. **Recursive versions crash on the medium tests without warning.** The cached recursive solutions raise RecursionError at about 1,000 nested calls (seen in Lessons 3, 4 and 5; Lesson 1's `frog_slow` on 100,000 stones). Say so where recursion is introduced, and use the recursive versions on small/edge files only.
7. **Stray files.** `__pycache__/` in every lesson folder (and Course source), and `build/` duplicates of every PDF. Add them to the build's clean step. (They are not in the zips.)

### Should fix
8. **Complexity not tied to code lines.** Cost claims ("exponentially many calls", "O(n)", "O(n squared)", "four sequential scans") rarely name the loops/lines responsible or give counts. Add a line | runs | total row for each cost claim; give call counts for the slow recursions (e.g. Lesson 1: `stairs_slow(30)` makes 4,356,617 calls). Typeset as O(n²), not "squared".
9. **Worked examples written as prose.** Many traces are sentences ("From 0 we can reach 4 and 7…", "At position 2 … two predecessors…"). Convert to step tables with the arithmetic written out (all lessons; the reviewers list each one below).
10. **Main idea stated late or not at all.** Each lesson's idea ("Remember the answer", "Count the ways to arrive", …) is on the cover/START-HERE but not opened with in the tutorial or teacher guide (Lessons 1, 4 explicitly). State it on tutorial p.2, teacher p.2 and slide 2; add a closing summary slide.
11. **Python used before it is explained:** `@lru_cache(None)`, functions inside functions, `range(n, -1, -1)`, `int(True)`, modulo. One sentence beside the listing that first uses each.
12. **Code slides.** Code slides are small, top-left, with no slide number, and end with "End of this complete function."; some split a function mid-loop. Enlarge and centre the code, add numbers, drop the filler, split only at function boundaries.
13. **Teacher guide layout.** Code appendix pages hold one short listing each (about 15–30% full); question pages leave half-page gaps. Put several listings per page; let questions flow.
14. **Teacher listings and answer listings have no line numbers** while the tutorial's do; add them (needed for the line-based cost explanations).
15. **Teacher p.last prints calls like `my_tower([0],)`** (tuple leftovers). Print normal calls.
16. **Worksheet trace tables** vary in labels and pre-filled cells, some have thin rows with no cells, and some questions that ask for a drawing give only ruled lines. One table style with ruled cells about 8 mm tall; drawing boxes where a drawing is asked for.
17. **Slides missing the blank tables** that the worksheet has (several questions per lesson).
18. **Tutorial page breaks.** Headings stranded at page foot; listings split across pages (keep each listing on one page).

---

## B. Per lesson

### Lesson 1 · Staircase and Frog
**Must fix:** `test-cases/legacy-frog/` (about 1 MB, in the student zip) is not in the manifest or mentioned anywhere, and its .txt files restate the answers — remove or document.
**Should fix:**
- No stones-and-jumps picture for Frog; add one with jump costs, the greedy route 0-2-3-5 (=50) dashed and the best route 0-2-4-5 (=30) solid; reuse it for L1-10/L1-11 answers and teacher p.12 (whose L1-11 trace is only the height table).
- Slide 13 call tree too small; repeated calls barely visible. Last-move diagram: one edge grey, one black — make them alike.
- L1-04 asks for `ways(n)` but the code is `stairs_slow`; use one name. `h_i` (p.15) vs `heights[i]`; define n in §3.3; explain that 122 means [1, 2, 2].
- Answers use `[10] * 100_000`, teacher/notebooks `[7] * 100000`: pick one.
- `recursion_demo` imports `sys` inside the function and returns None silently.
- Tutorial p.11: "frog_slow is correct on both small and large inputs" — it hits RecursionError first.
- Pacing: Frog gets 45 min for six questions and three programs; say L1-12–L1-15 may continue next session, mark L1-13 as extension. Add a picture of the call stack for "stack frame".
- Teacher p.3 uses student wording ("Your teacher may leave Frog…").

### Lesson 2 · Dice Combinations and Grid Paths
**Must fix:**
- **L2-04 answer contradicts itself and the code** (teacher p.5, answers p.6, slide 10 say "a negative total contributes 0"; the code skips large faces so no negative total is ever asked). Rephrase.
- **L2-09 answer slide (25) shows the same empty dot grid as the question** — no routes drawn; the answers PDF only lists coordinates. Draw the 3×3 grid with both routes and the blocked centre.
**Should fix:**
- Grid is only "." and "*" text; draw a real grid with the blocked cell and arrows from above/left. Worksheet L2-09 asks to draw routes but gives no grid. Add a call tree (§1.3), a slot picture for the moving sum (§3.1), and the 4×4 appendix count table.
- Tutorial p.5 uses totals 4–6 (8, 16, 32) before deriving them; L2-01 asks about best[4] = 30 without restating Lesson 1's heights.
- L2-04/L2-05 ask for modulo before L2-06 teaches it; L2-11 asks for a cached grid function the worksheet never shows how to write.
- Notation: `ways[total]` (tutorial, code) vs `ways[s]` (others) vs `i` (teacher notebook); "trap" vs "blocked".
- Teacher timetable: L2-08 missing; slots don't match questions; 15 min for two coding tasks.
- Worksheet: too little space for L2-13 (four predictions), L2-12 (2×2 boxes), L2-04 (tree), L2-08.
- Answers p.2 promises "annotated diagrams" that are not there; p.17 repeats p.16's code.
- Appendix maths set in Computer Modern instead of the body font.

### Lesson 3 · Mortal Kombat Tower and Array Description
**Must fix:** **`count` means two opposite things** — worksheet/answers/slides/teacher call the prefix table `count[i][v]`, while the code and tutorial call it `table[i][v]` and `count(i, previous)` is the recursive completion function one question earlier. Use `table` everywhere.
**Should fix:**
- No diagrams at all. Add: a boss strip shaded by who defeats each boss; arrows showing `friend[i]` reading `me[i+1]`/`me[i+2]` (and back); arrows from row i−1 columns v−1, v, v+1 into [i][v] with padding columns greyed; the before/now rows showing why overwriting in place breaks.
- The tower example is used before it is stated, and its tables have no boss row.
- One player has three names (`me`, "you", "we"); `solve_array(values, maximum)` then `m = maximum` (use m); "skip points"/"sessions" in A.1 vs "turn"/"points"; arrays written as 2111 in A.2.
- "Fill from position 4 back to 0" — 4 is preset; the loop fills 3 down to 0.
- Question order: L3-08 (prefix meaning) → L3-09 (suffix recursion) → L3-10 (prefix table) switches meaning twice; move L3-08 next to L3-10.
- L3-12 table missing from slides/notebook; teacher timetable row names don't match L3-01.
- Nice: replace the slice `sum(table[i-1][v-1:v+2])` with the three terms written out.

### Lesson 4 · Fruit Feast
**Must fix:** **The tests can't catch a wrong solution.** small, medium and large all have the limit itself as the answer, so `return limit` passes 3 of 5 tests. Replace medium and large with inputs whose answer is below the limit, and add a small one where water is needed and the answer is below the limit.
**Should fix:**
- No two-layer diagram (dry row above, wet row below, fruit arrows right, water arrows down-left, route 0→7→3→10) although the teacher guide tells the teacher to draw it.
- Names drift: `dry[f]`/`wet[f]` vs "After water" vs "No drink / Just drank / Then ate"; appendix T, A, B not linked to limit, a, b.
- "Four sequential scans" vs "three passes" everywhere else.
- Worksheet: L4-06's prompt prints L4-05's answer right under it; L4-07 prints L4-06's answer; L4-07/L4-09 tables have no cells; L4-02/L4-06 need blank diagram boxes.
- Slides 17 and 22–23 lack the tables the PDFs have; slide 21 holds 3 lines.
- Straight-quote typography (”seed”) in tutorial lines 90, 154.
- Teacher notebook: "drinking at zero often…" should be "always".

### Lesson 5 · Hoof, Paper, Scissors
**Should fix:**
- Notation: `j` (rules boxes, L5-09) vs `used` (tutorial, code); `budget` vs K; `best` is both the recursive function and a local variable — rename the variable (e.g. `came_from`).
- No transition diagram: two `before` rows (0 and 1 switches) with arrows into `now[1][H]` (stay from `before[1][H]`, switch from `before[0][P]`/`before[0][S]`), labelled with values.
- Tutorial p.7: the 1-switch P and S cells are shown but not worked; §2.4 rows partly worked; §3.2 budget examples are prose.
- Appendix uses a 6-round example (HHSSPP) while the whole lesson uses the 5-round HHSSP, without saying so.
- L5-12 answer says "table supplied with the question" but the worksheet and slide show none.
- Slides 22–23 split `hps_table` mid-loop (slide 23 starts with an orphaned `if old != g:`).
- Notebook L5-10 tests don't match L5-11 (add ('HHH',0) and ('S',2)).
- Nice: "Input. the file…" lowercase; quote style differs between code files and PDFs; the 15-minute slot to write `hps_table` is tight.

---

## Suggested order
1. Course-wide items 1–7 in `Course source/` (one change each fixes all five lessons), then rebuild.
2. The lesson must-fixes: L2's contradicting answer and empty answer slide, L3's `count`/`table` clash, L4's test data, L1's legacy-frog folder.
3. Diagrams (L1 stones, L2 grid/routes, L3 four figures, L4 two layers, L5 transitions) and prose→table conversions.
4. Notation, layout and slide polish.

Detailed per-lesson reports (with page numbers for every prose example, scratch checks and page images) are in the review scratch folders rev-1 … rev-5.

---

## Status (25 Oct)
- **Done:** section A items 1–11 and 18 (generator); all section B "Must fix" items; every tutorial-related "Should fix" and "Nice to have" (diagrams, step tables, cost-by-line, Python notes, main idea, notation across all formats, layout). Tutor books are now 26/27/23/17/19 pages. All verify scripts pass (including the new verify_books.py), 25 PDFs compile cleanly, no overlaps.
- **Still open (other formats):** A12 code slides; A13 teacher-guide layout; A14 line numbers in teacher/answer listings; A15 `my_tower([0],)` call printing; A16 worksheet table style and drawing boxes; A17 blank tables on slides; item 10 for teacher p.2 / slide 2 / closing slide.

## Status (25 Oct, later): classroom formats
- **Done, in the generator only:**
  - **A10 (main idea).** Teacher p.2 opens with a "Main idea: say this at the start" box: the idea, one sentence and "By the end of the lesson you will be able to". Slide 2 gives the same in student wording. A new closing slide gives the main idea, four "What we learned" lines and a new exit question. The data is in `content.IDEAS`.
  - **A12 (code slides).** Code slides use the question-slide layout: header, title and slide number. The code is centred on a code-paper panel and line-numbered. Most functions are now 17–24 pt (before: 17 pt in the top-left corner). Four are below 17 pt: `array_cached` (16.5 pt, 17 lines, kept whole) and three with 79–81-character lines that cannot be wider without wrapping the code: `array_full` 16 pt, `hps_cached` 16 pt and `hps_table` 15.5 pt. "End of this complete function." is gone.
    - A function stays on one slide whenever it fits.
    - Otherwise it splits only before a top-level statement: never mid-loop, never after a decorator, never leaving a part with fewer than five lines. Only `feast_table` (lines 1–9 / 10–20) and `hps_table` (1–10 / 11–22) split.
    - Every slide is numbered, including the title slide.
  - **A13 (teacher layout).** Questions flow, each kept whole; part headings sit inline. Trace answers, code answers and exercise checks follow without forced page breaks. The code appendix holds 2–3 numbered listings per page.
  - **A14 (line numbers).** Every code listing in the teacher guide and the answer booklet is numbered in the tutor-book style, with the same numbers as the tutor book. Inputs, outputs and traces stay unnumbered.
  - **A15 (calls).** Calls print as normal calls, e.g. `my_tower([0])` and `my_frog([7] * 100000)`, in the teacher guide, notebooks and stub checks. They are built with `ast` and checked against the reference functions at build time.
  - **A16 (worksheets).**
    - Tables: one ruled-cell table style with about 8 mm rows. Labels are the code names (`ways[step]`, `heights[i]`, `best[i]`, `ways[total]`, `dry[f]`, `wet[f]`). The policy is that the start value and given data are pre-filled and nothing else is.
    - Drawing spaces: L1-04 and L2-04 call-tree boxes; L2-09 three blank 3×3 grids with the centre blocked; L2-12 two 2×2 grids; L4-02 a chain of boxes; L4-06 halving boxes.
    - Prediction space: a four-row prediction table for L2-13, and a cell table for L5-12.
    - Ruled lines now fill each question's space, and a question alone on its page gets the full page.
    - Prompts no longer state the previous answer (L1-02, L4-06, L4-07). The L2-03 table no longer pre-fills total 3, which is L2-02's answer.
    - Name and Date appear once, on page 2, so the cover may be skipped.
  - **A17 (slide tables).** Every question with a worksheet table shows it blank on the question slide and filled on the answer slide. This covers L1-01, L1-09, L1-15, L2-07, L2-13, L3-12, L4-07, L4-09 and L5-12, plus the completed L1-11 route table. Notebooks also show those blank tables.
  - **Per-lesson items:**
    - L1 "What to complete in class" wording is now neutral.
    - L1-11 teacher/answers now show the greedy and best route costs.
    - Frog's large test is `[7] * 100000` everywhere.
    - L2 timetable: L2-08 is included, slots are named after the questions, and L2-04/05 get 25 minutes. The L3 first row now matches L3-01. The tutor-book appendix shows the new plans.
    - L2-03 and L2-06 "Prompt if stuck" are rewritten.
    - L4 "after water" is now "just drank".
    - Answers p.2 no longer promises "annotated diagrams". The optional-question sentence appears only where an optional question exists.
    - Repeated listings in the answers (L1-15, L2-13, L3-06) are replaced by "Same implementation as Lx-NN (page n)" plus that question's own check. `verify_answers.py` runs those checks against the earlier listing.
- **Page counts (before → after).**
  - Teacher: 22/20/17/13/13 → 12/11/9/8/8.
  - Slides: 42/38/33/27/29 → 43/39/34/28/30. The extra slide in each deck is the closing summary.
  - Worksheets: 14/14/11/10/10, unchanged.
  - Answers: 19/18/16/13/14 → 16/14/11/8/10 (now flowing; see below).
  - Tutor books: 26/27/23/17/19, unchanged.
- **Checks:** all verify scripts pass; 25 PDFs compile with 0 errors and 0 Overfull warnings; overlap check is 0 on all 25; notebooks execute; publish.py was run and no `__pycache__` is left.
- **Answer booklets now flow, like the teacher guide.** There is no forced page per question. Each question block (heading, answer, tables and figures) stays together and moves to the next page rather than splitting; each program part (numbered listing, check and output) is kept whole. "Same implementation as Lx-NN (page n)" page numbers are checked against the PDFs. Every page except the last is at least about half full. Pages: 19/18/16/13/14 → 16/14/11/8/10. verify_books.py no longer mistakes a font-subset tag such as `LMXTQP+` for Latin Modern.


## Status (26 Oct): recursion refresher, starting points and one student worksheet
- Finished the interrupted generator edits and rebuilt all five lessons. The full Frog progression remains in Lesson 1: whole-route costs, greedy counterexample, exhaustive recursion, caching and iteration. The two-hour timetable gives recursion an eight-minute refresher, staircase the remainder of the first hour, a five-minute break, and Frog plus comparison/exit work the remaining 55 minutes. Choose one refresher exercise in class if students already know recursion; all four remain available for practice.
- Added four teaching slides, a call-stack diagram and computed trace tables before staircase. L1-01 to L1-04 cover tracing, returned values, repairing a base case and writing factorial. They appear in the tutor book, teacher guide, student sheet, answers, slides and notebooks. Existing Lesson 1 IDs were shifted consistently; there are now 70 question IDs across the course.
- Every one of the 23 implementation questions prints exact function signatures, including nested helpers, and 1–3 hints. Notebook stubs keep the same signatures. Local practice uses the same function names as the reference implementations. Completed tables are included in the teacher notebooks.
- Retired the regular worksheet output from generation, compilation and packaging. Its 15 old PDF/TeX/build files were moved to `~/.Trash/IOI regular worksheets 2026-10-26`; the active student sheet is `worksheet-printer-friendly.pdf`. Answer booklets remain. A pre-edit recovery copy is in `Archive/Before completing recursion and starting points 2026-10-26.zip`.
- Validation: all 25 PDFs compile with zero errors and zero Overfull/missing-character/undefined warnings; all 70 question/answer slide pairs and page bounds pass; all ten notebooks execute in fresh kernels; 9,989 program checks, 49 file-based practice cases, 456 tutor-book checks, answer-booklet checks and the new signature checks pass. Printed covers and Colab link targets were checked; remote notebook availability was not checked.
- Visual review: rendered all formats and inspected the new recursion pages, teacher timetable, question/answer pages and all 23 implementation question slides. Fixed the recursion code/table collision and crowded hints. Tutor-book margin references remain unobscured. Rendered review sheets are in `Course source/starting-points-qa/`, `answers-qa/`, `print-qa/` and `qa/`.
- Local publishing completed: regenerated `START-HERE.txt`, the five student packs and `Lessons 1-5.zip` using `publish.py`; verified the archive contains 25 PDFs and no retired worksheet files. Lessons 2–5 remain local, as requested; this update does not upload them to GitHub. Classroom pacing remains a proposed plan, not a timed classroom trial.


## Status (26 Oct): matching lesson IDs and explicit returned results
- Checked complete question prompts, not just ID occurrences, across the teacher guides, student worksheets, answer booklets, slides and both notebooks for every lesson. The new `verify_lesson_alignment.py` also validates deferred-code links and tutor-book references. All 70 IDs agree across the current local files.
- The GitHub Lesson 1 notebook was older: its L1-15 coding exercise is L1-19 in the current course, after the four recursion exercises. In the updated teacher guide, L1-15 is “A greedy choice can fail” on page 9; L1-19 is the new Frog coding instance on page 10.
- Added output meanings for every function and nested helper in all 23 implementation starting points. Supplied the outer helper call (for example, `return cost(len(heights) - 1)`) and any setup its arguments require. Students still implement the helper. The notebook stubs call the unfinished helper and return None until it is completed; checks continue to report “Not implemented yet”.
- Removed obsolete instructions to rename functions when the reference and exercise already use the same name. Rebuilt the classroom PDFs with code and return descriptions side by side on slides, and hints underneath. Reviewed the changed slides and printed pages; all 25 PDFs compile without errors or overflow warnings. All ten notebooks execute and the 9,989 program checks pass; answer booklet, worksheet, alignment and signature checks pass.
- GitHub publication scope is Lesson 1 student files only. Existing Lessons 2–5 on GitHub must remain byte-for-byte unchanged. Teacher materials and answers remain in the local course pack.

- Published the matching Lesson 1 notebook and printer-friendly worksheet to GitHub in commit `9204705479fe3f34c3c34b0d9890e340b2f29b55`. Removed the retired regular worksheet from the repository after preserving its local copy in Trash. Verified the remote main branch and byte-for-byte equality of existing Lessons 2–5.


## Status (26 Oct): L1-18 explicitly asks for the implementation
- L1-18 now asks students to write frog_table(heights) using a loop, states the return value, supplies the scaffold and hints, and asks them to test their code. The notebook implementation cell is under L1-18. L1-19 reuses that function for new test cases instead of introducing it.
- Updated the shared generator and rebuilt the four Lesson 1 classroom PDFs and both notebooks. Added a regression check for the implementation in L1-18 and reuse in L1-19. All four PDFs compile without warnings; alignment, starting-point, PDF, answer-booklet and printer-friendly checks pass. All ten notebooks execute; 9,991 program checks pass. Visually reviewed worksheet page 5 and slides 50 and 53.
- Published only the Lesson 1 student notebook and printer-friendly worksheet in commit `3c6947138b34e5e47f93eb7ba239d75d461516a5`; verified remote main matches and existing Lessons 2–5 remain unchanged.


## Status (26 Oct): audit of explicit coding instructions and reuse
- Reviewed all 70 question prompts against the student notebook's actual cells and the corresponding worksheet, slides, teacher guide and answer booklet. Every one of the 20 implementation tasks now explicitly asks for code and names its function. L3-12 no longer assumes an unrequested function exists. L1-12, L1-13 and L1-16 name exactly what students must write.
- Six follow-up testing questions explicitly name the function and earlier implementation question. Removed redundant starting scaffolds from L2-13, L4-09 and L5-10. Moved the requested boundary test cells under L4-10 and L5-11. Kept every supplied student trace table and its worked answer.
- L1-17 now shows the cached Frog solution as a labelled worked example, consistently with cached staircase. Removed the generator's inference that different functions are the same program merely because they pass the same small examples; deferred implementation links are explicit.
- Added verify_task_intent.py to the normal verify.py run: it checks prompt wording, function names, actual stubs under each question, absence of overwritten implementations, and the six reuse/test links and their executable checks. Added a check that every worked trace table has a corresponding student table.
- Validation: 9,992 program checks pass; all ten notebooks execute in clean kernels; all 70 IDs and full prompts align across formats; signature/return/hint, answer booklet, printed worksheet and page-bound checks pass. All 20 rebuilt classroom PDFs compile without errors or overflow warnings. The five tutor books were unchanged. Visually reviewed changed slides and printed question pages, with examples from both teacher and answer booklets. Lesson 1 remains five printed pages including its cover.
- Local corrections cover all five lessons. GitHub publication is restricted to the Lesson 1 student notebook and printer-friendly worksheet; existing Lessons 2–5 are preserved.
- Squashed the recent Lesson 1 updates into commit `2a0011bb0f89d38434c4cbdaea8d1e309cfaea76` on top of the original publication commit, then pushed with an explicit force-with-lease. Verified remote main matches, the working tree is clean, and all existing Lessons 2–5 files retain their original hashes. Recovery bundle: `/tmp/julians-pathfinder-before-audit-squash.bundle`.


## Status (26 Oct): recursion questions before revealed answers
- Removed the countdown output and full countdown(3) call sequence from the introductory slides. L1-01 now gives the first completed countdown trace, after its question.
- Split the sum_to(3) trace into a question slide with missing returned values and a separate following answer slide. Updated the teacher instructions to match slides 3–7 and to pause before revealing results.
- Added runnable sum_to, countdown and sum_squares examples to the student notebook. Students enter a prediction or opt into running the example before its output appears. Three completed trace tables are in closed HTML details panels; teacher notebooks keep the worked traces visible. No exercises or question IDs were removed.
- Added verify_recursion_reveal.py to the normal verification suite. Checks cover blank question vs following answer, closed panels, no saved student outputs, default execution without revealed results, and correct outputs after opting in. All ten notebooks execute; 9,992 program checks and the 70-question alignment audit pass. Both rebuilt PDFs compile with no warnings; reviewed slides 3–7 and the teacher page visually.
- Published the updated Lesson 1 student notebook in the existing squashed Lesson 1 commit, now `91023db640a6f95bdb0cee1697c09ccbac0d7f59`; verified remote main and unchanged Lessons 2–5. Slides and teacher guide are updated locally. Student-pack checks permit only the three explicitly supplied trace functions, while continuing to reject implementation solutions.


## Status (26 Oct): warmer Lesson 1 slides and recursion diagrams
- Added a slide-only terracotta, amber and green palette, warm code panels and labelled colour cues. Printed materials and Lessons 2–5 retain their existing appearance.
- Illustrated the call stack and direction of calls/returned answers. Added a complete stairs_slow(3) call tree, highlighted repeated staircase calls, and a Frog dependency tree with computed costs and labelled final-jump costs. Numerical labels come from the reference functions.
- Preserved every exercise and the separate question/answer reveals. Reviewed the entire deck as contact sheets and enlarged the changed recursion pages; adjusted the denser diagrams to keep text clear. The Lesson 1 deck compiles with zero errors or overflow warnings. Recursion-reveal, all-format alignment, PDF bounds and slide-illustration checks pass.
- Rebuilt the local published PDF and course archive. No GitHub files were changed by this slide-only update.

- Header follow-up: replaced the three-colour decorative strip with one thin (0.6 mm) terracotta rule. Lesson 1 slides rebuilt without compiler warnings and the rendered header checked.

- Selected header variant A applied throughout Lesson 1: removed the decorative top rule, placed titles first, and moved lesson/exercise/question/answer context to the footer. All 58 slides reviewed in rendered contact sheets; zero compiler warnings, all question IDs present, page bounds and question-before-answer checks pass. Other lessons unchanged.

## Status (26 Oct): Lesson 1 slide cohesion
- Kept selected quiet header A. Added consistent section navigation (Recursion, Staircase, Frog, Review), aligned the main content start and code panels, and used exact function signatures for Python slide titles. Secondary advice uses the quiet text colour so instructional diagrams retain emphasis.
- Added two illustrated transitions linking the sections through the same Explore / Remember / Build in order sequence. The deck now has 60 slides; all 20 question/answer pairs and all complete code remain in order.
- Updated the illustration checker to locate exercise labels in the footer as well as the header. Zero compilation warnings; full-prompt alignment, PDF bounds, illustration and recursion-reveal checks pass. Reviewed the whole rendered deck and enlarged both new transitions. Local slide PDF and course archive updated; no GitHub or other lesson changes.


## Status (21 Nov): two consolidated teacher volumes
- Moved teacher material into Teacher/: Teacher Book (108 pages) for preparation and Teacher Class Notes (56 pages) for classroom use. Both cover all five lessons with one linked contents page, lesson bookmarks and continuous page numbering.
- Preserved all 70 exercise IDs, complete questions, answers, hints, misconceptions and code references. Class Notes includes each lesson's Colab link; Teacher Book does not.
- Updated the generators, compiler, publication process and readmes so separate tutorial/teacher PDFs and sources stay in the internal build folder. Archived the former lesson-level material in Archive/Teacher materials before consolidation-2026-11-21.zip.
- Both volumes compile with zero errors and zero overflow warnings. Verified question coverage, complete classroom content, internal links, page numbers, text bounds and illustrated covers; inspected rendered pages.


## Status (21 Nov): teacher-book design polish and course title
- Named the course Dynamic Programming: From Recursion to Efficient Solutions. Both illustrated covers and PDF metadata carry the title, with Teacher Book and Class Notes identifying each volume.
- Reworked contents pages into aligned lesson rows with clickable titles and clear page numbers. Standardised lesson openings and added volume/lesson footers. Gave timetable activities more width while keeping minutes and exercise IDs in compact columns.
- Retained the established monochrome illustrations, fonts, code, diagrams and teaching content. Teacher Book remains 108 pages; better timetable wrapping brings Class Notes to 55 pages.
- Checked rendered covers, contents, all lesson openings and representative teaching pages. Both volumes compile without errors or overflow warnings; all 70 exercise IDs, complete questions/answers, code and internal links pass verification.


## Status (21 Nov): preserve tutorial depth, using Candies as the reference
- Confirmed that Teacher Book contains the detailed tutorial chapters, while Class Notes is the short teaching companion. Original individual tutorials remain in the recovery archive.
- Added eight integrated tutor walkthroughs across Lessons 1-5: cache hits; Frog's full-route candidates; dice contributions; whose turn in Tower; Array Description positions, values and counts; Fruit Feast recursive returns and reachability flags; and HPS past/future wins and switch budgets. Added two dependency diagrams and worked tables before the general code.
- Small example calculations are derived in Python and checked against the reference solutions. Student exercise IDs, questions, notebooks and implementation files are unchanged. Corrected lesson-prefixed section references in the combined volume and prevented single-line paragraph fragments at page breaks.
- Final validation: Teacher Book 113 pages; Class Notes 55 pages. Both compile with zero warnings. All 70 exercise IDs, complete classroom content, code and internal links verified; 456 tutor-book checks and the eight new walkthrough checks pass.

## Status (21 Nov): Frog as a graph and recovering a cheapest path
- Added L1-21 after the existing cost exercises; L1-01 to L1-20 retain their IDs. Students implement frog_path(heights), returning both the minimum cost and stone indices. The reference keeps the i - 1 predecessor on ties and explains the -1 start marker, backwards traversal and one final reversal.
- Added the weighted graph of all legal jumps, linked explicitly to the staircase graph. Stone indices, heights and arrow costs are distinguished. Question/answer slides precede the recursion exercise; a later diagram highlights the recovered route. Explained why the graph has one node per stone while the recursion tree can repeat calls for that stone.
- Added worked candidate and predecessor tables, backwards trace, graph and complete implementation in Teacher Book; matching questions, signatures, hints, diagrams and answers in classroom materials and notebooks. L1-21 is a 15-20 minute extension or follow-up outside the two-hour core. The original AtCoder adapter still returns only the cost.
- Added frog-path small, medium, large and edge datasets, starter and reference functions. Independently enumerated all legal routes on 3,279 small inputs; checked ties, arrow labels, and legal optimal returned paths on 500 and 100,000 stones. All 55 file-based practice cases and ten notebook executions passed.
- Validation: all 71 question IDs align, all 21 implementation questions have matching signatures and hints, question slides precede their answers, and rebuilt PDFs compile without errors or overflow warnings. Inspected the new book, worksheet, answer, class-note and slide pages, including the graph and backwards-trace diagrams.

## Status (21 Nov): Dice circular-buffer explanation
- Expanded L2-08 without changing exercise IDs. Moved the memory-saving Dice chapter beside the Dice material, before Grid Paths. Explained the target total, physical slot and stored count separately, including initial zeros, the first wrap at total 6, and replacing total 1 with total 7 in slot 1.
- Added dice_ring as a complete intermediate solution: six stored counts, summed before overwriting. The existing dice_window then maintains the sum, matching the circular-buffer algorithm discussed with the author. Both use O(n) time and O(1) extra memory; keeping the sum reduces the constant work, while the fixed buffer is what saves memory.
- Added a slot-reuse diagram, before/after table, totals 1-9 trace with arithmetic, line-by-line runtime explanation, and matching worksheet, class notes, answer booklet, slides and notebooks. Explained why window is already reduced modulo MOD before assignment and why the function returns the saved count, not the sum for the following target.
- Independently compared the full table, six-slot sum and saved-sum versions for totals 0-500, 1000 and 1000000; tested wraparound, the six-entry limit and modular arithmetic with a small modulus. The notebook worked examples include both implementations. The two-hour timetable retains a brief preview, with the full trace available as follow-up.
- Final checks: 464 tutor-book checks pass; all 71 IDs and implementation signatures align; all ten notebooks execute; independent answer-booklet programs run. Inspected the new diagrams, trace pages, worksheet and question/answer slides. Rebuilt PDFs have zero compiler errors or overflow warnings. Teacher Book is 120 pages and Teacher Class Notes is 56 pages.
