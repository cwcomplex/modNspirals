#!/usr/bin/python

import sys
from PIL import Image
import gmpy
from math import sqrt
import operator

#
# Idea for using dictionary from
#   http://users.softlab.ece.ntua.gr/~ttsiod/primes.html 
#

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

def generateImages(block, maxSquareSize, N, fileprefix):

# Probably an easier way for me to put dictionary into the image .. hrm.
  im = Image.new("L", (maxSquareSize, maxSquareSize))
  im2 = Image.new("RGB", (maxSquareSize, maxSquareSize))

  for rc in block.keys():
      im.putpixel((rc[0], rc[1]-1), (block[rc[0], rc[1]]+1) * N)
 
      # weird ass map
      r = (block[rc[0], rc[1]] + 1) * N
      g = int(((block[rc[0], rc[1]] + 1) * N) / 2)
      b = int(((block[rc[0], rc[1]] + 1) * N/2))
      im2.putpixel((rc[0], rc[1]-1), (r, g, b)) 
  im.save(fileprefix+"-grey.png")
  im2.save(fileprefix+"-color.png")
  del im
  del im2




def generateSquare(N, k):
  print "Generating square for N=%d k=%d\n" % (N, k)

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

  for jj in range(0, maxIterationCount+5):
    for mn in modNSet:
      # We are moving right
      if currentPosition[1] == 0:
        print "y=0, dx=%d, dy=%d" % ( dx, dy)
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
      print "SQUARE %d: %dx%d itercnt: %d coords=%d" % (squareCount, root, root, jj+1, len(coords))
      minx = min(coords, key=operator.itemgetter(0))
      maxx = max(coords, key=operator.itemgetter(0))
      miny = min(coords, key=operator.itemgetter(1))
      maxy = max(coords, key=operator.itemgetter(1))
      if (maxx[0]-minx[0]) != (maxy[1]-miny[1]):
        print "min/max dumb test failed!"
 
      if squareCount == k:
#        print sorted(coords)
        generateImages(block, maxSquareSize, N, "N=%d_k=%d" % (N, k))
        del block
        return
#    else:
#      print "NOT SQUARE: len=%d" % len(coords)

def main():

#### I NEED square count detection
  for N in range(5, 50):
    for k in range(2, 20): 
      generateSquare(N, k)
#  generateSquare(21, 25)

if __name__ == "__main__":
  main()
