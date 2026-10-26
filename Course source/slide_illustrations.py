"""Selected slide illustrations; the shared questions and answers stay intact.

Assets were generated with image_gen. Prompts and source paths are recorded in
slide-illustration-prompts.json. Each asset appears on one slide only.
"""

# (question ID, answer slide): (asset, layout, maximum width, maximum height).
ILLUSTRATIONS = {
    ('L1-05', False): ('staircase', 'below-table', 24, 3.8),
    ('L1-10', True): ('cache', 'below-text', 17, 5.7),
    ('L1-14', False): ('frog-stones', 'below-text', 24, 5.7),
    ('L2-02', False): ('dice', 'below-text', 19, 6.0),
    ('L2-09', False): ('grid', 'beside-table', 11, 6.8),
    ('L3-02', False): ('tower', 'below-text', 25, 6.0),
    ('L3-07', False): ('array', 'below-text', 24, 5.2),
    ('L4-01', False): ('fruit', 'below-text', 21, 6.0),
    ('L4-02', False): ('water', 'below-text', 21, 6.0),
    ('L5-02', False): ('gestures', 'below-text', 24, 5.7),
    ('L5-03', True): ('switch', 'beside-table', 12, 6.8),
}


def image_node(name, x, y, width, height):
    return (rf'\node[anchor=south,inner sep=0] at ({x},{y}) '
            rf'{{\includegraphics[width={width}cm,height={height}cm,keepaspectratio]'
            rf'{{assets/slides/{name}.png}}}};' + '\n')


def illustrated_body(u, answer, table, tex, stxt, ruled):
    """Return an illustrated body, or None to keep the existing slide layout."""
    spec = ILLUSTRATIONS.get((u['id'], answer))
    if spec is None:
        return None
    asset, layout, width, height = spec
    body = u['a'] if answer else u['q']
    out = stxt(1.5, 12.4, 29, 23 if table else 25, tex(body), 'ink', 'body')
    if table:
        if layout == 'beside-table':
            # Keep the editable grid and its notation beside the illustrated grid.
            out += (r'\node[anchor=north west,inner sep=0,text width=14cm] '
                    r'at ([yshift=-8mm]body.south west) {'
                    + ruled(table[0], table[1], tex, True) + '};\n')
            out += image_node(asset, 24.5, 1.8, width, height)
        else:
            out += (r'\node[anchor=north west,inner sep=0,text width=29cm] '
                    r'at ([yshift=-8mm]body.south west) {'
                    + ruled(table[0], table[1], tex, True) + '};\n')
            out += image_node(asset, 16, 1.3, width, height)
    else:
        out += image_node(asset, 16, 2.1, width, height)
        footer = (r'\textbf{Watch for:} ' + tex(u['mis']) if answer else
                  'Think on your own first. Then compare your reasoning with a partner.')
        out += stxt(1.5, 1.45, 28, 17, footer, 'quiet')
    return out
