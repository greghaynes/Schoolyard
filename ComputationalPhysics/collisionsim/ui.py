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
from physics import Field, CollidableCircle

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
		# menus
		self.fileMenu = self.menuBar().addMenu('File')
		self.fileMenu.addAction(self.startSimAction)
		self.fileMenu.addAction(self.stopSimAction)
	def simulationStarted(self):
		self.startSimAction.setEnabled(False)
		self.stopSimAction.setEnabled(True)
	def simulationEnded(self):
		self.startSimAction.setEnabled(True)
		self.stopSimAction.setEnabled(False)
