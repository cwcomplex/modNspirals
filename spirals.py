#!/usr/bin/python

import sys
from PIL import Image
import gmpy
from math import sqrt
import operator
from collections import defaultdict
import time


colors = [ "\33[01;30m",
  "\33[22;31m",
  "\33[01;21m",
  "\33[22;32m",
  "\33[01;32m",
  "\33[22;34m",
  "\33[01;34m",
  "\33[22;33m",
  "\33[01;33m",
  "\33[22;36m",
  "\33[22;36m",
  "\33[22;35m",
  "\33[01;35m" ]

gend = {}

def toRGB1(rc, N):
  r = (block[rc[0], rc[1]] + 1) * N
  g = int(((block[rc[0], rc[1]] + 1) * N) / 2)
  b = int(((block[rc[0], rc[1]] + 1) * N/2))
  return (r, g, b)    

#  im2 = Image.new("RGB", (maxSquareSize, maxSquareSize))
#      (r, g, b) = toRGB1(rc, N) 
#      im2.putpixel((rc[0], rc[1]-1), (r, g, b)) 
#  im2.save(fileprefix+"-color.png")
#  del im2

def generateImages(block, maxSquareSize, N, fileprefix):
  im = Image.new("L", (maxSquareSize, maxSquareSize))
  step = int(255/N) + 1
  for rc in block.keys():
      im.putpixel((rc[0], rc[1]-1), (block[rc[0], rc[1]]+1) * step)
  im.save(fileprefix+"-grey.png")
  del im


def generateSquare(N, k):

  # Generate the (mod N) set
  modNSet = range(0, N)
  # Must prove this by combining patterns from multiple N patterns
  maxSquareSize = k*N
  maxIterationCount = k*k*N
  currentPosition = [ int(maxSquareSize / 2), int(maxSquareSize / 2) ]
  dx = 1
  dy = 0
  squareCount = 0
  block = {}
  prev = currentPosition
  for jj in range(0, maxIterationCount+5):
    for mn in modNSet:
      prev = currentPosition
      if currentPosition[1] == 0:
        print "y=0, dx=%d, dy=%d" % ( dx, dy)
      # We are moving right
      if dx == 1:
        testEntry = ( currentPosition[0], currentPosition[1] + 1 )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = 0
          dy = 1
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0] + 1, currentPosition[1]] = mn
        currentPosition[0] += 1
        continue
      # We are moving left
      elif dx == -1: 
        testEntry = ( currentPosition[0], currentPosition[1] - 1 )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = 0
          dy = -1
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0] - 1, currentPosition[1]] = mn
        currentPosition[0] -= 1
        continue
      # We are moving up
      elif dy == 1:
        testEntry = ( currentPosition[0] - 1, currentPosition[1] )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = -1
          dy = 0
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0], currentPosition[1] + 1] = mn
        currentPosition[1] += 1
        continue
      # We are moving down
      elif dy == -1:
        testEntry = ( currentPosition[0] + 1, currentPosition[1] )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = 1
          dy = 0
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0], currentPosition[1] - 1] = mn
        currentPosition[1] -= 1
        continue
      else:
        print "Bad state in spiraling! dx=%d dy=%d\n" % (dx, dy)
        sys.exit(10)

      if currentPosition[0] < 0:
        print "Bad position"
#        print block
      elif currentPosition[1] < 0:
        print "Bad position"
#        print block
    
    # Are we a square at this point?
    coords = block.keys()
    if gmpy.is_square(len(coords)):
      root = int(sqrt(len(coords)))
      squareCount += 1
      minx = min(coords, key=operator.itemgetter(0))
      maxx = max(coords, key=operator.itemgetter(0))
      miny = min(coords, key=operator.itemgetter(1))
      maxy = max(coords, key=operator.itemgetter(1))
      if (maxx[0]-minx[0]) != (maxy[1]-miny[1]):
        print "min/max dumb test failed!"
 
#      sq_out = "N=%d k=%d: %dx%d itercnt: %d" % (N, squareCount, root, root, jj+1)
        
#      if prev[1] < maxy[1]:
#        sq_out += " TOP"
#      else:
#       sq_out += " BOTTOM" 

#      generateImages(block, maxSquareSize, N, "N=%d_k=%d" % (N, squareCount))
      if squareCount == k:
#        print sq_out 
        gend[N,k] = (root, jj+1)      
        del block
        return

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

def testSpirals(args):
  (N_MIN, N_MAX, k_MIN, k_MAX) = args
  for N in range(N_MIN, N_MAX+1):
    print N
    sys.stdout.flush()
    for k in range(k_MIN, k_MAX+1):
      generateSquare(N, k)

  # Squares are generated and pushed into a dict
  for N in range(N_MIN, N_MAX+1):

    maxsquares = getMaximalSquares(N)

    for k in range(k_MIN,k_MAX+1):
      type = ""

      msk = maxsquares.keys()
      ldenom = 1
      idenom = 1
      for zz in msk:
        ldenom *= sqrt(maxsquares[zz])
        idenom *= maxsquares[zz]

      # (kN/ldenom, kkN/idenom)
      if gend[N,k][0] == (k*N)/ldenom and gend[N,k][1] == (k*k*N)/idenom:
        print "[%d, %d]: (%d, %d) ~ PASS" % (N, k, gend[N,k][0], gend[N,k][1])
      else:
        print "[%d, %d]: (%d, %d) ~ FAIL" % (N, k, gend[N,k][0], gend[N,k][1])
      
def main():

  inputs = [ (2, 50, 1, 5),
             (51, 100, 1, 5),
             (101, 150, 1, 5),
             (151, 200, 1, 5),
             (201, 250, 1, 5),
             (251, 300, 1, 5),
             (301, 350, 1, 5),
             (351, 400, 1, 5),
             (401, 450, 1, 5),
             (451, 500, 1, 5) ]

  for ii in inputs:
    t0 = time.time()
    testSpirals(ii)
    t1 = time.time()
    print "%s time: %f seconds" % (str(ii), t1-t0)

          
if __name__ == "__main__":
  main()
