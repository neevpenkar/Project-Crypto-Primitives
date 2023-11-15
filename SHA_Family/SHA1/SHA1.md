This is a (rather slow) implementation of the SHA 1 algorithm almost as given in the specification at https://www.ietf.org/rfc/rfc3174.txt .
It utilizes a custom version of the Word32 class previously created for Salsa20 wherein a little more control over the underlaying endian can be be obtained.
Note 1: There is a reference implementation attached, which I needed leter on during debugging to find a very very silly mistake over which I wated around two hours.
Note 2: **SHA 1 is broken -** The proof of which is taken from the research of CWI Amsterdam and Google Research https://shattered.io/static/shattered.pdf .
  Attached are the two different documents which cause the collisions aka two different documents which after hashing result in the same hash.
Note 3: Boy am I surprised at the speed of this implementation. Surely I could reduce the amount of 'if' statements in the code to speed up the algorithm.
