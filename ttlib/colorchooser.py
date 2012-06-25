# -*- coding: utf-8 -*-
"""
ColorChooser
============

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

GREY = -1

def get_shade( color, idx, n ):
    if (color == GREY):
        # Greys, DO include white and black here
        grey = (n-idx-1)/(n-1)
        return [ grey, grey, grey ]
    elif (idx < (n-1)/2):
        # Linear interpolate between color and "white" (skipping white itself)
        return [ 1 - 2*(idx+1)*(1-c)/(n+1) for c in color ]
    elif (idx > (n-1)/2):
        # Linear interpolate between color and "black" (skipping black itself)
        return [ 2*c*(n-idx)/(n+1) for c in color ]
    else:
        return color

#               red,     orange,    yellow,  green,   cyan,    blue,    magenta, GREYS
grid_colors = [ [1,0,0], [1,0.5,0], [1,1,0], [0,1,0], [0,1,1], [0,0,1], [1,0,1], GREY ]


class ColorSwatch(Widget):
    """Basic swatch object for ColorChoosers. Don't use this class directly.
    """

    color = ListProperty([1,1,1])
    """:class:`~kivy.properties.ListProperty`, defaults to [1,1,1].
    Color of the swatch.
    """

    _rec = ObjectProperty(None)
    """:class:`~kivy.properties.ObjectProperty`. Private reference to
    rectangle swatch.
    """

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        self.register_event_type('on_hover')
        self.register_event_type('on_release')
        super(ColorSwatch,self).__init__(**kwargs)

        self.bind(color=self._redraw)
        self.bind(size=self._update_rec, pos=self._update_rec)
        self._redraw()


    def _redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            self._rec = Rectangle(size=self.size, pos=self.pos)

    def _update_rec(self, *args):
        self._rec.size = self.size
        self._rec.pos = self.pos


    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_press')
            return True

    def on_touch_move(self,touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_hover')
            return True

    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_release')
            return True


    def on_press(self,*args):
        """Event triggered when touch down intersects swatch"""
        pass
    def on_hover(self,*args):
        """Event triggered when touch move intersects swatch"""
        pass
    def on_release(self,*args):
        """Event triggered when touch up intersects swatch"""
        pass


class ColorChooserGrid(GridLayout):
    """Presents a grid of color swatches to choose from. Displays 8 columns
    (7 colors plus one column of greys) and `rows` rows. Each column
    displays different shades of a color.
    """

    color = ListProperty([1,1,1])
    """:class:`~kivy.properties.ListProperty`, defaults to [1,1,1].
    Color of the most recently touched swatch.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("rows", 7)
        super(ColorChooserGrid,self).__init__(**kwargs)
        self.bind(rows=self._redraw)
        self._redraw()

    def _redraw(self, *args):
        self.clear_widgets()
        for r in range(self.rows):
            for c in grid_colors:
                swatch = ColorSwatch(color=get_shade(c, r, self.rows))
                swatch.bind(on_press=self.on_activity, on_hover=self.on_activity, on_release=self.on_activity)
                self.add_widget(swatch)

    # No need to pass touches to children unless touch is in our bbox
    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            return super(ColorChooserGrid,self).on_touch_down(touch)
    def on_touch_move(self,touch):
        if self.collide_point(*touch.pos):
            return super(ColorChooserGrid,self).on_touch_move(touch)
    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            return super(ColorChooserGrid,self).on_touch_up(touch)

    def on_activity(self,swatch):
        self.color = swatch.color



Factory.register("ColorChooserGrid", ColorChooserGrid)
