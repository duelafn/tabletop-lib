# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.settings import SettingItem

from ttlib import ttlib_dir

class TTSettingInt(SettingItem):
    minimum = NumericProperty(0)
    maximum = NumericProperty(float("inf"))
    step    = NumericProperty(1)
    plus    = ObjectProperty(None)
    minus   = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TTSettingInt, self).__init__(**kwargs)
        self.minus.children[0].source = ttlib_dir("data/glyphicons/circle_minus.png")
        self.plus.children[0].source  = ttlib_dir("data/glyphicons/circle_plus.png")

    def step_up(self, obj):
        if int(self.value) < self.maximum:
            self.value = str( min(self.maximum, int(self.value) + self.step) )

    def step_down(self, obj):
        if int(self.value) > self.minimum:
            self.value = str( max(self.minimum, int(self.value) - self.step) )

Builder.load_file(ttlib_dir("ttsettingint.kv"), rulesonly=True)
