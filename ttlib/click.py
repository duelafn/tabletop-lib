# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy
from kivy.factory import Factory
from kivy.uix.widget import Widget

class DblTap(Widget):
    """Implements double-tap handling for kivy widgets

    Passes touch events to parent classes.
    Performs state changes when possible (useful when parent is a Button)
    """

    def __init__(self, **kwargs):
        self.register_event_type('on_dbl_tap')
        super(DblTap, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if touch.is_double_tap:
            touch.grab(self)
            if hasattr(self, "_do_press"):
                self._do_press()
            self.dispatch('on_dbl_tap')
            return True
        return super(DblTap, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(DblTap, self).on_touch_up(touch)
        touch.ungrab(self)
        if hasattr(self, "_do_release"):
            self._do_release()
        return True

    def on_dbl_tap(self):
        pass

Factory.register("DblTap", DblTap)
