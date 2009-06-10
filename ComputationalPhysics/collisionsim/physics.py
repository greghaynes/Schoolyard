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
		self.colliders = {}
	def velocity(self):
		return self.velocityVal
	def setVelocity(self, velocity):
		self.velocityVal = velocity
	def isCollidingWith(self, otherItem):
		return False
	def step(self, stepSize):
		vel = self.velocity()
		dx = vel.x() * stepSize
		dy = vel.y() * stepSize
		# print 'moving [' + str(dx) + ', ' + str(dy) + ']'
		if dx != 0 or dy != 0:
			self.moveBy(dx, dy)
	def momentum(self):
		return self.velocity().magnitude() * self.mass

class CollidableCircle(QtGui.QGraphicsEllipseItem, CollidableObject):
	def __init__(self, center, radius, mass, velocity, parent=None, scene=None):
		QtGui.QGraphicsEllipseItem.__init__(self, parent, scene)
		CollidableObject.__init__(self, mass, velocity)
		rect = QtCore.QRectF(0, 0, 2*radius, 2*radius)
		self.setRect(rect)
		self.setPos(center)
		self.radius = radius
		self.mass = mass
		self.setVelocity(velocity)
	def isCollidingWith(self, otherCircle):
		pos = self.pos()
		otherpos = otherCircle.pos()
		# Well leave as sqares because sqroot's are slow
		distsq = (pos.x() - otherpos.x())**2 + (pos.y() + otherpos.y())**2
		radsumsq = self.radius**2 + otherCircle.radius**2
		# print str(distsq) + ', ' + str(radsumsq)
		if distsq <= radsumsq:
			return True
		else:
			return False

# Contains all objects and controls simulation
class Field(QtGui.QGraphicsScene):
	def __init__(self, parent=None):
		QtGui.QGraphicsScene.__init__(self, parent)
		self.isRunningVal = False
		self.isPausedVal = False
		self.collisionFunction = self.inelasticCollision
		self.stepSize = .08
	def isRunning(self):
		return self.isRunningVal
	def elasticCollisions(self):
		return self.collisionFunction == self.elasticCollision
	def setElasticCollisions(self, value):
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
			self.timer.setInterval(self.stepSize**-1)
			self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.timeSlice)
			self.timer.start()
			self.emit(QtCore.SIGNAL('started()'))
			return True
	def stop(self):
		if self.isRunning():
			self.timer.stop()
			self.isRunningVal = False
			self.isPausedVal = False
			self.emit(QtCore.SIGNAL('stopped()'))
	def timeSlice(self):
		'Each step do collision detection with every combination of two objects'
		'If they are colliding set the items speed apropriately.'
		itemList = self.items()
		i = 0
		for item in itemList:
			for otherItem in itemList[i:]:
				if item != otherItem and item.isCollidingWith(otherItem):
					# print 'Collision!'
					self.collisionFunction(item, otherItem)
			i += 1
		for item in itemList:
			item.step(self.stepSize)
	def elasticCollision(self, object, otherObject):
		'Sets object to have velocity of colliding with otherObject'
		print 'collision'
		masssum = object.mass + otherObject.mass
		objmassdr = float(object.mass - otherObject.mass)/(masssum)
		obj2mdr = (2.*otherObject.mass)/(masssum)
		oomassdr = float(otherObject.mass - object.mass)/(masssum)
		oo2mdr = (2.*object.mass)/(masssum)
		# Store temp velocities because we will need them after we change their values
		ovelx = object.velocity().x()
		ovely = object.velocity().y()
		oovelx = otherObject.velocity().x()
		oovely = otherObject.velocity().y()
		object.velocity().setX((objmassdr * ovelx) + (obj2mdr*oovelx))
		object.velocity().setY((objmassdr * ovely) + (obj2mdr*oovely))
		otherObject.velocity().setX((oomassdr * oovelx) + (oo2mdr*ovelx))
		otherObject.velocity().setY((oomassdr * oovely) + (oo2mdr*ovely))
	def inelasticCollision(self, object, otherObject):
		if object.colliders.has_key(otherObject):
			return
		print 'Collision!'
		xmag = object.velocity().x() + otherObject.velocity().x()
		ymag = object.velocity().y() + otherObject.velocity().y()
		for update in object.colliders:
			if not otherObject.colliders.has_key(update):
				otherObject.colliders[update] = True
		for update in otherObject.colliders:
			if not object.colliders.has_key(update):
				object.colliders[update] = True
		object.colliders[otherObject] = True
		otherObject.colliders[object] = True
		combmass = object.mass
		for update in object.colliders:
			combmass += update.mass
		resVel = Vector(float(xmag) / combmass, float(ymag) / combmass)
		object.setVelocity(resVel)
		for update in object.colliders:
			update.setVelocity(resVel)