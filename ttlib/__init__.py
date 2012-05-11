# -*- coding: utf-8 -*-
"""TabletopLib - Tools and Kivy widgets for Tabletop Games
"""

__version__ = "0.2.1"


import os.path

ttlib_parent_dir = (os.path.split(__file__))[0]
def ttlib_dir(*path):
    return os.path.join(ttlib_parent_dir, *path)
