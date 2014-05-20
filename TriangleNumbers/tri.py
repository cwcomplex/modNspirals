#!/usr/bin/python

import sys
from PIL import Image
#import gmpy
from math import sqrt
import operator
from collections import defaultdict
import time

def generateImages(block, maxSquareSize, N, fileprefix):
  im = Image.new("L", (maxSquareSize, maxSquareSize))
  step = int(255/N) + 1
  ks = block.keys()
  print ks
  for rc in block.keys():
      print rc
      im.putpixel((rc[0], rc[1]-1), (block[rc[0], rc[1]]) * step)
  im.save(fileprefix+"-grey.png")
  del im


def generateTriangle(N, k):
  modNset = range(0, N);
# Need to think this through
  maxBlock = k*k*N
  maxIteration = k*k*k*N

  currentPosition = [ 0, maxBlock ]
  block = {}
  dx = 0
  dy = 0

  tricount = 0
  for jj in range(0, maxIteration+5):
    for mn in modNset:


      prev = currentPosition
      block[prev[0], prev[1]] = mn

      if prev[0] == 0 and prev[1] == maxBlock:  # At start
        currentPosition[0] += 1 
        currentPosition[1] += 0 
        dx = -1
        dy = -1
        continue

# we are moving up-left
      if dx == -1 and dy == -1:
        if prev[0] == 0:
          print "You have reached x-min with mn=%d"%(mn)
          if mn == (N-1):
              tricount += 1
              if tricount == k:
                return block
          currentPosition[1] += -1
          dx = dy = 1
        else:
          currentPosition[0] += dx
          currentPosition[1] += dy
      elif dx == 1 and dy == 1:
        if prev[1] == maxBlock:
          print "You have reached y-max with mn=%d" % (mn)
          if mn == (N-1):
              tricount += 1
              if tricount == k:
                return block
          currentPosition[1] += -1
          currentPosition[0] += 1
          dx = dy = -1
        else:
          currentPosition[0] += dx
          currentPosition[1] += dy

def main():
  blok = generateTriangle(5, 6) 
  generateImages(blok, 5*6*6, 5, 'yo')
  print blok


if __name__ == '__main__':
  main()
