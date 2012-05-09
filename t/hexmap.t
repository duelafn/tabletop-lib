#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2
import sys
sys.path.append("")

from ttlib.hexmap import HexMap
from math import sqrt

SQRT3 = sqrt(3)
SQRT3_2 = sqrt(3)/2
SQRT3_4 = sqrt(3)/4


#     |-------- width ------------------------|
#
# 10  o       o       *---*---*       o       o     —
#                    /         \                    |
# 9     o           *           *           o       |
#                  /             \                  |
# 8       *---*---*       *       *---*---*
#        /         \             /         \        h
# 7     *           *           *           *       e
#      /             \         /             \      i
# 6   *       *       *---*---*       *       *     g
#      \             /         \             /      h
# 5     *           *           *           *       t
#        \         /             \         /
# 4       *---*---*       *       *---*---*         |
#        /         \             /         \        |
# 3     *           *           *           *       |
#      /             \         /             \      |
# 2   *       *       *---*---*       *       *     |
#      \             /         \             /      |
# 1     *           *           *           *       |
#        \         /             \         /        |
# 0       *---*---*       o       *---*---*         —
# =
# i
#   j= 0 0 0   1   2 2 2   3   4 4 4   5   6 6 6

class BasicAccess(unittest2.TestCase):
    def setUp(self):
        self.obj = {
            ".":  [ (0,0), (0,2), (0,4), (0,6), (0,8),
                    (2,0), (2,2), (2,4), (2,6), (2,8), (2,10),
                    (4,0), (4,2), (4,4), (4,6), (4,8), (4,10),
                    (6,0), (6,2), (6,4), (6,6), (6,8),
                   ],
            "\\": [ (0,1), (0,5), (2,3), (2,7), (4,1), (4,5), (4,9), (6,3), (6,7) ],
            "/":  [ (0,3), (0,7), (2,1), (2,5), (2,9), (4,3), (4,7), (6,1), (6,5) ],
            "-":  [ (1,0), (1,4), (1,8), (3,2), (3,6), (3,10), (5,0), (5,4), (5,8) ],
            "o":  [ (1,2), (1,6), (3,4), (3,8), (5,2), (5,6) ],
            None: [ (1,1), (1,3), (1,5), (1,7), (1,9),
                    (3,1), (3,3), (3,5), (3,7), (3,9),
                    (5,1), (5,3), (5,5), (5,7), (5,9),
                    ],
            }

    def assertAlmostEqualArray(self, a, b, places=None, msg=None, delta=None):
        self.assertEqual(len(a), len(b), msg + ": arrays have same length")
        for i in xrange(len(a)):
            self.assertAlmostEqual(a[i], b[i], places, msg + ": index " + str(i), delta)

    def test_identify(self):
        m = HexMap( rows=2, cols=3 )

        for (shape, points) in self.obj.iteritems():
            for p in points:
                self.assertEqual( m.identify(*p), shape, "Shape of " + str(p) )

    def test_size(self):
        m = HexMap( rows=2, cols=3 )
        self.assertAlmostEqual( m.width,  5, 7, "Width of 2x3" )
        self.assertAlmostEqual( m.height, 5 * SQRT3_2, 7, "Height of 2x3" )

        m = HexMap( rows=3, cols=6 )
        self.assertAlmostEqual( m.width,  9.5, 7, "Width of 3x6" )
        self.assertAlmostEqual( m.height, 7 * SQRT3_2, 7, "Height of 3x6" )

        m = HexMap( rows=11, cols=9 )
        self.assertAlmostEqual( m.width,  14, 7, "Width of 3x6" )
        self.assertAlmostEqual( m.height, 23 * SQRT3_2, 7, "Height of 3x6" )

    def test_address2xy(self):
        m = HexMap( rows=2, cols=3 )
        places = {
            (0,0): (.5,0),
            (0,1): (.25,SQRT3_4),
            (0,2): (0,SQRT3_2),
            (0,3): (.25,3*SQRT3_4),
            (0,4): (.5,SQRT3),
            (0,5): (.25,5*SQRT3_4),

            (1,0): (1,0),
            (1,2): (1,SQRT3_2),
            (1,4): (1,2*SQRT3_2),
            (1,6): (1,3*SQRT3_2),

            (2,0): (1.5,0),
            (2,1): (1.75,SQRT3_4),
            (2,2): (2,SQRT3_2),
            (2,3): (1.75,3*SQRT3_4),
            (2,4): (1.5,SQRT3),
            (2,5): (1.75,5*SQRT3_4),

#            (3,0): (1,0),
            (3,2): (2.5,SQRT3_2),
            (3,4): (2.5,2*SQRT3_2),
            (3,6): (2.5,3*SQRT3_2),

            (4,0): (3.5,0),
            (4,1): (3.25,SQRT3_4),
            (4,2): (3,SQRT3_2),
            (4,3): (3.25,3*SQRT3_4),
            (4,4): (3.5,SQRT3),
            (4,5): (3.25,5*SQRT3_4),

#            (3,0): (1,0),
            (5,2): (4,SQRT3_2),
            (5,4): (4,2*SQRT3_2),
            (5,6): (4,3*SQRT3_2),
            }

        for (addr, xy) in places.iteritems():
            self.assertAlmostEqualArray( xy, m.address2xy(*addr), 7, "address2xy" + str(addr) )

    def test_is_off_map(self):
        in_map = set()
        out_of_map = set()
        for (shape, points) in self.obj.iteritems():
            if shape:
                in_map.update(points)
        for t in [ (i,j) for i in xrange(-2,9) for j in xrange(-2,13) ]:
            if not t in in_map:
                out_of_map.add(t)

        m = HexMap( rows=2, cols=3 )
        for addr in in_map:
            self.assertFalse( m.is_off_map(*addr), "is_off_map: "+str(addr) )

        for addr in out_of_map:
            self.assertTrue(  m.is_off_map(*addr), "is_off_map: "+str(addr) )


if __name__ == '__main__':
    unittest2.main()
