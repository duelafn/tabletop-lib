#!/usr/bin/python

import sys
sys.path.extend([".", ".."])


import kivy
import ttlib.colorchooser

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle, Color


class ColorChooserTest(App):
    def on_start(self):
        super(ColorChooserTest,self).on_start()

        def update_color(*args):
            color = self.root.chooser.color[0:3] + [1]
            self.root.button.background_color = color
            self.root.widget.canvas.clear()
            with self.root.widget.canvas:
                Color(*color)
                Rectangle(pos=self.root.widget.pos, size=self.root.widget.size)

        self.root.chooser.bind(color=update_color)


if __name__ in ('__main__', '__android__'):
    ColorChooserTest().run()
