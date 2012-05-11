# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty

from ttlib import ttlib_dir

class TTApp(App):
    screen = StringProperty("")

    def build(self):
        super(TTApp, self).build()
        kivy.resources.resource_add_path(ttlib_dir("data/glyphicons"))
        kivy.resources.resource_add_path(self.data_dir("glyphicons"))
        kivy.resources.resource_add_path(self.data_dir("themes/default"))
        self.theme = self.config.get(self.app_name, 'theme')
        if self.theme != 'default':
            kivy.resources.resource_add_path(self.data_dir("themes", self.theme))
        self.goto_screen("new")

    def on_start(self):
        super(TTApp, self).on_start()
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, win, key, scancode, string, modifiers):
        if key == 292:
            win.toggle_fullscreen()
            win.update_viewport()
            return True
        elif key == 27:
            if self.screen == "new":
                exit()
            else:
                self.goto_screen("new")
            return True

    def on_config_change(self, config, section, key, value):
        super(TTApp, self).on_config_change(config, section, key, value)
        if config is self.config:
            if (section, key) == (self.app_name, 'theme'):
                if self.theme != value:
                    if self.theme != 'default':
                        kivy.resources.resource_remove_path(self.data_dir("themes", self.theme))
                    if value != 'default':
                        kivy.resources.resource_add_path(self.data_dir("themes", value))
                    self.theme = value

    def goto_screen(self, screen_name, **kwargs):
        self.root.clear_widgets()
