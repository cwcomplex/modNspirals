#!/usr/bin/python

import sys
from PIL import Image
import gmpy
from math import sqrt
import operator

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

def main():
  genIm = False 

  if len(sys.argv) == 2 and sys.argv[1] == '-i':
    genIm = True

  N_MIN=2
  N_MAX=500
  k_MIN=1
  k_MAX=5

  for N in range(N_MIN, N_MAX+1):
    print "----------"
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

  #    print "%d, len=%d, maxsq=%d"%(k, len(part[k]), maxsq)
      maxsquares[k] = maxsq

    for k in range(k_MIN, k_MAX+1):
      msk = maxsquares.keys()
      ldenom = 1
      idenom = 1
      for zz in msk:
        ldenom *= sqrt(maxsquares[zz])
        idenom *= maxsquares[zz]
      print "N=%d, k=%d: len=%d iterates=%d" % (N, k, (k*N)/ldenom, (k*k*N)/idenom)

       

          
if __name__ == "__main__":
  main()
