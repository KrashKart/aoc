from array import array

class Grid:
    # declare slots to save memory
    __slots__ = ("w", "h", "data", "typecode", "is_char")

    def __init__(self, w, h, data=None, typecode="B", fill=0, is_char=False):
        self.w, self.h = w, h
        self.typecode = typecode
        self.is_char = is_char
        self.data = data if data is not None else array(typecode, [fill]) * (w * h)

    # constructors
    @classmethod
    def from_chars(cls, text):
        lines = text.splitlines()
        data = array("B", "".join(lines).encode("ascii"))
        return cls(len(lines[0]), len(lines), data, "B", is_char=True)

    @classmethod
    def from_digits(cls, text, typecode="B"):
        lines = text.splitlines()
        data = array(typecode, (int(c) for line in lines for c in line))
        return cls(len(lines[0]), len(lines), data, typecode)

    @classmethod
    def from_ints(cls, rows, typecode="i"):
        data = array(typecode, (v for row in rows for v in row))
        return cls(len(rows[0]), len(rows), data, typecode)

    @classmethod
    def blank(cls, w, h, fill=0, typecode="i"):
        return cls(w, h, None, typecode, fill)

    # accessors
    def get(self, x, y):
        return self.data[y * self.w + x]

    def set(self, x, y, v):
        self.data[y * self.w + x] = v

    def in_bounds(self, x, y):
        """Test if (x, y) is within the grid bounds."""
        return 0 <= x < self.w and 0 <= y < self.h

    # grid operations
    def copy(self):
        return Grid(self.w, self.h, self.data[:], self.typecode, is_char=self.is_char)

    def count(self, v):
        """Count the number of occurrences of value v in the grid."""
        return self.data.count(ord(v) if isinstance(v, str) else v)

    def find(self, v):
        """Find the first occurrence of value v in the grid and return its (x, y) coordinates."""
        v = ord(v) if isinstance(v, str) else v
        try:
            i = self.data.index(v)
        except ValueError:
            return None
        return i % self.w, i // self.w

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.data.tobytes())

    # display functions
    def yield_rows(self):
        w, d = self.w, self.data
        for y in range(self.h):
            row = d[y*w:(y+1)*w]
            yield "".join(map(chr, row)) if self.is_char else " ".join(map(str, row))

    def __str__(self):
        return "\n".join(self.yield_rows())
    