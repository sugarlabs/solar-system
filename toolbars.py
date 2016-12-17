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

from gettext import gettext as _

from utils import make_separator
from utils import get_icon_name
from utils import get_body_name
from constants import Screen
from constants import BodyName
from constants import CelestialBodyType

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GObject

from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.radiotoolbutton import RadioToolButton
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton
from sugar3.graphics.toolbarbox import ToolbarBox as SugarToolbarBox
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton


class ToolbarInfo(Gtk.Toolbar):

    __gsignals__ = {
        "show-simulation": (GObject.SIGNAL_RUN_FIRST, None, []),
        "show-info": (GObject.SIGNAL_RUN_FIRST, None, []),
        "go-back": (GObject.SIGNAL_RUN_FIRST, None, []),
        "go-forward": (GObject.SIGNAL_RUN_FIRST, None, []),
    }

    def __init__(self):
        Gtk.Toolbar.__init__(self)

        self.button = ToolbarButton(page=self, icon_name="info")

        self.button_simulation = RadioToolButton(icon_name="solar-system", group=None)
        self.button_simulation.set_tooltip(_("Show solar system"))
        self.button_simulation.connect("toggled", self._show_simulation_cb)
        self.insert(self.button_simulation, -1)

        self.button_info = RadioToolButton(icon_name="info", group=self.button_simulation)
        self.button_info.set_tooltip(_("Show information"))
        self.button_info.connect("toggled", self._show_info_cb)
        self.insert(self.button_info, -1)

        self.insert(make_separator(False), -1)

        self.back_button = ToolButton("go-previous-paired")
        self.back_button.set_tooltip(_("Go back"))
        self.back_button.set_sensitive(False)
        self.back_button.connect("clicked", self._go_back_cb)
        self.insert(self.back_button, -1)

        self.forward_button = ToolButton("go-next-paired")
        self.forward_button.set_tooltip(_("Go forward"))
        self.forward_button.set_sensitive(False)
        self.forward_button.connect("clicked", self._go_forward_cb)
        self.insert(self.forward_button, -1)

        self.show_all()

    def _show_simulation_cb(self, widget):
        self.emit("show-simulation")

    def _show_info_cb(self, widget):
        self.emit("show-info")

    def _go_back_cb(self, widget):
        self.emit("go-back")

    def _go_forward_cb(self, widget):
        self.emit("go-forward")

    def select_screen(self, screen):
        if screen == Screen.SOLAR_SYSTEM:
            self.button_simulation.props = True

        elif screen == Screen.INFO:
            self.button_info.props.active = True


class ToolbarView(Gtk.Toolbar):

    __gsignals__ = {
        "show-orbits": (GObject.SIGNAL_RUN_FIRST, None, [bool]),
        "show-body": (GObject.SIGNAL_RUN_FIRST, None, [int, bool]),
        "zoom-changed": (GObject.SIGNAL_RUN_FIRST, None, [float]),
    }

    def __init__(self):
        Gtk.Toolbar.__init__(self)

        self.button = ToolbarButton(page=self, icon_name="toolbar-view")

        self.buttons = {
            CelestialBodyType.MERCURY: None,
            CelestialBodyType.VENUS: None,
            CelestialBodyType.EARTH: None,
            CelestialBodyType.MARS: None,
            CelestialBodyType.JUPITER: None,
            CelestialBodyType.SATURN: None,
            CelestialBodyType.URANUS: None,
            CelestialBodyType.NEPTUNE: None
        }

        orbits_button = ToggleToolButton("show-orbits")
        orbits_button.set_tooltip(_("Show planets orbits"))
        orbits_button.connect("toggled", self._show_orbits_cb)
        self.insert(orbits_button, -1)

        self.insert(make_separator(False), -1)

        for planet in self.buttons:
            button = ToggleToolButton(get_icon_name(planet))
            button.set_tooltip(get_body_name(planet))
            button.set_active(True)
            button.connect("toggled", self._show_planet_cb, planet)
            self.insert(button, -1)

            self.buttons[planet] = button

        self.insert(make_separator(False), -1)

        adj = Gtk.Adjustment(1, 0.8, 500, 0.5, 1)
        zoom_scale = Gtk.HScale()
        zoom_scale.set_draw_value(False)
        zoom_scale.set_adjustment(adj)
        zoom_scale.set_size_request(200, 1)
        zoom_scale.connect("value-changed", self._zoom_changed_cb)

        zoom_out = ToolButton("zoom-out")
        zoom_out.set_tooltip(_("Zoom out"))
        zoom_out.connect("clicked", self._zoom_out_cb, zoom_scale)
        self.insert(zoom_out, -1)

        item = Gtk.ToolItem()
        item.add(zoom_scale)
        self.insert(item, -1)

        zoom_in = ToolButton("zoom-in")
        zoom_in.set_tooltip(_("Zoom in"))
        zoom_in.connect("clicked", self._zoom_in_cb, zoom_scale)
        self.insert(zoom_in, -1)

        self.show_all()

    def _show_orbits_cb(self, button):
        self.emit("show-orbits", button.get_active())

    def _show_planet_cb(self, button, planet):
        self.emit("show-body", planet, button.get_active())

    def _zoom_changed_cb(self, scale):
        self.emit("zoom-changed", scale.get_value())

    def _zoom_out_cb(self, widget, scale):
        new_value = scale.get_value() - 2.5
        lower_value = scale.get_adjustment().get_lower()
        if new_value < lower_value:
            scale.set_value(lower_value)

        else:
            scale.set_value(new_value)

    def _zoom_in_cb(self, widget, scale):
        new_value = scale.get_value() + 2.5
        upper = scale.get_adjustment().get_upper()
        if new_value > upper:
            scale.set_value(upper)

        else:
            scale.set_value(new_value)


class ToolbarBox(SugarToolbarBox):

    __gsignals__ = {
        "show-simulation": (GObject.SIGNAL_RUN_FIRST, None, []),
        "show-info": (GObject.SIGNAL_RUN_FIRST, None, []),
        "go-back": (GObject.SIGNAL_RUN_FIRST, None, []),
        "go-forward": (GObject.SIGNAL_RUN_FIRST, None, []),
        "show-orbits": (GObject.SIGNAL_RUN_FIRST, None, [bool]),
        "show-body": (GObject.SIGNAL_RUN_FIRST, None, [int, bool]),
        "speed-changed": (GObject.SIGNAL_RUN_FIRST, None, [float]),
        "zoom-changed": (GObject.SIGNAL_RUN_FIRST, None, [float]),
    }

    def __init__(self, activity):
        SugarToolbarBox.__init__(self)

        activity_button = ActivityToolbarButton(activity)
        self.toolbar.insert(activity_button, -1)

        self.toolbar.insert(make_separator(False), -1)

        self.toolbar_info = ToolbarInfo()
        self.toolbar_info.connect("show-simulation", self._show_simulation_cb)
        self.toolbar_info.connect("show-info", self._show_info_cb)
        self.toolbar_info.connect("go-back", self._go_back_cb)
        self.toolbar_info.connect("go-forward", self._go_forward_cb)
        self.toolbar.insert(self.toolbar_info.button, -1)

        self.toolbar_view = ToolbarView()
        self.toolbar_view.connect("show-orbits", self._show_orbits_cb)
        self.toolbar_view.connect("show-body", self._show_body_cb)
        self.toolbar_view.connect("zoom-changed", self._zoom_changed_cb)
        self.toolbar.insert(self.toolbar_view.button, -1)

        self.toolbar.insert(make_separator(False), -1)

        adj = Gtk.Adjustment(1, 0, 15, 0.1, 1)
        speed_scale = Gtk.HScale()
        speed_scale.set_draw_value(False)
        speed_scale.set_adjustment(adj)
        speed_scale.set_size_request(200, 1)
        speed_scale.connect("value-changed", self._speed_changed_cb)

        slow_button = ToolButton("speed-down")
        slow_button.set_tooltip(_("Slow down"))
        slow_button.connect("clicked", self._speed_down_cb, speed_scale)
        self.toolbar.insert(slow_button, -1)

        item = Gtk.ToolItem()
        item.add(speed_scale)
        self.toolbar.insert(item, -1)

        fast_button = ToolButton("speed-up")
        fast_button.set_tooltip(_("Speed up"))
        fast_button.connect("clicked", self._speed_up_cb, speed_scale)
        self.toolbar.insert(fast_button, -1)

        self.toolbar.insert(make_separator(True), -1)

        stop_button = StopButton(activity)
        self.toolbar.insert(stop_button, -1)

    def set_can_back_back(self, can):
        self.toolbar_info.button_back.set_sensitive(can)

    def set_can_go_forward(self, can):
        self.toolbar_info.forward_button.set_sensitive(can)

    def _speed_down_cb(self, widget, scale):
        new_value = scale.get_value() - 0.5
        lower_value = scale.get_adjustment().get_lower()
        if new_value < lower_value:
            scale.set_value(lower_value)

        else:
            scale.set_value(new_value)

    def _speed_up_cb(self, widget, scale):
        new_value = scale.get_value() + 0.5
        upper = scale.get_adjustment().get_upper()
        if new_value > upper:
            scale.set_value(upper)

        else:
            scale.set_value(new_value)

    def _show_simulation_cb(self, widget):
        self.emit("show-simulation")

    def _show_info_cb(self, widget):
        self.emit("show-info")

    def _go_back_cb(self, widget):
        self.emit("go-back")

    def _go_forward_cb(self, widget):
        self.emit("go-forward")

    def _speed_changed_cb(self, scale):
        self.emit("speed-changed", scale.get_value())

    def _show_orbits_cb(self, toolbar, show):
        self.emit("show-orbits", show)

    def _show_body_cb(self, toolbar, body, show):
        self.emit("show-body", body, show)

    def _zoom_changed_cb(self, toolbar, zoom):
        self.emit("zoom-changed", zoom)

    def select_screen(self, screen):
        self.toolbar_info.select_screen(screen)

    def set_can_go_forward(self, can):
        self.toolbar_info.forward_button.set_sensitive(can)

    def set_can_go_back(self, can):
        self.toolbar_info.back_button.set_sensitive(can)
