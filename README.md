# Wing with ribs

Wing 4.02

Wing 4.01 had a 8degree kink in the TE so for 4.02 I
flipped the wing over and printed it with LE down instead
of TE down as 4.01 was.

Bad news 4.01 got a kink towards the LE, so that didn't work
and I'll have to change something else, maybe increase diameter
of the cabin.

Another change was to print the dowels with 100% infil up from
50% in 4.01. Because in 4.01 the dowel broke at the wing tail
juncture.

4.02 files pretty well, but took quite a bit LESS ballast on the
nose then I thought it should. I calculated that it should be
about 3.75g but only 1.43g was needed at -60mm.
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/wing4 (4.02)
$ ./wing4.02-cg-ballast.py 
noseWeight=7.86g
tailWeight=5.44g
oacWeight=13.3g
oaWeight=13.49g
ballastOffset=-60mm from LE wing
ballast=3.78g
cgLoc=15.00mm from LE wing
cgPct=0.3%
```
It only took 1.43g of ballast
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/wing4 (4.02)
$ ./wing4.02-cg.py 
noseWeight=8.15g
tailWeight=6.77g
oacWeight=14.92g
oaWeight=14.91g
ballastOffset=-60 from LE wing
ballast=1.43g
cgLoc=27.12mm from LE wing
cgPct=54.24
```
WHY?
