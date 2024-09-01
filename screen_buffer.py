
class ScreenBuffer:

    def __init__(self, other=None):
        if other is not None:
            self.from_other(other)
        else:
            # Make a new blank one
            self._buffer = [0] * 16

    def clear(self):
        self._buffer = [0] * 16

    def from_other(self, other):
        if isinstance(other, ScreenBuffer):
            # Copy constructor
            self._buffer = other._buffer.copy()
        else:
            # Assume it is a raw art image
            self._buffer = other.copy()

    def and_with(self, other):
        if isinstance(other, ScreenBuffer):
            other = other._buffer
        for i in range(16):
            self._buffer[i] &= other[i]

    def or_with(self, other):
        if isinstance(other, ScreenBuffer):
            other = other._buffer
        for i in range(16):
            self._buffer[i] |= other[i]

    def andor_with(self, other, mask):
        if isinstance(other, ScreenBuffer):
            other = other._buffer
        if isinstance(mask, ScreenBuffer):
            mask = mask._buffer
        for i in range(16):
            self._buffer[i] = (self._buffer[i] & mask[i]) | other[i]
