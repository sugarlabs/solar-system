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

from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import GObject


class InfoView(Gtk.VBox):

    __gsignals__ = {
        "change-cursor": (GObject.SIGNAL_RUN_FIRST, None, [int]),
    }

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.body = None

        self.scroll = Gtk.ScrolledWindow()
        self.pack_start(self.scroll, True, True, 0)

        self.view = Gtk.TextView()
        self.view.set_top_margin(15)
        self.view.set_bottom_margin(15)
        self.view.set_left_margin(30)
        self.view.set_right_margin(30)
        self.view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.view.override_font(Pango.FontDescription("12"))
        self.view.set_editable(False)
        self.view.set_cursor_visible(False)
        self.scroll.add(self.view)

        self.buffer = self.view.get_buffer()
        self.buffer.create_tag("title", font="20", weight=Pango.Weight.BOLD, pixels_below_lines=10)
        self.buffer.create_tag("subtitle", font="14", weight=Pango.Weight.BOLD, pixels_below_lines=6)

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

    def _add_text_with_tag(self, text, tag):
        self.buffer.insert_with_tags_by_name(self.buffer.get_end_iter(), text, tag)

    def _add_text(self, text):
        self.buffer.insert(self.buffer.get_end_iter(), text)

    def load_file(self, file_path):
        with open(file_path) as file:
            empty_line = False

            for line in file.read().splitlines():
                if line.strip() == "" and not empty_line:
                    empty_line = True

                elif line.strip() == "" and empty_line:
                    empty_line = False
                    continue

                elif line.strip() != "":
                    empty_line = False

                if line.startswith("[[") and line.endswith("]]"):
                    self._add_text_with_tag(line[2:-2] + "\n", "title")

                elif line.startswith("[") and line.endswith("]"):
                    self._add_text_with_tag(line[1:-1] + "\n", "subtitle")

                elif line.startswith("#"):
                    empty_line = True
                    continue

                else:
                    self._add_text(line + "\n")
