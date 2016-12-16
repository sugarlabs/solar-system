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

from utils import get_data_file
from constants import Cursor, CelestialBodyType

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit", "3.0")

from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import WebKit
from gi.repository import GObject


class WebView(WebKit.WebView):

    def __init__(self):
        WebKit.WebView.__init__(self)


class InfoView(Gtk.VBox):

    __gsignals__ = {
        "change-cursor": (GObject.SIGNAL_RUN_FIRST, None, [int]),
    }

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.body = None

        self.scroll = Gtk.ScrolledWindow()
        self.pack_start(self.scroll, True, True, 0)

        self.view = WebView()
        self.scroll.add(self.view)

    def set_body(self, body):
        self.body = body
        self.emit("change-cursor", Cursor.LOADING)
        self.load_info(body)
        self.emit("change-cursor", Cursor.ARROW)

        self.show_all()

    def load_info(self, body):
        if body == CelestialBodyType.CELESTIAL_BODY:
            #self.load_file()
            pass

        elif body == CelestialBodyType.STAR:
            #self.load_file()
            pass

        elif body == CelestialBodyType.PLANET:
            #self.load_file()
            pass

        elif body == CelestialBodyType.DWARF_PLANET:
            #self.load_file()
            pass

        elif body == CelestialBodyType.NATURAL_SATELLITE:
            #self.load_file()
            pass

        elif body == CelestialBodyType.SUN:
            #self.load_file()
            pass

        elif body == CelestialBodyType.MERCURY:
            self.load_file(get_data_file("mercury"))

        elif body == CelestialBodyType.VENUS:
            self.load_file(get_data_file("venus"))

        elif body == CelestialBodyType.EARTH:
            self.load_file(get_data_file("earth"))

        elif body == CelestialBodyType.MARS:
            self.load_file(get_data_file("mars"))

        elif body == CelestialBodyType.JUPITER:
            self.load_file(get_data_file("jupiter"))

        elif body == CelestialBodyType.SATURN:
            self.load_file(get_data_file("saturn"))

        elif body == CelestialBodyType.URANUS:
            self.load_file(get_data_file("uranus"))

        elif body == CelestialBodyType.NEPTUNE:
            self.load_file(get_data_file("neptune"))

        elif body == CelestialBodyType.MOON:
            #self.load_file()
            pass

    def load_file(self, file_path):
        self.view.open(file_path)
