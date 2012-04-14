
from distutils.core import setup

import re
__version__ = re.search(r'(?m)^__version__\s*=\s*"([\d.]+)"', open('ttlib/__init__.py').read()).group(1)


setup(
    name='TabletopLib',
    version=__version__,
    author='Dean Serenevy',
    author_email='dean@serenevy.net',
    packages=['ttlib'],
    url='https://github.com/duelafn/tabletop-lib',
    license='LICENSE',
    description='Tools and Kivy widgets for Tabletop Games',
    long_description=open('README').read(),
    install_requires=[
        "Kivy >= 1.2.0",
    ],
)
