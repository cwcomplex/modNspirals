#!/usr/bin/python

def findOnd(n, prefix, numlist):
  for ni in range(n, 16+1, 1):
    print "Ond_%d achieved by:" % ni 
    for it,t in enumerate(numlist):
      if t % ni == 0:
        print "\t%s%d\t%d" % (prefix, it+2, t)

def main():
  n = 2
  nMax = 100

  trinums = []
  for ni in range(n, nMax+1, 1):
    td = (ni*(ni+1))/2
    trinums.append(td)

  print ','.join([str(x) for x in trinums])
  hexnums = []
  for ni in range(n, nMax+1, 1):
    hd = ni*(2*ni - 1)
    hexnums.append(hd)

  findOnd(n, 'T_', trinums)
  findOnd(n, 'H_', hexnums)

  for it,p in enumerate(trinums):
    for q in trinums[it+1:]:
      poss = p + q
      if poss in trinums:
        print "Found: %d + %d = %d" % (p, q, poss)

if __name__ == '__main__':
  main()
