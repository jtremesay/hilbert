from setuptools import setup, find_packages

setup(
    name='hilbert',
    version='0.1-dev',
    packages=find_packages(),
    install_requires=[
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'hilbert = hilbert:main',
        ],
    },
    author='killruana',
    author_email='killruana@gmail.com',
    description='Hilbert curve generator',
    license='WTFPL',
    url='https://github.com/killruana/hilbert',
)
