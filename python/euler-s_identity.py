#! /usr/bin/env python3

import cmath

r = cmath.exp(1j * cmath.pi) + 1
print("%.3f+%.3fi" % (r.real, r.imag))
