#!/usr/bin/python

import sys
from math import sqrt
import operator
from operator import mul
import matplotlib.pyplot as plt

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
  N_MAX=100
  k_MIN=1
  k_MAX=99

  print "LENGTHS"

  LINES = []
  SLOPES = []
  NSET = range(N_MIN, N_MAX+1)
  for N in NSET:
    maxx = getMaximalSquares(N)
    msk = maxx.keys()
    ldenom = 1
    for zz in msk:
      ldenom *= sqrt(maxx[zz])

    YLINE = [] 
    print "--- N=%d ---" % (N)
    for k in range(k_MIN, k_MAX+1):
      lcs = (k*N)/ldenom
      print "k=%d l=%d" % (k, lcs)
      YLINE.append(lcs)

    SLOPES.append(abs(YLINE[1] - YLINE[0]))
    LINES.append(YLINE)
  print SLOPES
  for J in LINES:
    plt.plot(J)
  plt.ylabel('length')
  plt.title('Lengths for fixed $N$, free $k$ of $Ond^k_N$')
  plt.show()

  LINES = []
  for k in range(k_MIN, k_MAX+1):
    print "--- k=%d ---" % (k) 

    YLINES = []
    for N in range(N_MIN, N_MAX+1):
      maxx = getMaximalSquares(N)
      ldenom = 1
      for zz in maxx.keys():
        ldenom *= sqrt(maxx[zz])

      lcs = (k*N)/ldenom 
      print "N=%d l=%d" %(N, lcs)
      YLINES.append(lcs)
    LINES.append(YLINES)

  for J in LINES:
    plt.plot(J)
  plt.ylabel('length')
  plt.title('Lengths for fixed $k$, free $N$ of $Ond^k_N$')
  plt.show()

  print "ITERATES"
  LINES = []
  SLOPES = []
  for N in range(N_MIN, N_MAX+1):
    maxx = getMaximalSquares(N)
    msk = maxx.keys()
    idenom = 1
    for zz in msk:
      idenom *= maxx[zz]

    YLINES = []
    print "--- N=%d ---" % (N)
    for k in range(k_MIN, k_MAX+1):
      ics = (k*k*N)/idenom
      print "k=%d i=%d" % (k, ics)

      YLINES.append(ics)
    SLOPES.append(YLINES[1]-YLINES[0])
    LINES.append(YLINES)

  for J in LINES:
    plt.plot(J)
  plt.ylabel('iterate')
  plt.title('Iterates for fixed $N$, free $k$ of $Ond^k_N$')
  plt.show()

  LINES = []
  for k in range(k_MIN, k_MAX+1):
    print "--- k=%d ---" % (k) 

    YLINES = []
    for N in range(N_MIN, N_MAX+1):
      maxx = getMaximalSquares(N)
      idenom = 1
      for zz in maxx.keys():
        idenom *= maxx[zz]
      ics = (k*k*N)/idenom 
      print "N=%d i=%d" %(N, ics)
      YLINES.append(ics)
    LINES.append(YLINES)
 
  for J in LINES:
    plt.plot(J)
  plt.ylabel('iterate')
  plt.title('Iterates for fixed $k$, free $N$ of $Ond^k_N$')
  plt.show()
          
if __name__ == "__main__":
  main()
