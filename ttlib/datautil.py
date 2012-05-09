# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function


def list_inserter(lst, item, **where):
    if (where.get('first',None)):
        idx = 0
    elif (where.get('before',None)):
        idx = lst.index(where['before'])
    elif (where.get('after',None)):
        idx = 1 + lst.index(where['after'])
    else:
        idx = len(lst)

    lst.insert(idx, item)
