import numpy
import matplotlib.pyplot as plt
import random

distances = []

def magnitude(vector3d):
	return (vector3d[0]**2 + vector3d[1]**2 + vector3d[2]**2)**.5

def runWalker(steps):
	location = [0, 0, 0]
	displacements = []
	for i in xrange(steps):
		direction = int(6*random.random())
		if direction == 0:
			location[0] += 1
		elif direction == 1:
			location[0] -= 1
		elif direction == 2:
			location[1] += 1
		elif direction == 3:
			location[1] -= 1
		elif direction == 4:
			location[2] += 1
		else:
			location[2] -= 1
		displacements.append(magnitude(location))
	return location, displacements

distances = []
for i in xrange(1000):
	distances.append(0);
for i in xrange(1000):
	location, displacements = runWalker(1000)
	for i in xrange(len(displacements)):
		distances[i] += displacements[i]**2

for i in xrange(len(distances)):
	distances[i] = distances[i] / 1000

slope,intercept = numpy.polyfit(xrange(1000),distances,1)
plt.title('Random 3-D walker: distance vs time, red=fitted line slope='+str(slope))
plt.xlabel('Number of steps')
plt.ylabel('Distance from origin squared')
plt.plot(distances,'x-')
plt.plot(slope*xrange(1000)+intercept,'r-')
plt.show()