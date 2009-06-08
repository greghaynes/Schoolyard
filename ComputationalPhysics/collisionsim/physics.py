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

from PyQt4 import QtCore, QtGui

def doLinesIntersect(pointa, dva, pointb, dvb):
	pass

# Represents a vector and caches properties of the vector
class Vector:
	def __init__(self, x=0, y=0):
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
			else:
				self.directionVal = Vector(self.x() / self.magnitude(), self.y() / self.magnitude())
				self.directionSet = True
		return self.directionVal
	def resetMagnitude(self):
		self.magnitudeSet = False
		self.magnitude = 0
	def resetDirection(self):
		self.directionSet = False
		self.direction = 0

class CollidableObject:
	'Parent class for collidable objects.  You want to instanciate a subclass.'
	def __init__(self, mass, velocity):
		self.mass = mass
		self.setVelocity(velocity)
	def velocity(self):
		return self.velocityVal
	def setVelocity(self, velocity):
		self.velocityVal = velocity
	def isCollidingWith(self, otherItem):
		return False

class CollidableCircle(QtGui.QGraphicsEllipseItem, CollidableObject):
	def __init__(self, center, radius, mass, velocity=Vector(), parent=None, scene=None):
		QtGui.QGraphicsEllipseItem.__init__(self, parent, scene)
		CollidableObject.__init__(self, mass, velocity)
		rect = QtCore.QRectF(0, 0, 2*radius, 2*radius)
		self.setRect(rect)
		self.setPos(center)
		self.radius = radius
		self.mass = mass
		self.setVelocity(velocity)
	def moveStep(self):
		pass

# Contains all objects and controls simulation
class Field(QtGui.QGraphicsScene):
	def __init__(self, parent=None):
		QtGui.QGraphicsScene.__init__(self, parent)
		self.isRunningVal = False
		self.isPausedVal = False
		self.collisionFunction = self.inelasticCollision
	def isRunning(self):
		return self.isRunningVal
	def elasticCollisions(self):
		return self.collisionFunction == self.elasticCollision
	def setElasticCollitions(self, value):
		if value == True:
			self.collisionFunction = self.elasticCollision
		elif value == False:
			self.collisionFunction = self.inelasticCollision
	def start(self):
		if self.isRunning():
			return False
		else:
			self.isRunningVal = True
			self.timer = QtCore.QTimer(self)
			self.timer.setSingleShot(False)
			self.timer.setInterval(100)
			self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.timeSlice)
			self.timer.start()
			self.emit(QtCore.SIGNAL('started()'))
			return True
	def stop(self):
		if self.isRunning():
			self.timer.stop()
			self.isRunningVal = False
			self.isPausedVal = False
	def timeSlice(self):
		'Each step do collision detection with every compination of two objects'
		'If they are colliding set the items speed apropriately.'
		itemList = self.items()
		for item in itemList:
			for otherItem in itemList:
				if item.isCollidingWith(otherItem):
					self.collisionFunction(item, otherItem)
	def elasticCollision(object, otherObject):
		'Sets object to have velocity of colliding with otherObject'
		pass
	def inelasticCollision(object, otherObject):
		pass
