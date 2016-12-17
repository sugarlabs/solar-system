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
import random

from constants import Color, OrbitTime, Radius, OrbitalRadius, BodyName, CelestialBodyType
from utils import km_to_pixels, au_to_pixels, get_sun_scale_radius, get_planet_scale_radius


class CelestialBody(object):

    def __init__(self):
        self.type = CelestialBodyType.CELESTIAL_BODY

        # Draw values
        self.x = 0
        self.y = 0
        self.color = (0, 0, 0)
        self.preselected = False
        self.visible = True

        # Data values
        self.radius = 0
        self.name = ""


class Star(CelestialBody):

    def __init__(self):
        CelestialBody.__init__(self)

        self.type = CelestialBodyType.STAR
        self.planets = []


class OrbitCelestialBody(CelestialBody):

    def __init__(self, around_the=None):
        CelestialBody.__init__(self)

        self.angle = random.randint(0, 359)
        self.orbit_time = 0
        self.orbital_radius = 0
        self.around_the = around_the

    def calculate_position(self, width, height, zoom):
        pass

    def advance(self, speed):
        self.angle += 360.0 / self.orbit_time * speed

        if self.angle >= 360:
            self.angle -= 360


class NaturalSatellite(OrbitCelestialBody):

    def __init__(self, planet=None):
        OrbitCelestialBody.__init__(self, around_the=planet)

        self.type = CelestialBodyType.NATURAL_SATELLITE

    def calculate_position(self, width, height, zoom):
        radius = km_to_pixels(width, height, self.radius, zoom)
        distance = au_to_pixels(width, height, self.orbital_radius, zoom) + get_planet_scale_radius(width, height, self.around_the, zoom) + radius * 2 + zoom
        self.x = distance * math.sin(self.angle * math.pi / 180.0)
        self.y = distance * math.cos(self.angle * math.pi / 180.0)


class Planet(OrbitCelestialBody):

    def __init__(self, star=None):
        OrbitCelestialBody.__init__(self, around_the=star)

        self.type = CelestialBodyType.PLANET
        self.natural_satellites = []

    def calculate_position(self, width, height, zoom):
        radius = km_to_pixels(width, height, self.radius, zoom)
        distance = au_to_pixels(width, height, self.orbital_radius, zoom) + get_sun_scale_radius(width, height, zoom) + radius
        self.x = distance * math.sin(self.angle * math.pi / 180.0)
        self.y = distance * math.cos(self.angle * math.pi / 180.0)


class Moon(NaturalSatellite):

    def __init__(self, earth=None):
        NaturalSatellite.__init__(self, planet=earth)

        self.type = CelestialBodyType.MOON
        self.color = Color.MOON
        self.orbit_time = OrbitTime.MOON
        self.radius = Radius.MOON
        self.orbital_radius = OrbitalRadius.MOON
        self.name = BodyName.MOON


class Fobos(NaturalSatellite):

    def __init__(self, mars=None):
        NaturalSatellite.__init__(self, planet=mars)

        self.type = CelestialBodyType.FOBOS
        self.color = Color.FOBOS
        self.orbit_time = OrbitTime.FOBOS
        self.radius = Radius.FOBOS
        self.orbital_radius = OrbitalRadius.FOBOS
        self.name = BodyName.FOBOS


class Deimos(NaturalSatellite):

    def __init__(self, mars=None):
        NaturalSatellite.__init__(self, planet=mars)

        self.type = CelestialBodyType.DEIMOS
        self.color = Color.DEIMOS
        self.orbit_time = OrbitTime.DEIMOS
        self.radius = Radius.DEIMOS
        self.orbital_radius = OrbitalRadius.DEIMOS
        self.name = BodyName.DEIMOS


class Io(NaturalSatellite):

    def __init__(self, jupiter=None):
        NaturalSatellite.__init__(self, planet=jupiter)

        self.type = CelestialBodyType.IO
        self.color = Color.IO
        self.orbit_time = OrbitTime.IO
        self.radius = Radius.IO
        self.orbital_radius = OrbitalRadius.IO
        self.name = BodyName.IO


class Europa(NaturalSatellite):

    def __init__(self, jupiter=None):
        NaturalSatellite.__init__(self, planet=jupiter)

        self.type = CelestialBodyType.EUROPA
        self.color = Color.EUROPA
        self.orbit_time = OrbitTime.EUROPA
        self.radius = Radius.EUROPA
        self.orbital_radius = OrbitalRadius.EUROPA
        self.name = BodyName.EUROPA


class Ganymede(NaturalSatellite):

    def __init__(self, jupiter=None):
        NaturalSatellite.__init__(self, planet=jupiter)

        self.type = CelestialBodyType.GANYMEDE
        self.color = Color.GANYMEDE
        self.orbit_time = OrbitTime.GANYMEDE
        self.radius = Radius.GANYMEDE
        self.orbital_radius = OrbitalRadius.GANYMEDE
        self.name = BodyName.GANYMEDE


class Callisto(NaturalSatellite):

    def __init__(self, jupiter=None):
        NaturalSatellite.__init__(self, planet=jupiter)

        self.type = CelestialBodyType.CALLISTO
        self.color = Color.CALLISTO
        self.orbit_time = OrbitTime.CALLISTO
        self.radius = Radius.CALLISTO
        self.orbital_radius = OrbitalRadius.CALLISTO
        self.name = BodyName.CALLISTO


class Mercury(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.MERCURY
        self.color = Color.MERCURY
        self.orbit_time = OrbitTime.MERCURY
        self.radius = Radius.MERCURY
        self.orbital_radius = OrbitalRadius.MERCURY
        self.name = BodyName.MERCURY


class Venus(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.VENUS
        self.color = Color.VENUS
        self.orbit_time = OrbitTime.VENUS
        self.radius = Radius.VENUS
        self.orbital_radius = OrbitalRadius.VENUS
        self.name = BodyName.VENUS


class Earth(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.EARTH
        self.color = Color.EARTH
        self.orbit_time = OrbitTime.EARTH
        self.radius = Radius.EARTH
        self.orbital_radius = OrbitalRadius.EARTH
        self.natural_satellites = [Moon(self)]
        self.name = BodyName.EARTH


class Mars(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.MARS
        self.color = Color.MARS
        self.orbit_time = OrbitTime.MARS
        self.radius = Radius.MARS
        self.orbital_radius = OrbitalRadius.MARS
        self.natural_satellites = [Fobos(self), Deimos(self)]
        self.name = BodyName.MARS


class Jupiter(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.JUPITER
        self.color = Color.JUPITER
        self.orbit_time = OrbitTime.JUPITER
        self.radius = Radius.JUPITER
        self.orbital_radius = OrbitalRadius.JUPITER
        self.natural_satellites = [Io(self), Europa(self), Ganymede(self), Callisto(self)]
        self.name = BodyName.JUPITER


class Saturn(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.SATURN
        self.color = Color.SATURN
        self.orbit_time = OrbitTime.SATURN
        self.radius = Radius.SATURN
        self.orbital_radius = OrbitalRadius.SATURN
        self.name = BodyName.SATURN


class Uranus(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.URANUS
        self.color = Color.URANUS
        self.orbit_time = OrbitTime.URANUS
        self.radius = Radius.URANUS
        self.orbital_radius = OrbitalRadius.URANUS
        self.name = BodyName.URANUS


class Neptune(Planet):

    def __init__(self, sun=None):
        Planet.__init__(self, star=sun)

        self.type = CelestialBodyType.NEPTUNE
        self.color = Color.NEPTUNE
        self.orbit_time = OrbitTime.NEPTUNE
        self.radius = Radius.NEPTUNE
        self.orbital_radius = OrbitalRadius.NEPTUNE
        self.name = BodyName.NEPTUNE


class Sun(Star):

    def __init__(self):
        Star.__init__(self)

        self.type = CelestialBodyType.SUN
        self.color = Color.SUN
        self.radius = Radius.SUN
        self.name = BodyName.SUN

        self.planets = [
            Mercury(self),
            Venus(self),
            Earth(self),
            Mars(self),
            Jupiter(self),
            Saturn(self),
            Uranus(self),
            Neptune(self)
        ]
