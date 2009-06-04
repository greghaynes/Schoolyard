# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import math

angstep = .01

func = lambda x, cosxmax: 1. / ((math.cos(x) - cosxmax)**.5)

def integrate(angmax):
	ang = angstep / 2.
	sum = 0
	cxm = math.cos(angmax)
	while ang < angmax:
		sum += func(ang, cxm)
		ang += angstep
	return sum

a = .01
da = .01
values = [[], []]
while a < math.pi:
	values[0].append(a)
	values[1].append(integrate(a))
	a += da

plt.plot(values[0], values[1])
plt.show()