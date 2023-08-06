# Notwendige Imports von Sympy

from sympy.abc import x,y

from sympy.matrices import Matrix

from mfp3 import putzer, picard

# Putzer

M = Matrix([[1,-1], [1,3]])

putzer(M)

# Picard

f = y**2

x0 = 0

y0 = 1

n = 3

picard(f,x0,y0,n)