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

import math

from constants import Color
from constants import BodyName
from constants import Speed
from utils import get_sun_scale_radius
from utils import get_planet_scale_radius
from utils import au_to_pixels
from celestial_bodies import Sun

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


class Area(Gtk.DrawingArea):

    __gsignals__ = {
        "body-selected": (GObject.SIGNAL_RUN_FIRST, None, [int]),
    }

    def __init__(self):
        Gtk.DrawingArea.__init__(self)

        self.width = 0
        self.height = 0
        self.speed = Speed.SLOW
        self.zoom = 16.5
        self.big_planets = False
        self.show_orbits = True
        self.sun = Sun()
        self.centered = self.sun
        self.x = 0
        self.y = 0

        self.draw_x = None
        self.draw_y = None
        self.select_body = True

        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK |
                        Gdk.EventMask.BUTTON_MOTION_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK)

        self.orbit_id = GObject.timeout_add(100, self._orbit)

        self.connect("draw", self.__draw_cb)
        self.connect("button-press-event", self.__press_cb)
        self.connect("button-release-event", self.__release_cb)
        self.connect("motion-notify-event", self.__motion_cb)

        self.redraw()

    def _orbit(self):
        for idx in range(0, len(self.sun.planets)):
            planet = self.sun.planets[idx]
            planet.advance(self.speed)
            planet.calculate_position(self.width, self.height, self.zoom)

            for satellite in planet.natural_satellites:
                satellite.advance(self.speed)
                satellite.calculate_position(self.width, self.height, self.zoom)

        return True

    def redraw(self):
        GObject.idle_add(self.queue_draw)
        GObject.idle_add(self.redraw)

    def __draw_cb(self, widget, context):
        self._calculate()
        self._draw_background(context)
        self._draw_celestial_bodies(context)

    def __press_cb(self, widget, event):
        self.draw_x = event.x
        self.draw_y = event.y
        self.select_body = True

    def __release_cb(self, widget, event):
        self.draw_x = None
        self.draw_y = None

        if self.select_body:
            for body in self.get_all_bodies():
                if body.preselected:
                    self.emit("body-selected", body.type)

        self.select_body = True

    def __motion_cb(self, widget, event):
        if self.draw_x is not None:
            self.select_body = False

            self.x += (event.x - self.draw_x)
            self.y += (event.y - self.draw_y)

            self.draw_x = event.x
            self.draw_y = event.y

        else:
            self.check_preselected_bodies(event)

    def _calculate(self):
        allocation = self.get_allocation()
        self.width = allocation.width
        self.height = allocation.height

    def _draw_background(self, context):
        # TODO: Draw Milky Way
        context.set_source_rgb(*Color.BACKGROUND)
        context.rectangle(0, 0, self.width, self.height)
        context.fill()

    def _draw_celestial_bodies(self, context):
        for planet in self.sun.planets:
            if not planet.visible:
                continue

            radius = get_planet_scale_radius(self.width, self.height, planet, self.zoom)
            if self.big_planets:
                radius = min(10 * radius, 35)

            x = self.x + planet.x + self.width / 2.0
            y = self.y + planet.y + self.height / 2.0
            context.set_source_rgb(*planet.color)
            context.arc(x, y, radius, 0, 2 * math.pi)
            context.fill()

            if self.show_orbits:
                radius = au_to_pixels(self.width, self.height, planet.orbital_radius, self.zoom) + get_sun_scale_radius(self.width, self.height, self.zoom)
                context.set_source_rgb(*planet.color)
                context.arc(self.x + self.width / 2, self.y + self.height / 2, radius, 0, 2 * math.pi)
                context.stroke()

            for satellite in planet.natural_satellites:
                if not satellite.visible:
                    continue

                radius = get_planet_scale_radius(self.width, self.height, satellite, self.zoom)
                if radius >= 1:
                    context.set_source_rgb(*satellite.color)
                    context.arc(x + satellite.x, y + satellite.y, radius, 0, 2 * math.pi)
                    context.fill()

        for body in self.get_all_bodies():
            if not body.preselected or not body.visible:
                continue

            x = self.x + body.x + self.width / 2.0
            y = self.y + body.y + self.height / 2.0

            if self.big_planets:
                radius = min(10 * radius, 35)

            context.set_source_rgb(*Color.SELECTED)
            context.arc(x, y, self.get_body_radius(body), 0, 2 * math.pi)
            context.stroke()

            break

        radius = get_sun_scale_radius(self.width, self.height, self.zoom)
        context.set_source_rgb(*self.sun.color)
        context.arc(self.x + self.width / 2, self.y + self.height / 2, radius, 0, 2 * math.pi)
        context.fill()

    def get_all_bodies(self):
        bodies = [self.sun]

        for planet in self.sun.planets:
            bodies.append(planet)

            for satellite in planet.natural_satellites:
                bodies.append(satellite)

        return bodies

    def get_body_radius(self, body):
        if body.name == BodyName.SUN:
            return get_sun_scale_radius(self.width, self.height, self.zoom)

        else:
            return get_planet_scale_radius(self.width, self.height, body, self.zoom)

    def check_preselected_bodies(self, event):
        for body in self.get_all_bodies():
            radius = self.get_body_radius(body)
            x = self.x + body.x + self.width / 2.0
            y = self.y + body.y + self.height / 2.0
            body.preselected = event.x > x - radius and event.x < x + radius and event.y > y - radius and event.y < y + radius

    def set_show_orbits(self, orbits):
        self.show_orbits = orbits

    def set_body_visible(self, body_type, visible):
        for body in self.get_all_bodies():
            if body.type == body_type:
                body.visible = visible
                break

    def set_speed(self, speed):
        self.speed = speed

    def set_zoom(self, zoom):
        self.zoom = zoom
