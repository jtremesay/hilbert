import itertools
from .drawing import create_hilbert_image


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


if __name__ == '__main__':
    main()

