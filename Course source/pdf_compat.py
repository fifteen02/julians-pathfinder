"""A small pdfplumber-compatible reader built on PyMuPDF, used when pdfplumber
is not installed. It provides only what the verify scripts use: pages with
width, height, extract_text(), chars, images and hyperlinks."""
try:
    import pdfplumber as _plumber
except ImportError:
    _plumber = None


class _Page:
    def __init__(self, page):
        self._p = page
        self.width = page.rect.width
        self.height = page.rect.height

    def extract_text(self, **_):
        return self._p.get_text()

    @property
    def chars(self):
        out = []
        for block in self._p.get_text('rawdict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    for c in span['chars']:
                        x0, top, x1, bottom = c['bbox']
                        if x1 > x0:  # skip zero-width ligature continuations
                            out.append(dict(text=c['c'], x0=x0, x1=x1, top=top, bottom=bottom))
        return out

    @property
    def images(self):
        out = []
        for info in self._p.get_image_info():
            x0, top, x1, bottom = info['bbox']
            out.append(dict(x0=x0, x1=x1, top=top, bottom=bottom))
        return out

    @property
    def hyperlinks(self):
        return [dict(uri=link.get('uri')) for link in self._p.get_links() if link.get('uri')]


class _Doc:
    def __init__(self, source):
        import fitz
        if hasattr(source, 'read'):
            self._d = fitz.open(stream=source.read(), filetype='pdf')
        else:
            self._d = fitz.open(str(source))
        self.pages = [_Page(p) for p in self._d]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._d.close()


def open(source):
    """pdfplumber.open when available, otherwise the PyMuPDF adapter."""
    if _plumber is not None:
        return _plumber.open(source)
    return _Doc(source)
