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

import os
import math

from constants import Radius
from constants import OrbitalRadius
from constants import AU_KM
from constants import LOCAL_DIR
from constants import CelestialBodyType
from constants import BodyName

from gi.repository import Gtk


def get_sun_scale_radius(width, height, zoom):
    #return Radius.SUN / 30000.0 * ((zoom) / (zoom + .15))
    return km_to_pixels(width, height, Radius.SUN, zoom) * 100


def get_planet_scale_radius(width, height, planet, zoom):
    #return planet.radius / 5000.0 * zoom
    return km_to_pixels(width, height, planet.radius, zoom) * 1000


def km_to_pixels(width, height, distance, zoom):
    radius = min(width, height) / 2.0 - 50
    return radius / (OrbitalRadius.NEPTUNE * AU_KM) * distance * zoom


def au_to_pixels(width, height, distance, zoom):
    return km_to_pixels(width, height, distance * AU_KM, zoom)


def get_data_file(name):
    return "file://" + os.path.join(LOCAL_DIR, "data", name + ".html")


def make_separator(expand=False):
    separator = Gtk.SeparatorToolItem()
    if expand:
        separator.set_expand(True)
        separator.props.draw = False

    return separator


def get_icon_name(body):
    if body == CelestialBodyType.MERCURY:
        return "mercury"

    elif body == CelestialBodyType.VENUS:
        return "venus"

    elif body == CelestialBodyType.EARTH:
        return "earth"

    elif body == CelestialBodyType.MARS:
        return "mars"

    elif body == CelestialBodyType.JUPITER:
        return "jupiter"

    elif body == CelestialBodyType.SATURN:
        return "saturn"

    elif body == CelestialBodyType.URANUS:
        return "uranus"

    elif body == CelestialBodyType.NEPTUNE:
        return "neptune"

    return ""


def get_body_name(body):
    if body == CelestialBodyType.SUN:
        return BodyName.SUN

    elif body == CelestialBodyType.MERCURY:
        return BodyName.MERCURY

    elif body == CelestialBodyType.VENUS:
        return BodyName.VENUS

    elif body == CelestialBodyType.EARTH:
        return BodyName.EARTH

    elif body == CelestialBodyType.MARS:
        return BodyName.MARS

    elif body == CelestialBodyType.JUPITER:
        return BodyName.JUPITER

    elif body == CelestialBodyType.SATURN:
        return BodyName.SATURN

    elif body == CelestialBodyType.URANUS:
        return BodyName.URANUS

    elif body == CelestialBodyType.NEPTUNE:
        return BodyName.NEPTUNE

    elif body == CelestialBodyType.MOON:
        return BodyName.MOON

    return _("Unknown")
