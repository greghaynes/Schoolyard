# -*- coding: utf-8 -*-

# PyCollisionSim  - A graphical collision simulator wirtten in python
# Copyright (C) 2009 Gregory Haynes <greg@greghaynes.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from PyQt4 import QtGui

def doLinesIntersect(pointa, dva, pointb, dvb):
	pass

# Represents a vector and caches properties of the vector
class Vector:
	def __init__(x=0, y=0):
		self.xVal = x
		self.yVal = y
		self.resetMagnitude()
		self.resetDirection()
	def x(self):
		return self.xVal
	def y(self):
		return self.yVal
	def setX(self, x):
		self.resetMagnitude()
		self.resetDirection()
		self.xVal = x
	def setY(self, y):
		self.resetMagnitude()
		self.resetDirection()
		self.yVal = y
	def magnitude(self):
		if not self.magnitudeSet:
			self.magnitudeVal = (self.x()**2. + self.y()**2.)**.5
			self.magnitudeSet = True
		return self.magnitudeVal
	def direction(self):
		if not self.directionSet:
			if self.magnitude() == 0:
				return False
			else
				self.directionVal = Vector(self.x() / self.magnitude(), self.y() / self.magnitude())
				self.directionSet = True
		return self.directionVal
	def resetMagnitude(self):
		self.magnitudeSet = False
		self.magnitude = 0
	def resetDirection(self):
		self.directionSet = False
		self.direction = 0

class CollidableObject(QtGui.QGraphicsItem):
	def __init__(self, velocity=Vector(), parent=None, scene=None):
		QtGui.QGraphicsItem.__init__(self, parent, scene)
		self.velocity = velocity
	def moveStep(self):
		pass
	def collidesWith(self, otherObject):
		pass

# Contains all objects and controls simulation
class Field(QtGui.QGraphicsScene):
	def __init__(self, parent=None):
		QtGui.QGraphicsScene.__init__(self, parent)
	def timeSlice(self):
		pass
