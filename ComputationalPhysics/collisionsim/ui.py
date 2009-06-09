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

import qrc
from PyQt4 import QtCore, QtGui
from physics import Field, CollidableCircle, Vector

class AboutData(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.setWindowTitle('About PyCollisionSim')
		label = QtGui.QLabel('<h2>PyCollisionSim</h2>\n' +
			'Created by Gregory Haynes.<br>' +
			'Copyright 2009 Gregory Haynes.<br>' +
			'Licensed under the GNU Public License (v2).')
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(label)

# Add Object dialog
class CreateObjectWidget(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.setWindowTitle('Create Object')
		self.xEdit = QtGui.QLineEdit()
		self.yEdit = QtGui.QLineEdit()
		self.xVelEdit = QtGui.QLineEdit()
		self.yVelEdit = QtGui.QLineEdit()
		self.radiusEdit = QtGui.QLineEdit()
		self.massEdit = QtGui.QLineEdit()
		locationLabel = QtGui.QLabel('Location')
		xLabel = QtGui.QLabel('X:')
		yLabel = QtGui.QLabel('Y:')
		xVelLabel = QtGui.QLabel('X:')
		yVelLabel = QtGui.QLabel('Y:')
		velocityLabel = QtGui.QLabel('Velocity')
		radiusLabel = QtGui.QLabel('Radius:')
		massLabel = QtGui.QLabel('Mass:')
		layout = QtGui.QGridLayout()
		layout.addWidget(locationLabel, 0, 0)
		layout.addWidget(xLabel, 1, 0)
		layout.addWidget(self.xEdit, 1, 1)
		layout.addWidget(yLabel, 2, 0)
		layout.addWidget(self.yEdit, 2, 1)
		layout.addWidget(velocityLabel, 3, 0)
		layout.addWidget(xVelLabel, 4, 0)
		layout.addWidget(self.xVelEdit, 4, 1)
		layout.addWidget(yVelLabel, 5, 0)
		layout.addWidget(self.yVelEdit, 5, 1)
		layout.addWidget(radiusLabel, 6, 0)
		layout.addWidget(self.radiusEdit, 6, 1)
		layout.addWidget(massLabel, 7, 0)
		layout.addWidget(self.massEdit, 7, 1)
		self.okButton = QtGui.QPushButton('Ok')
		self.connect(self.okButton, QtCore.SIGNAL('clicked(bool)'), self.accept)
		self.cancelButton = QtGui.QPushButton('Cancel')
		self.connect(self.cancelButton, QtCore.SIGNAL('clicked(bool)'), self.close)
		buttonLayout = QtGui.QHBoxLayout()
		buttonLayout.addWidget(self.cancelButton)
		buttonLayout.addWidget(self.okButton)
		layout.addLayout(buttonLayout, 8, 1)
		self.setLayout(layout)

# CollisionSimulator window
class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.field = Field(self)
		self.connect(self.field, QtCore.SIGNAL('started()'), self.simulationStarted)
		self.connect(self.field, QtCore.SIGNAL('stopped()'), self.simulationEnded)
		# window settings
		self.resize(600, 600)
		self.setWindowTitle('Collision Simulator')
		view = QtGui.QGraphicsView(self.field, self)
		self.setCentralWidget(view)
		view.adjustSize()
		# actions
		self.startSimAction = QtGui.QAction('Start', self)
		self.startSimAction.setIcon(QtGui.QIcon(':/icons/start.png'))
		self.connect(self.startSimAction, QtCore.SIGNAL('triggered()'), self.field.start)
		self.stopSimAction = QtGui.QAction('Stop', self)
		self.stopSimAction.setEnabled(False)
		self.stopSimAction.setIcon(QtGui.QIcon(':/icons/stop.png'))
		self.connect(self.stopSimAction, QtCore.SIGNAL('triggered()'), self.field.stop)
		self.addObjectAction = QtGui.QAction('Add Object', self)
		self.addObjectAction.setIcon(QtGui.QIcon(':/icons/add.png'))
		self.connect(self.addObjectAction, QtCore.SIGNAL('triggered()'), self.createObject)
		self.clearAction = QtGui.QAction('Clear Objects', self)
		self.clearAction.setIcon(QtGui.QIcon(':/icons/clear.png'))
		self.connect(self.clearAction, QtCore.SIGNAL('triggered()'), self.field.clear)
		self.chickenExampleAction = QtGui.QAction('Chicken', self)
		self.connect(self.chickenExampleAction, QtCore.SIGNAL('triggered()'), self.chickenExample)
		self.ricochet3ExampleAction = QtGui.QAction('3 object ricochet', self)
		self.connect(self.ricochet3ExampleAction, QtCore.SIGNAL('triggered()'), self.ricochet3)
		self.exitAction = QtGui.QAction('Exit', self)
		self.exitAction.setIcon(QtGui.QIcon(':/icons/exit.png'))
		self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		self.aboutAction = QtGui.QAction('About', self)
		self.connect(self.aboutAction, QtCore.SIGNAL('triggered()'), self.aboutData)
		# menus
		self.fileMenu = self.menuBar().addMenu('File')
		self.fileMenu.addAction(self.startSimAction)
		self.fileMenu.addAction(self.stopSimAction)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAction)
		self.editMenu = self.menuBar().addMenu('Edit')
		self.editMenu.addAction(self.addObjectAction)
		self.editMenu.addAction(self.clearAction)
		self.exampleMenu = self.menuBar().addMenu('Examples')
		self.exampleMenu.addAction(self.chickenExampleAction)
		self.exampleMenu.addAction(self.ricochet3ExampleAction)
		self.helpMenu = self.menuBar().addMenu('Help')
		self.helpMenu.addAction(self.aboutAction)
		# toolbar
		self.toolbar = self.addToolBar('Control')
		self.toolbar.addAction(self.startSimAction)
		self.toolbar.addAction(self.stopSimAction)
		self.toolbar = self.addToolBar('Edit')
		self.toolbar.addAction(self.addObjectAction)
		self.toolbar.addAction(self.clearAction)
	def simulationStarted(self):
		self.startSimAction.setEnabled(False)
		self.stopSimAction.setEnabled(True)
	def simulationEnded(self):
		self.startSimAction.setEnabled(True)
		self.stopSimAction.setEnabled(False)
	def createObject(self):
		widget = CreateObjectWidget(self)
		if widget.exec_():
			if widget.xEdit.text().isEmpty() or widget.yEdit.text().isEmpty() or widget.yVelEdit.text().isEmpty() or widget.xVelEdit.text().isEmpty():
				return False
			else:
				loc = QtCore.QPointF(float(widget.xEdit.text()), float(widget.yEdit.text()))
				vel = Vector(float(widget.xVelEdit.text()), float(widget.yVelEdit.text()))
				newObj = CollidableCircle(loc, float(widget.radiusEdit.text()), float(widget.massEdit.text()), vel, None, self.field)
				# debugObj(newObj)
	def aboutData(self):
		widget = AboutData(self)
		widget.exec_()
	def chickenExample(self):
		obj = CollidableCircle(QtCore.QPointF(-100, 0), 5, 5, Vector(10, 0), None, self.field)
		obj2 = CollidableCircle(QtCore.QPointF(100, 0), 5, 5, Vector(-10, 0), None, self.field)
	def ricochet3(self):
		obj1 = CollidableCircle(QtCore.QPointF(-100, 0), 5, 5, Vector(0, 0), None, self.field)
		obj2 = CollidableCircle(QtCore.QPointF(0, 0), 5, 5, Vector(3, 0), None, self.field)
		obj3 = CollidableCircle(QtCore.QPointF(100, 0), 5, 5, Vector(-20, 0), None, self.field)

def debugObj(obj):
	vel = obj.velocity()
	print 'vel: [' + str(vel.x()) + ', ' + str(vel.y()) + ']'