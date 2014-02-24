modNspirals
===========

The set mod N = { 0, 1, ..., N-1 }

I want to iterate over mod N in a spiral fashion over a set of lattic
points. I define a 'square' to be achieved when the length of the sides
are equal /and/ the last value placed is N-1; that is, so an iteration
ends in a corner producing a square. In spiraling, we go clockwise.


Conj. Given N >= 2 in |N and k => 1 in |N, the k-th square will have
      upper bound on size as k*N-by-k*N and upper bound on iterations
      of mod N as k*k*N.
    
Conj. For some values of N, k*N-by-k*N, k*k*N is exact.

Conj. For 4|N, the above is not exact.  

Conj. For 4|N case, we have some that follow (kN)/2-by-(kN)/2 and 
      iterations being a*k^2 where a = N/4. So, N=20,k=3 -> (30x30, 45)
      *Tested for N=4,8,20,24,28
     
Conj. The above 4|N case fails for N=16, which follows (kN)/4-by-(kN)/4
      and k^2 iterations.

Conj. All odd squares flip flop corners they end on for values of k

supported with run.log output
