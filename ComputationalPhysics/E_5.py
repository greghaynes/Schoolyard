import random
import math

count = 1000 # number of points to use for Monte-Carlo and Simpsons

hitcount = 0
for i in xrange(count):
	x = random.random()
	y = random.random()
	if (x**2 + y**2)**.5 <= 1:
		hitcount += 1

sum = 0
dx = 1. / count
x = 0
for i in xrange(count):
	val = (1 - x**2)**.5
	if i == 0 or i == (count-1):
		sum += val
	elif i % 2 == 0:
		sum += 4 *val
	else:
		sum += 2 * val
	x += dx
sum *= (dx / 3)
sum *= 4

hitrate = hitcount / float(count)
print 'Using circle of radius=1'
print 'Monte-Carlo'
print '\tHits: ' + str(hitcount) + '/' + str(count) + ' = ' + str(hitrate) + '%'
print '\tEstimated area: ' + str(hitrate * 4)
print 'Simpsons Integration'
print '\tEstimated area: ' + str(sum)

