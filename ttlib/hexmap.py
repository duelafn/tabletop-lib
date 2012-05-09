# -*- coding: utf-8 -*-
"""

Hex-tiled region:

  rows:   number of hex rows (the sample below has 2 rows)
  cols:   number of hex columns (the sample below has 3 cols)

Notation / Terminology:

  We use (i,j) to refer to row and column ('address') of an object in the
  map data structure. We use (x,y) to refer to a offset ('coordinate') from
  the origin of the map.

  The coordinate system assumes a unit hexagon (hexagon edge length is 1).


Address System:

  Addresses stored in a (2*cols+1)x(4*rows+2+1) matrix.
  (width)x(height) physical coordinate system superimposed.
  hexagon edges assumed to be length 1 (perform transformations in calling code).

       |-------- width ------------------------|
 
#  10  o       o       *---*---*       o       o     —
#                     /         \                    |
#  9     o           *           *           o       |
#                   /             \                  |
#  8       *---*---*       *       *---*---*
#         /         \             /         \        h
#  7     *           *           *           *       e
#       /             \         /             \      i
#  6   *       *       *---*---*       *       *     g
#       \             /         \             /      h
#j 5     *           *           *           *       t
#         \         /             \         /
#  4       *---*---*       *       *---*---*         |
#         /         \             /         \        |
#  3     *           *           *           *       |
#       /             \         /             \      |
#  2   *       *       *---*---*       *       *     |
#       \             /         \             /      |
#  1     *           *           *           *       |
#         \         /             \         /        |
#  0       *---*---*       o       *---*---*         —
#
#      0 0 0   1   2 2 2   3   4 4 4   5   6 6 6
#                          i
"""


from __future__ import division, absolute_import, print_function
import numpy
from math import sqrt

SQRT3 = sqrt(3)
SQRT3_2 = sqrt(3)/2
SQRT3_4 = sqrt(3)/4

IDENTIFY_POINTS = {
    (0,0): '.',  (0,2): '.', (2,0): '.', (2,2): '.',
    (0,1): '\\', (2,3): '\\',
    (0,3): '/',  (2,1): '/',
    (1,0): '-',  (3,2): '-',
    (1,2): 'o',  (3,0): 'o',
    (1,1): None, (1,3): None, (3,1): None, (3,3): None,
    }
EDGES = set(['-', '/', '\\'])

class HexMap(object):

    @staticmethod
    def identify(i,j):
        """
        Returns string identifying feature at given address.

        hex    → return "o"
        vertex → return "."
        edge   → return one of "/", "\", or "-" depending on direction of edge

        None is returned if the address does not correspond to any geometric feature, e.g.: (1,1)

        """
        return IDENTIFY_POINTS[(i%4,j%4)]

    @staticmethod
    def is_vertex(i,j):
        """Return True if feature at address is a vertex"""
        return '.' == HexMap.identify(i,j)

    @staticmethod
    def is_edge(i,j):
        """Return True if feature at address is an edge"""
        return HexMap.identify(i,j) in EDGES

    @staticmethod
    def is_face(i,j):
        """Return True if feature at address is a face"""
        return 'o' == HexMap.identify(i,j)


    def __init__(self, rows, cols, **opt):
        """map = HexMap( a, b )

        """
        self.rows = rows
        self.cols = cols

        self.height = SQRT3 * rows + SQRT3_2
        (ic, rc) = divmod(cols, 2)
        self.width  = 3 * ic + ( 2 if rc else .5 )

        self.objects = {}
        self.places = {}

    def __getitem__(self, key):
        """map[i,j] → list of objects at address (i,j) or None

        raises IndexError unless 0 ≤ i,j < self.rows,self.cols
        """
        (i,j) = key
        if not (0 <= i < self.rows and 0 <= j < self.cols):
            raise IndexError("(%d,%d) Out of bounds" % key)
        return self.places.get((i,j), None)

    def __contains__(self, item):
        """object in map → boolean"""
        return item in self.objects.values()

    def get(self, i, j, dflt=None):
        """map.get(i,j, dflt=None) → get address, allowing override of default"""
        return self.places.get((i,j), dflt)

    def place_object(self, obj, i, j, front=False):
        """Place an object at address (i,j).

        First removes object from its current location (if any)
        """
        self.maybe_remove_object(obj)
        self.objects[obj] = (i,j)
        try:
            if front:
                self.places[(i,j)].insert(0,obj)
            else:
                self.places[(i,j)].append(obj)
        except KeyError, AttributeError:
            self.places[(i,j)] = [obj]

    def remove_object(self, obj):
        """Remove an object from its current location.

        Raises KeyError if object is not on the board.
        """
        loc = self.objects[obj]
        del self.objects[obj]
        self.places[loc].remove(obj)

    def maybe_remove_object(self, obj):
        """Remove an object from its current location.

        Does nothing if object not currently on the board.
        """
        try:
            self.remove_object(obj)
        except KeyError:
            pass

    def clear_space(self, i, j):
        """Remove all objects from address (i,j)

        Raises KeyError if address is empty.
        """
        for obj in self.places[i,j]:
            del self.objects[obj]
        del self.places[i,j]


    def is_off_map(self, i, j):
        """Arrr, Here there be Dragons!"""
        if i < 0 or j < 0 or i > 2*self.cols or j > 4*self.rows+2:
            return True
        if j == 0 and i%4 == 3:
            return True
        if j == 4*self.rows+2 and i%4 == 1:
            return True
        if j > 4*self.rows and (i == 0 or i == 2*self.cols):
            return True
        if not self.identify(i,j):
            return True
        return False

    def faces(self):
        """Returns generator giving hex address pairs for all faces on the map"""
        return ( (2*i+1, 4*j+2+2*(i%2)) for i in xrange(self.cols) for j in xrange(self.rows) )

    def edges(self):
        """Returns generator giving hex address pairs for all edges on the map"""
        pass

    def vertices(self):
        """Returns generator giving hex address pairs for all vertices on the map"""
        pass

    def address2xy(self, i, j):
        """Returns unit coordinates of addresss (i,j)."""
        MAGIC = [ .5, .25, 0, .25 ]
        y = j * SQRT3_4

        (a, b) = divmod(i, 4)
        if 0 == b:
            dx = MAGIC[j % 4]
        elif 1 == b:
            dx = 1
        elif 2 == b:
            dx = 2 - MAGIC[j % 4]
        elif 3 == b:
            dx = 2.5
        return [3 * a + dx, y]

    def nearest_feature(self, x, y):
        """
        Convert coordinate (x,y) to an (i,j) address pair of nearest
        feature on the map.
        """
        pass

    def nearest_hex(self, x, y):
        """
        Convert coordinate (x,y) to an (i,j) address pair of nearest
        hex location on the map.
        """
        pass

    def nearest_vertex(self, x, y):
        """
        Convert user coordinate (x,y) to an (i,j) address pair of nearest
        vertex location on the map.
        """
        pass

    def nearest_edge(self, x, y):
        """
        Convert user coordinate (x,y) to an (i,j) address pair of nearest
        edge location on the map.
        """
        pass

    def adjacent_vertices(self, i, j):
        """
        Returns list of adjacent vertices on the map. Faces have up to 6
        adjacent vertices, edges have up to 2 adjacent vertices, vertices
        have up to 3 adjacent vertices.
        """
        pass

    def adjacent_edges(self, i, j):
        """
        Returns list of adjacent edges on the map. Faces have up to 6
        adjacent edges, edges have up to 4 adjacent edges, vertices have up
        to 3 adjacent edges.
        """
        pass

    def adjacent_faces(self, i, j):
        """
        Returns list of adjacent faces on the map. Faces have up to 6
        adjacent faces, edges have up to 2 adjacent faces, vertices have up
        to 3 adjacent faces.
        """
        pass
