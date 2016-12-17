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
from gettext import gettext as _

AU_KM = 149597870.7
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))


class Screen:
    SOLAR_SYSTEM = 0
    INFO = 1


class Cursor:
    ARROW = 0
    LOADING = 1


class CelestialBodyType:
    CELESTIAL_BODY    = 0
    STAR              = 1
    PLANET            = 2
    DWARF_PLANET      = 3
    NATURAL_SATELLITE = 4
    SUN               = 5
    MERCURY           = 6
    VENUS             = 7
    EARTH             = 8
    MARS              = 9
    JUPITER           = 10
    SATURN            = 11
    URANUS            = 12
    NEPTUNE           = 13
    MOON              = 14
    FOBOS             = 15
    DEIMOS            = 16
    IO                = 17
    EUROPA            = 18
    GANYMEDE          = 19
    CALLISTO          = 20


class Color:
    BACKGROUND = (0, 0, 0)
    SELECTED = (0.2, 1.0, 0.2)

    # Celestial Bodies
    SUN      = (1.0, 1.0, 0.690196078)
    MERCURY  = (0.81568627451, 0.639215686275, 0.411764705882)
    VENUS    = (0.949019607843, 0.470588235294, 0.211764705882)
    EARTH    = (0.462745098039, 0.545098039216, 0.745098039216)
    MARS     = (0.749019607843, 0.364705882353, 0.313725490196)
    JUPITER  = (0.874509803922, 0.549019607843, 0.235294117647)
    SATURN   = (0.811764705882, 0.721568627451, 0.611764705882)
    URANUS   = (0.654901960784, 0.772549019608, 0.823529411765)
    NEPTUNE  = (0.388235294118, 0.541176470588, 0.949019607843)
    MOON     = (0.8, 0.8, 0.8)
    FOBOS    = (0.5, 0.5, 0.5)
    DEIMOS   = (0.65, 0.65, 0.65)
    IO       = (0.945098039216, 0.839215686275, 0.521568627451)
    EUROPA   = (0.717647058824, 0.58431372549, 0.403921568627)
    GANYMEDE = (0.572549019608, 0.505882352941, 0.435294117647)
    CALLISTO = (0.450980392157, 0.372549019608, 0.274509803922)


class OrbitTime:  # Days
    MERCURY = 87.9775
    VENUS   = 224.701
    EARTH   = 365.256363004
    MARS    = 779.96
    JUPITER = 4332.865826377
    SATURN  = 10759.713693783
    URANUS  = 30777.895
    NEPTUNE = 60190

    MOON     = 27.32
    FOBOS    = 0.31891023
    DEIMOS   = 1.262
    IO       = 1.769166667
    EUROPA   = 3.551805556
    GANYMEDE = 7.15455296
    CALLISTO = 16.6890184


class Radius:  # Km
    SUN     = 695700

    MERCURY = 2440
    VENUS   = 6052
    EARTH   = 6371
    MARS    = 3390
    JUPITER = 69911
    SATURN  = 58232
    URANUS  = 25362
    NEPTUNE = 24622

    MOON     = 1737
    FOBOS    = 11
    DEIMOS   = 12
    IO       = 1821.6
    EUROPA   = 1560.8
    GANYMEDE = 2634.1
    CALLISTO = 2410.3


class OrbitalRadius:  # AU
    MERCURY = 0.387
    VENUS   = 0.72333199
    EARTH   = 1.0
    MARS    = 1.523662
    JUPITER = 5.20336301
    SATURN  = 9.53707032
    URANUS  = 19.1912639
    NEPTUNE = 30.0689634

    MOON     = 0.00256955  # To earth
    FOBOS    = 0.0000626827104  # To mars
    DEIMOS   = 0.00015682041  # To mars
    IO       = 0.00281822193  # To Jupiter
    EUROPA   = 0.0044846895  # To Jupiter
    GANYMEDE = 0.007155182056  # To Jupiter
    CALLISTO = 0.01256702379  # To Jupiter


class BodyName:
    SUN = _("Sun")

    MERCURY = _("Mercury")
    VENUS   = _("Venus")
    EARTH   = _("Earth")
    MARS    = _("Mars")
    JUPITER = _("Jupiter")
    SATURN  = _("Saturn")
    URANUS  = _("Uranus")
    NEPTUNE = _("Neptune")

    MOON     = _("Moon")
    FOBOS    = _("Fobos")
    DEIMOS   = _("Deimos")
    IO       = _("Io")
    EUROPA   = _("Europa")
    GANYMEDE = _("Ganymede")
    CALLISTO = _("Callisto")


class Speed:
    STOPPED = 0
    SLOW = 1
    NORMAL  = 5
    FAST    = 10
