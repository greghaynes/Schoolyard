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
from physics import Field, CollidableCircle, Vector

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
		# window settings
		self.resize(600, 600)
		self.setWindowTitle('Collision Simulator')
		view = QtGui.QGraphicsView(self.field, self)
		self.setCentralWidget(view)
		view.adjustSize()
		# actions
		self.startSimAction = QtGui.QAction('Start', self)
		self.connect(self.startSimAction, QtCore.SIGNAL('triggered()'), self.field.start)
		self.stopSimAction = QtGui.QAction('Stop', self)
		self.stopSimAction.setEnabled(False)
		self.connect(self.stopSimAction, QtCore.SIGNAL('triggered()'), self.field.stop)
		self.addObjectAction = QtGui.QAction('Add Object', self)
		self.connect(self.addObjectAction, QtCore.SIGNAL('triggered()'), self.createObject)
		# menus
		self.fileMenu = self.menuBar().addMenu('File')
		self.fileMenu.addAction(self.startSimAction)
		self.fileMenu.addAction(self.stopSimAction)
		self.editMenu = self.menuBar().addMenu('Edit')
		self.editMenu.addAction(self.addObjectAction)
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
