from array import array

# clockwise in screen coordinates (y points down), so turning right is (d + 1) % 4
DIRS4 = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIRS8 = DIRS4 + ((1, 1), (-1, 1), (-1, -1), (1, -1))
DIRMAP = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}


class Grid:
    """A w x h grid stored row-major in a flat array; char grids hold ASCII codes."""
    __slots__ = ("w", "h", "data", "typecode", "is_char")

    def __init__(self, w, h, data=None, typecode="B", fill=0, is_char=False):
        """Build a grid from a flat array, or a w*h array of fill when data is None."""
        self.w, self.h = w, h
        self.typecode = typecode
        self.is_char = is_char
        self.data = data if data is not None else array(typecode, [fill]) * (w * h)

    @classmethod
    def from_chars(cls, text):
        """Build a char grid from multiline text."""
        lines = text.splitlines()
        return cls(len(lines[0]), len(lines), array("B", "".join(lines).encode("ascii")), "B", is_char=True)

    @classmethod
    def from_digits(cls, text, typecode="B"):
        """Build an int grid from multiline text of single digits."""
        lines = text.splitlines()
        return cls(len(lines[0]), len(lines), array(typecode, (int(c) for line in lines for c in line)), typecode)

    @classmethod
    def from_ints(cls, rows, typecode="i"):
        """Build an int grid from a list of equal-length int rows."""
        return cls(len(rows[0]), len(rows), array(typecode, (v for row in rows for v in row)), typecode)

    @classmethod
    def blank(cls, w, h, fill=0, typecode="i"):
        """Build a w x h grid filled with fill."""
        return cls(w, h, None, typecode, fill)

    def _like(self, w, h, data):
        return Grid(w, h, data, self.typecode, is_char=self.is_char)

    def get(self, x, y):
        """Return the value at (x, y)."""
        return self.data[y * self.w + x]

    def set(self, x, y, v):
        """Set the value at (x, y) to v."""
        self.data[y * self.w + x] = v

    def __getitem__(self, p):
        return self.data[p[1] * self.w + p[0]]

    def __setitem__(self, p, v):
        self.data[p[1] * self.w + p[0]] = v

    def in_bounds(self, x, y):
        """Test if (x, y) is within the grid bounds."""
        return 0 <= x < self.w and 0 <= y < self.h

    def idx(self, x, y):
        """Convert (x, y) to a flat index."""
        return y * self.w + x

    def xy(self, i):
        """Convert a flat index to (x, y)."""
        return i % self.w, i // self.w

    def _nbrs(self, x, y, dirs):
        w, h = self.w, self.h
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                yield nx, ny

    def neighbours4(self, x, y):
        """Yield the in-bounds orthogonal neighbours of (x, y)."""
        return self._nbrs(x, y, DIRS4)

    def neighbours8(self, x, y):
        """Yield the in-bounds orthogonal and diagonal neighbours of (x, y)."""
        return self._nbrs(x, y, DIRS8)

    def nbr4_idx(self, i):
        """Return the flat indices of the in-bounds orthogonal neighbours of flat index i."""
        w, x, out = self.w, i % self.w, []
        # i % w guards stop i±1 wrapping onto the previous/next row
        if x:
            out.append(i - 1)
        if x + 1 < w:
            out.append(i + 1)
        if i >= w:
            out.append(i - w)
        if i + w < len(self.data):
            out.append(i + w)
        return out

    def copy(self):
        """Return an independent copy of the grid."""
        return self._like(self.w, self.h, self.data[:])

    def count(self, v):
        """Count the number of occurrences of value v in the grid."""
        return self.data.count(ord(v) if isinstance(v, str) else v)

    def find(self, v):
        """Find the first occurrence of value v in the grid and return its (x, y) coordinates."""
        try:
            i = self.data.index(ord(v) if isinstance(v, str) else v)
        except ValueError:
            return None
        return i % self.w, i // self.w

    def find_all(self, v):
        """Return the (x, y) coordinates of every occurrence of value v."""
        v = ord(v) if isinstance(v, str) else v
        d, w, out, i = self.data, self.w, [], -1
        try:
            while True:
                i = d.index(v, i + 1)
                out.append((i % w, i // w))
        except ValueError:
            return out

    def rows(self):
        """Return each row as an array slice."""
        d, w = self.data, self.w
        return [d[y * w:(y + 1) * w] for y in range(self.h)]

    def cols(self):
        """Return each column as an array slice."""
        d, w = self.data, self.w
        return [d[x::w] for x in range(w)]

    def transpose(self):
        """Return a new grid mirrored along the main diagonal."""
        data = array(self.typecode)
        for c in self.cols():
            data += c
        return self._like(self.h, self.w, data)

    def flip_h(self):
        """Return a new grid mirrored left to right."""
        data = array(self.typecode)
        for r in self.rows():
            data += r[::-1]
        return self._like(self.w, self.h, data)

    def flip_v(self):
        """Return a new grid mirrored top to bottom."""
        data = array(self.typecode)
        for r in reversed(self.rows()):
            data += r
        return self._like(self.w, self.h, data)

    def rotate_cw(self):
        """Return a new grid rotated 90 degrees clockwise."""
        return self.transpose().flip_h()

    def __eq__(self, other):
        return self.w == other.w and self.h == other.h and self.data == other.data

    def __hash__(self):
        return hash(self.data.tobytes())

    def yield_rows(self):
        """Yield each row as a display string."""
        w, d = self.w, self.data
        for y in range(self.h):
            row = d[y * w:(y + 1) * w]
            yield "".join(map(chr, row)) if self.is_char else " ".join(map(str, row))

    def __str__(self):
        return "\n".join(self.yield_rows())
