# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import os
import os.path

def user_conf(name):
    if os.environ.get('XDG_CONFIG_HOME', None):
        return os.path.join(os.environ['XDG_CONFIG_HOME'], name)
    else:
        return os.path.join( os.path.expanduser("~/.config"), name )

def user_data(name):
    if os.environ.get('XDG_DATA_HOME', None):
        return os.path.join(os.environ['XDG_DATA_HOME'], name)
    else:
        return os.path.join( os.path.expanduser("~/.local/share"), name )
