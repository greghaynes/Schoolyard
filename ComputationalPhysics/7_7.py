# -*- coding: utf-8 -*-
import random

count = 1000
hits = 0
for i in xrange(count):
	x = random.random()
	y = random.random()
	z = random.random()
	dist = (x**2 + y**2 + z**2)**.5
	if dist <= 1:
		hits += 1
print str(hits/float(count) * 8)
