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

from area import Area
from infoview import InfoView
from toolbars import ToolbarBox
from constants import Screen
from constants import Cursor
from utils import get_data_file

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from sugar3.activity import activity


class SolarSystem(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.screen = None

        self.toolbarbox = ToolbarBox(self)
        self.toolbarbox.connect("show-simulation", self._show_simulation_cb)
        self.toolbarbox.connect("show-info", self._show_info_cb)
        self.toolbarbox.connect("go-back", self._go_back_cb)
        self.toolbarbox.connect("go-forward", self._go_forward_cb)
        self.toolbarbox.connect("show-orbits", self._show_orbits_cb)
        self.toolbarbox.connect("show-body", self._show_body_cb)
        self.toolbarbox.connect("speed-changed", self._speed_changed_cb)
        self.toolbarbox.connect("zoom-changed", self._zoom_changed_cb)
        self.set_toolbar_box(self.toolbarbox)

        self.box = Gtk.VBox()
        self.set_canvas(self.box)

        self.area = Area()
        self.area.connect("body-selected", self._body_selected)

        self.info_view = InfoView()
        self.info_view.connect("change-cursor", self._change_cursor)
        self.info_view.connect("can-go-back", self._can_go_back_cb)
        self.info_view.connect("can-go-forward", self._can_go_forward_cb)

        self.set_screen(Screen.SOLAR_SYSTEM)
        self.show_all()

    def set_screen(self, screen):
        if screen == self.screen:
            return

        self.screen = screen

        if self.screen == Screen.SOLAR_SYSTEM:
            self.toolbarbox.set_can_go_back(False)
            self.toolbarbox.set_can_go_forward(False)
            self.toolbarbox.enable_simulation_widgets()

            if self.info_view.get_parent() == self.box:
                self.box.remove(self.info_view)

            if self.area.get_parent() == None:
                self.box.pack_start(self.area, True, True, 0)
                self.box.reorder_child(self.area, 0)

        elif self.screen == Screen.INFO:
            self.toolbarbox.set_can_go_back(self.info_view.view.can_go_back())
            self.toolbarbox.set_can_go_forward(self.info_view.view.can_go_forward())
            self.toolbarbox.disable_simulation_widgets()

            if self.area.get_parent() == self.box:
                self.box.remove(self.area)

            if self.info_view.get_parent() == None:
                self.box.pack_start(self.info_view, True, True, 0)
                self.box.reorder_child(self.info_view, 0)

        self.toolbarbox.select_screen(self.screen)
        self.show_all()

    def _show_simulation_cb(self, widget):
        self.set_screen(Screen.SOLAR_SYSTEM)

    def _show_info_cb(self, widget):
        if self.screen != Screen.INFO:
            self.set_screen(Screen.INFO)
            self.info_view.load_file(get_data_file("index"))

    def _go_back_cb(self, widget):
        self.info_view.back()

    def _go_forward_cb(self, widget):
        self.info_view.forward()

    def _show_orbits_cb(self, widget, show):
        self.area.set_show_orbits(show)

    def _show_body_cb(self, widget, body, show):
        self.area.set_body_visible(body, show)

    def _speed_changed_cb(self, widget, speed):
        self.area.set_speed(speed)

    def _zoom_changed_cb(self, widget, zoom):
        self.area.set_zoom(zoom)

    def _body_selected(self, widget, body):
        print body, self.screen, Screen.INFO
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

    def _can_go_back_cb(self, widget, can):
        self.toolbarbox.set_can_go_back(can)

    def _can_go_forward_cb(self, widget, can):
        self.toolbarbox.set_can_go_forward(can)
