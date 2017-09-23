HILBERT_UP = 0
HILBERT_DOWN = 1
HILBERT_LEFT = 2
HILBERT_RIGHT = 3


HILBERT_STATE_MACHINE = {
    HILBERT_UP: (
        HILBERT_RIGHT,
        HILBERT_UP,
        HILBERT_UP,
        HILBERT_RIGHT,
        HILBERT_UP,
        HILBERT_DOWN,
        HILBERT_LEFT,
    ),
    HILBERT_LEFT: (
        HILBERT_DOWN,
        HILBERT_LEFT,
        HILBERT_LEFT,
        HILBERT_DOWN,
        HILBERT_LEFT,
        HILBERT_RIGHT,
        HILBERT_UP,
    ),
    HILBERT_RIGHT: (
        HILBERT_UP,
        HILBERT_RIGHT,
        HILBERT_RIGHT,
        HILBERT_UP,
        HILBERT_RIGHT,
        HILBERT_LEFT,
        HILBERT_DOWN,
    ),
    HILBERT_DOWN: (
        HILBERT_LEFT,
        HILBERT_DOWN,
        HILBERT_DOWN,
        HILBERT_LEFT,
        HILBERT_DOWN,
        HILBERT_UP,
        HILBERT_RIGHT,
    ),
}


class HilbertContext:
    def __init__(self, distance, x=None, y=None):
        self.distance = distance
        self.x = x if x is not None else distance // 2
        self.y = y if y is not None else distance // 2

    def as_tuple(self):
        return (self. x, self.y)

    def up(self):
        begin = self.as_tuple()
        self.y += self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def down(self):
        begin = self.as_tuple()
        self.y -= self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def left(self):
        begin = self.as_tuple()
        self.x -= self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def right(self):
        begin = self.as_tuple()
        self.x += self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def move(self, direction):
        return {
            HILBERT_UP: self.up,
            HILBERT_DOWN: self.down,
            HILBERT_LEFT: self.left,
            HILBERT_RIGHT: self.right
        }[direction]()


class HilbertContext:
    def __init__(self, distance, x=None, y=None):
        self.distance = distance
        self.x = x if x is not None else distance // 2
        self.y = y if y is not None else distance // 2

    def as_tuple(self):
        return (self. x, self.y)

    def up(self):
        begin = self.as_tuple()
        self.y += self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def down(self):
        begin = self.as_tuple()
        self.y -= self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def left(self):
        begin = self.as_tuple()
        self.x -= self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def right(self):
        begin = self.as_tuple()
        self.x += self.distance
        end = self.as_tuple()
        line = (begin, end)

        return line

    def move(self, direction):
        return {
            HILBERT_UP: self.up,
            HILBERT_DOWN: self.down,
            HILBERT_LEFT: self.left,
            HILBERT_RIGHT: self.right
        }[direction]()


def hilbert_sequence(n, ctx, turn=HILBERT_UP):
    if n == 0:
        return

    n -= 1

    turns = (turn for turn in HILBERT_STATE_MACHINE[turn])

    for move in hilbert_sequence(n, ctx, next(turns)):
        yield move

    yield ctx.move(next(turns))

    for move in hilbert_sequence(n, ctx, next(turns)):
        yield move

    yield ctx.move(next(turns))

    for move in hilbert_sequence(n, ctx, next(turns)):
        yield move

    yield ctx.move(next(turns))

    for move in hilbert_sequence(n, ctx, next(turns)):
        yield move
