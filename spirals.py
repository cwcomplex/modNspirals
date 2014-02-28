#!/usr/bin/python

import sys
from PIL import Image
import gmpy
from math import sqrt
import operator


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

def main():
  genIm = False 

  if len(sys.argv) == 2 and sys.argv[1] == '-i':
    genIm = True

  N_MIN=301
  N_MAX=350
  k_MIN=1
  k_MAX=5
  for N in range(N_MIN, N_MAX+1):
    print N
    sys.stdout.flush()
    for k in range(k_MIN, k_MAX+1):
      generateSquare(N, k)

  for N in range(N_MIN, N_MAX+1):
    pf = primes(N)
    for k in range(k_MIN,k_MAX+1):
      type = ""

      # (kN, kkN) case
      if gend[N,k][0] == k*N and gend[N,k][1] == k*k*N:
        type = "(kN, kkN)" 

      # (\sqrt{N}k, kk) case
      elif gend[N,k][0] == k*sqrt(N) and gend[N,k][1] == k*k:
        type = "(sqrt(N)k, kk)"

      # to be revised case... 
      elif gend[N,k][0] == 0.5*k*N and gend[N,k][1] == 0.25*k*k*N:
        type = "((1/2)kN, (1/4)kkN)"
      else:
        if gend[N,k][0] < k*N and gend[N,k][1] < k*k*N:
          type = "No Match bounded"
        else:
          type = "No Match broke bounds"

      print "[%d, %d]: (%d, %d) ~ %s ~ %s" % (N, k, gend[N,k][0], gend[N,k][1], type, str(pf))
      
          
if __name__ == "__main__":
  main()
