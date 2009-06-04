import random
import math

count = 10000 # number of points to use

print 'Calculating area of a sphere with radius=1 using ' + str(count) + ' random points'
hits = 0
for i in xrange(count):
	x = random.random()
	y = random.random()
	z = random.random()
	dist = (x**2 + y**2 + z**2)**.5
	if dist <= 1:
		hits += 1
hitrate = hits/float(count)
print 'Percent inside sphere: ' + str(hits) + '/' + str(count) + ' = ' + str(hitrate) + '%'
print 'Estimated area: ' + str(hitrate * 8)
print 'Actial area: ' + str((4/3.)*math.pi)
