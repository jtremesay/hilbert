import cgi
import cgitb
import sys
import time
from .drawing import create_hilbert_image


MIN_N = 0
MAX_N = 6
DEFAULT_N = 3
IMAGE_SIZES = (64, 128, 256, 512, 1024)
DEFAULT_IMAGE_SIZE = 128
DEFAULT_ENABLE_GRID = False
DEFAULT_ENABLE_STREAM = False



def send_image(image):
    print('content-type: image/png')
    print()

    sys.stdout.flush()
    image.save(sys.stdout.buffer, 'PNG')
    sys.stdout.buffer.flush()


def route_main(n, image_size, enable_grid, enable_stream):
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
    print('''<form method=get>''')
    print('''    <label>N <select name="n">''')
    for n_ in range(MIN_N, MAX_N + 1):
        if n == n_:
            print('''<option value="{n}" selected>{n}</option>'''.format(n=n_))
        else:
            print('''<option value="{n}">{n}</option>'''.format(n=n_))
    print('''</select></label>''')

    print('''<label>Image size <select name="image_size">''')
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
    print('''</label>''')

    print('''<label>Enable stream''')
    if enable_stream:
        print('''<input type="checkbox" name="enable_stream" checked>''')
    else:
        print('''<input type="checkbox" name="enable_stream">''')
    print('''</label>''')

    print('''<input type=submit value="Apply"></form>''')

    if n > MIN_N:
        print('''<a href="?mode=main&image_size={image_size}&n={n}&enable_grid={enable_grid}">Previous</a>'''
            .format(
                image_size=image_size,
                n=n - 1,
                enable_grid='on' if enable_grid else 'off'))

    print('''<img src="?mode={mode}&image_size={image_size}&n={n}&enable_grid={enable_grid}">'''
        .format(
            mode='stream' if enable_stream else 'image',
            image_size=image_size,
            n=n,
            enable_grid='on' if enable_grid else 'off'))

    if n < MAX_N:
        print('''<a href="?mode=main&image_size={image_size}&n={n}&enable_grid={enable_grid}">Next</a>'''
            .format(
                image_size=image_size,
                n=n + 1,
                enable_grid='on' if enable_grid else 'off'))

        print('''\
    </body>
</html>''')


def route_image(n, image_size, enable_grid):
    image = create_hilbert_image(image_size, n, enable_grid)
    send_image(image)


def route_stream(n, image_size, enable_grid):
    print('X-Accel-Buffering: no');
    print('Content-type: multipart/x-mixed-replace; boundary=endofsection');
    print()
    print('--endofsection')

    def write_image(image):
        send_image(image)
        print('--endofsection')
        sys.stdout.flush()
        time.sleep(1)

    create_hilbert_image(image_size, n, enable_grid, on_image_update=write_image)


def main_cgi():
    cgitb.enable()

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
        enable_grid = fs['enable_grid'].value == 'on'
    except KeyError:
        enable_grid = DEFAULT_ENABLE_GRID

    try:
        enable_stream = fs['enable_stream'].value == 'on'
    except KeyError:
        enable_stream = DEFAULT_ENABLE_STREAM

    if mode == 'main':
        route_main(n, image_size, enable_grid, enable_stream)
    elif mode == 'image':
        route_image(n, image_size, enable_grid)
    elif mode == 'stream':
        route_stream(n, image_size, enable_grid)
    else:
        print('Status: 501')
        print()

        return
