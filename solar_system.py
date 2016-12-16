#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, Cristian García <cristian99garcia@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from constants import Screen
from constants import Cursor
from area import Area
from infoview import InfoView

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


class SolarSystem(Gtk.VBox):

    __gsignals__ = {
        "view-changed": (GObject.SIGNAL_RUN_FIRST, None, [int])
    }

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.screen = None

        self.area = Area()
        self.area.connect("body-selected", self._body_selected)

        self.info_view = InfoView()
        self.info_view.connect("change-cursor", self._change_cursor)

        adj = Gtk.Adjustment(10, 0.2, 100, 0.5, 1)
        s = Gtk.HScale()
        s.set_draw_value(False)
        s.set_adjustment(adj)
        s.connect("value-changed", self.change_zoom)
        self.pack_start(s, False, False, 0)

        adj = Gtk.Adjustment(1, 0.1, 5, 0.1, 1)
        s = Gtk.HScale()
        s.set_draw_value(False)
        s.set_adjustment(adj)
        s.connect("value-changed", self.change_speed)
        self.pack_start(s, False, False, 0)

        self.set_screen(Screen.SOLAR_SYSTEM)
        self.show_all()

    def _body_selected(self, widget, body):
        self.set_screen(Screen.INFO)
        self.info_view.set_body(body)

    def _change_cursor(self, widget, cursor):
        if self.get_window() == None:
            return

        cursor_type = None

        if cursor == Cursor.ARROW:
            cursor_type = Gdk.CursorType.ARROW

        elif cursor == Cursor.LOADING:
            cursor_type = Gdk.CursorType.WATCH

        if cursor_type != None:
            self.get_window().set_cursor(Gdk.Cursor(cursor_type))

    def change_zoom(self, widget):
        self.area.zoom = widget.get_value()

    def change_speed(self, widget):
        self.area.speed = widget.get_value()

    def set_screen(self, screen):
        if screen == self.screen:
            return

        self.screen = screen

        if self.screen == Screen.SOLAR_SYSTEM:
            if self.info_view.get_parent() == self:
                self.remove(self.info_view)

            if self.area.get_parent() == None:
                self.pack_start(self.area, True, True, 0)
                self.reorder_child(self.area, 0)

        elif self.screen == Screen.INFO:
            if self.area.get_parent() == self:
                self.remove(self.area)

            if self.info_view.get_parent() == None:
                self.pack_start(self.info_view, True, True, 0)
                self.reorder_child(self.info_view, 0)


if __name__ == "__main__":
    win = Gtk.Window()
    win.set_title("Solar System")
    win.set_default_size(560, 480)
    #win.maximize()
    win.connect("destroy", Gtk.main_quit)

    solar_system = SolarSystem()
    win.add(solar_system)

    win.show_all()

    Gtk.main()
