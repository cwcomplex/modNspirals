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

def toRGB1(rc, N):
  r = (block[rc[0], rc[1]] + 1) * N
  g = int(((block[rc[0], rc[1]] + 1) * N) / 2)
  b = int(((block[rc[0], rc[1]] + 1) * N/2))
  return (r, g, b)    


def generateImages(block, maxSquareSize, N, fileprefix):
  im = Image.new("L", (maxSquareSize, maxSquareSize))
#  im2 = Image.new("RGB", (maxSquareSize, maxSquareSize))

  step = int(255/N) + 1
  for rc in block.keys():
      im.putpixel((rc[0], rc[1]-1), (block[rc[0], rc[1]]+1) * step)

#      (r, g, b) = toRGB1(rc, N) 
#      im2.putpixel((rc[0], rc[1]-1), (r, g, b)) 


  im.save(fileprefix+"-grey.png")
  del im
#  im2.save(fileprefix+"-color.png")
#  del im2


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
 
      sq_out = "N=%d k=%d: %dx%d itercnt: %d" % (N, squareCount, root, root, jj+1)
        

      # 
      if N % 4 != 0:
        if not ((root == squareCount*N) and ((jj+1) == squareCount*squareCount*N)):
          sq_out += " FAIL (kN-by-kN, kkN)"
        else:
          sq_out += " PASS (kN-by-kN, kkN)"
      else:
        if not ((root == (squareCount*N)/2) and ((jj+1) == (squareCount*squareCount*N)/4)):
          sq_out += " FAIL (kN/2-by-kN/2, kkN/4)"
        else:
          sq_out += " PASS (kN/2-by-kN/2, kkN/4)"
 
      if prev[1] < maxy[1]:
        sq_out += " TOP"
      else:
        sq_out += " BOTTOM" 

#      generateImages(block, maxSquareSize, N, "N=%d_k=%d" % (N, squareCount))
      if squareCount == k:
        print sq_out 
        del block
        return


def main():
  genIm = False 

  if len(sys.argv) == 2 and sys.argv[1] == '-i':
    genIm = True

  for N in range(2, 65):
    for k in range(1,6):
      generateSquare(N, k)
    
if __name__ == "__main__":
  main()
