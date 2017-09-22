import itertools
from PIL import Image, ImageDraw
import sys
import time


COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)


def draw_grid(image_draw, grid_size, square_size):
    for x in range(0, grid_size, square_size):
        top = (x, 0)
        bottom = (x, grid_size)
        line = (top, bottom)
        image_draw.line(line, COLOR_RED)
    image_draw.line(
        ((grid_size - 1, 0), (grid_size - 1, grid_size)),
        COLOR_RED)

    for y in range(0, grid_size, square_size):
        left = (0, y)
        right = (grid_size, y)
        line = (left, right)
        image_draw.line(line, COLOR_RED)
    image_draw.line(
        ((0, grid_size - 1), (grid_size, grid_size - 1)),
        COLOR_RED)


HILBERT_UP = 0
HILBERT_DOWN = 1
HILBERT_LEFT = 2
HILBERT_RIGHT = 3


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

def create_hilbert_image(image_size, n, enable_grid=False, on_image_update=None):
    image_dimensions = (image_size, image_size)
    image = Image.new('RGB', image_dimensions, COLOR_WHITE)

    squares_per_side = 2 ** n
    square_size = image_size // squares_per_side
    ctx = HilbertContext(square_size)

    image_draw = ImageDraw.Draw(image)
    if enable_grid:
        draw_grid(image_draw, image_size, square_size)
    del image_draw

    for move in hilbert_sequence(n, ctx):
        image_draw = ImageDraw.Draw(image)
        image_draw.line(move, COLOR_BLUE)
        del image_draw

        if on_image_update is not None:
            on_image_update(image)

    return image


def main():
    image_sizes = (
        128,
        256,
        512,
        1024,
    )
    dimensions = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
    )
    for image_size, n in itertools.product(image_sizes, dimensions):
        image_name = 'hilbert_{n}n_{size}x{size}.png'.format(n=n, size=image_size)
        print('creating {}'.format(image_name))
        image = create_hilbert_image(image_size, n)
        print('saving {}'.format(image_name))
        image.save(image_name, 'PNG')


def cgi_send_image(image):
    print('content-type: image/png')
    print()

    sys.stdout.flush()
    image.save(sys.stdout.buffer, 'PNG')
    sys.stdout.buffer.flush()


def main_cgi():
    import cgi
    import cgitb
    import sys

    cgitb.enable()

    MIN_N = 0
    MAX_N = 6
    DEFAULT_N = 3
    IMAGE_SIZES = (64, 128, 256, 512, 1024)
    DEFAULT_IMAGE_SIZE = 128
    DEFAULT_ENABLE_GRID = False
    DEFAULT_ENABLE_STREAM = False

    fs = cgi.FieldStorage()
    try:
        mode = fs['mode'].value
    except KeyError:
        mode = 'main'

    try:
        image_size = int(fs['image_size'].value)
    except KeyError:
        image_size = DEFAULT_IMAGE_SIZE
    else:
        if image_size not in IMAGE_SIZES:
            image_size = DEFAULT_IMAGE_SIZE

    try:
        n = int(fs['n'].value)
    except KeyError:
        n = DEFAULT_N
    else:
        n = min(max(MIN_N, n), MAX_N)

    try:
        enable_grid = bool(fs['enable_grid'].value)
    except KeyError:
        enable_grid = DEFAULT_ENABLE_GRID

    try:
        enable_stream = bool(fs['enable_stream'].value)
    except KeyError:
        enable_stream = DEFAULT_ENABLE_STREAM

    if mode == 'main':
        print('content-type: text/html')
        print()
        print('''\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Hilbert curve</title>
    </head>
<body>''')
        print('''\
            <form method=get>''')

        print('''
                <label>N
            <select name="n">''')
        for n_ in range(MIN_N, MAX_N + 1):
            if n == n_:
                print('''<option value="{n}" selected>{n}</option>'''.format(n=n_))
            else:
                print('''<option value="{n}">{n}</option>'''.format(n=n_))
        print('''\
                </select>
            </label>''')

        print('''\
            <label>Image size
                <select name="image_size">''')
        for image_size_ in IMAGE_SIZES:
            if image_size == image_size_:
                print('''<option value="{image_size}" selected>{image_size}</option>'''.format(image_size=image_size_))
            else:
                print('''<option value="{image_size}">{image_size}</option>'''.format(image_size=image_size_))
        print('''\
                </select>
            </label>''')

        print('''<label>Display grid''')
        if enable_grid:
            print('''<input type="checkbox" name="enable_grid" checked>''')
        else:
            print('''<input type="checkbox" name="enable_grid">''')
        print('''\
                </label>''')

        print('''<label>Enable stream''')
        if enable_stream:
            print('''<input type="checkbox" name="enable_stream" checked>''')
        else:
            print('''<input type="checkbox" name="enable_stream">''')
        print('''\
                </label>''')

        print('''\
                <input type=submit value="Apply">
            </form>''')

        if n > MIN_N:
            print('''\
            <a href="?mode=main&image_size={image_size}&n={n}&enable_grid={enable_grid}">Previous</a>'''.format(image_size=image_size, n=n - 1, enable_grid=enable_grid))

        print('''\
            <img src="?mode={mode}&image_size={image_size}&n={n}&enable_grid={enable_grid}">'''.format(mode='stream' if enable_stream else 'image', image_size=image_size, n=n, enable_grid=enable_grid))

        if n < MAX_N:
            print('''\
            <a href="?mode=main&image_size={image_size}&n={n}&enable_grid={enable_grid}">Next</a>'''.format(image_size=image_size, n=n + 1, enable_grid=enable_grid))

        print('''\
    </body>
</html>''')

        return
    elif mode == 'image':
        image = create_hilbert_image(image_size, n, enable_grid)
        cgi_send_image(image)

        return
    elif mode == 'stream':
        print('X-Accel-Buffering: no');
        print('Content-type: multipart/x-mixed-replace; boundary=endofsection');
        print()
        print('--endofsection')

        def write_image(image):
            cgi_send_image(image)
            print('--endofsection')
            sys.stdout.flush()
            time.sleep(.25)

        image = create_hilbert_image(image_size, n, enable_grid, on_image_update=write_image)
        cgi_send_image(image)
        print('--endofsection')

        return
    else:
        print('Status: 501')
        print()

        return


if __name__ == '__main__':
    main()

