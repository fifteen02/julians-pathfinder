"""Narrative tutor books, one module per lesson (book_l1.py ... book_l5.py).

The classroom prompt sheets remain in content.py; the block constructors are in
book_blocks.py, the figures in book_figures.py and the measured numbers in book_kit.py.
build_books.py renders BOOKS; verify_books.py checks them.
"""
import importlib

BOOKS = {n: importlib.import_module(f'book_l{n}').BOOK for n in range(1, 6)}

from book_walkthroughs import enrich
enrich(BOOKS)

from frog_path_extension import tutorial_section
frog_chapter=next(ch for ch in BOOKS[1]['chapters'] if ch['title']=='Frog: keep the cheapest route')
position=next(i for i,s in enumerate(frog_chapter['sections']) if s['title']=='Frog: edge cases, mistakes and the judge')
frog_chapter['sections'].insert(position,tutorial_section())
frog_chapter['sections'][position-1]['next']='Extend the cost answer by recovering one cheapest route.'

import frog_graph as FG
graph_section=next(s for s in frog_chapter["sections"] if s["title"]=="Ask about the last jump to a stone")
graph_section["blocks"][:0]=FG.book_blocks()
