#!/usr/bin/python

import sys
from PIL import Image
import gmpy
from math import sqrt
import operator
from operator import mul

from collections import defaultdict

def partition(seq, key):
  d = defaultdict(list)
  for x in seq:
    d[key(x)].append(x)
  return d

gend = {}

def primes(n):
  primfac = []
  d = 2
  while d*d <= n:
    while (n % d) == 0:
      primfac.append(d)  # supposing you want multiple factors repeated
      n /= d
    d += 1
  if n > 1:
    primfac.append(n)
  return primfac

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True

def getMaximalSquares(N):
  factors = primes(N)

  part = defaultdict(list)
  for f in factors:
    part[f].append(f)
  maxsquares = {}
  maxsquares[1] = 1
  pk = part.keys() 
  for k in pk:
    pcnt = len(part[k])
    if pcnt == 1:
      continue
    maxsq = 1
    for j in part[k]:
      maxsq *= j
    while pcnt > 2:
      if is_square(maxsq) == False:
        maxsq /= k
        pcnt -= 1
        continue
      break
    maxsquares[k] = maxsq
  return maxsquares

def main():
  N_MIN=2
  N_MAX=100000
  k_MIN=1
  k_MAX=5

  rootfracs = []
  sqfracs = []
  for N in range(N_MIN, N_MAX+1):
    maxx = getMaximalSquares(N)
    msk = maxx.keys()
    idenom = 1
    for zz in msk:
      idenom *= maxx[zz]
    print "%d %d" % (N, idenom)
    continue
    if idenom > 1:
      if is_square(idenom) == True:
        print "idenom is square = %d" % ( idenom)
      else:
        print "idenom is not square = %d" % ( idenom)
    else:
      print "idenom is 1"

#    rootfracs.append(ldenom)
#    sqfracs.append(idenom)      
#    print "N=%d, 1/%d, 1/%d -- %s" %(N, ldenom, idenom, str(factors))
#  print str(rootfracs)
#  print str(sqfracs)
#    print "N=%d, k=%d: root=%d sq=%d" % (N, k, ldenom, idenom)

#    for k in range(k_MIN, k_MAX+1):
#      ldenom = 1
#      idenom = 1
#      for zz in msk:
#        ldenom *= sqrt(maxsquares[zz])
#        idenom *= maxsquares[zz]
#      print "N=%d, k=%d: len=%d iterates=%d" % (N, k, (k*N)/ldenom, (k*k*N)/idenom)

       

          
if __name__ == "__main__":
  main()
