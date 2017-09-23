from PIL import Image, ImageDraw
from .hilbert import HilbertContext, hilbert_sequence


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
