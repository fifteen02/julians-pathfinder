"""Constructors for tutor-book content (see build_books.py for how each block renders)."""


def section(title, ids, goal, next, *blocks):
    return dict(title=title, ids=list(ids), goal=goal, next=next, blocks=list(blocks))


def chapter(title, goal, *sections, opening=()):
    return dict(title=title, goal=goal, sections=list(sections), opening=list(opening))


def code(name, run=None): return ('code', name, run)
def diagram(ident): return ('diagram', ident)
def table(head, rows, spec=None): return ('table', head, rows, spec)
def pause(question, answer): return ('pause', question, answer)
def figure(tikz, caption): return ('figure', tikz, caption)
def python(ids, title, text): return ('python', ids, title, text)
def problem(**statement): return ('problem', statement)
def items(*texts): return ('items', list(texts))
def listing(text): return ('listing', text)
def judge(fn): return ('judge', fn)


def cost(title, name, small, full, entries):
    """A line-cost table for programs.<name>.

    small = (args, params, label): a concrete run whose line counts are measured;
    full  = (params, label): the full-size parameters.
    entries = [(code snippet, words, formula(**params))]. Each formula must equal the
    measured count on the small run; it is then evaluated at full size.
    """
    import book_kit as K
    args, params, small_label = small
    full_params, full_label = full
    hits = K.line_runs(name, args)
    rows = []
    for snippet, words, f in entries:
        line = K.listing_line(name, snippet)
        measured = hits.get(line, 0)
        assert measured == f(**params), (name, snippet, measured, f(**params))
        shown = snippet[0] if isinstance(snippet, tuple) else snippet
        rows.append([str(line), '`' + shown + '`', words, K.comma(measured), K.big(f(**full_params))])
    return ('cost', title, ['Line', 'Code', 'How often it runs', small_label, full_label], rows)


# A comparison table that ends each problem: case | answer | why it matters
def edges(rows): return table(['Case', 'Answer', 'Why it matters'], rows, r'>{\raggedright\arraybackslash}p{36mm}>{\raggedright\arraybackslash}p{24mm}X')


def mistakes(rows): return table(['Mistake', 'What the program does', 'Output (correct)'], rows, r'>{\raggedright\arraybackslash}p{40mm}X>{\raggedright\arraybackslash}p{26mm}')


def recap(*texts): return ('recap', list(texts))
