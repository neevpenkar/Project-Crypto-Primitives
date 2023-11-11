from Word import Word, makeBlock, makeBlockList
from Logger1 import Logger1
from datetime import datetime

r = r"E:\Projects 3\Blake2\Blake2\Version3Blake2B\Log_{index}.txt"
now = datetime.now()
logger = Logger1(r.format(index = 4)) #now.strftime("%H_%M_%S")))

R1, R2, R3, R4 = 32, 24, 16, 63
blake2b_iv = [0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
             0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
             0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
             0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179
            ]
blake2b_iv = [Word(i) for i in blake2b_iv]

def printBlock(block):
    for i in block:
        temp = str(i)
        temp.removeprefix("0x")
        print(temp, end="")
    print()
    print()
    return

SIGMA = [
        [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],
        [ 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 ],
        [ 11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4 ],
        [ 7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8 ],
        [ 9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13 ],
        [ 2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9 ],
        [ 12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11 ],
        [ 13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10 ],
        [ 6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5 ],
        [ 10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0 ],
        [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],
        [ 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 ],
        [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ], # Added
        [ 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 ], # Added
        ]

def G(v:list, a, b, c, d, x, y, log=True):
    v = v.copy()
    w = 64 # Specification
    R1, R2, R3, R4 = 32, 24, 16, 63

    v[a] = (v[a] + v[b] + x) # M1
    v[d] = (v[d] ^ v[a]).rotateRight(R1) # M2
    v[c] = (v[c] + v[d])     % 2**w # M3
    v[b] = (v[b] ^ v[c]).rotateRight(R2) # M4
    v[a] = (v[a] + v[b] + y) % 2**w # M5
    v[d] = (v[d] ^ v[a]).rotateRight(R3)
    v[c] = (v[c] + v[d])     % 2**w
    v[b] = (v[b] ^ v[c]).rotateRight(R4) # M8

    return v

def F(h, m, t, f):
    logger.log(h, "h at the start of F")
    #logger.log(m, "m at the start of F")

    v = h.copy()
    for i in blake2b_iv:
        v.append(i.copy())
    #v.extend(blake2b_iv.copy())

    logger.log(v, "v after init")
    v[12] = v[12] ^ Word(t % (2**64))
    v[13] = v[13] ^ Word(t >> 64)
    #logger.log(v, "v after length xor before invert")
    if f == True:
        v[14].invert()
    logger.log(v, "v after length xor after invert")
    #raise RuntimeError("Paused by me")

    for i in range(12):
        #logger.log(i, "Round i", 0)
        s = SIGMA[i % 10]
        v = G( v, 0, 4,  8, 12, m[s[ 0]], m[s[ 1]] )
        v = G( v, 1, 5,  9, 13, m[s[ 2]], m[s[ 3]] )
        v = G( v, 2, 6, 10, 14, m[s[ 4]], m[s[ 5]] )
        v = G( v, 3, 7, 11, 15, m[s[ 6]], m[s[ 7]] )

        v = G( v, 0, 5, 10, 15, m[s[ 8]], m[s[ 9]] )
        v = G( v, 1, 6, 11, 12, m[s[10]], m[s[11]] )
        v = G( v, 2, 7,  8, 13, m[s[12]], m[s[13]] )
        v = G( v, 3, 4,  9, 14, m[s[14]], m[s[15]] )

    for i in range(8):
        h[i] = h[i] ^ v[i] ^ v[i+8]
    return h

def Blake2NoKey(ll, block, hashsize=64):

    h = blake2b_iv.copy()
    h[0] = h[0] ^ Word(0x01010000^hashsize)

    h = F(h, block, ll, True)

    temp = bytearray()
    for i in h:
        temp.extend(i.toByteArray())
    return temp[0:hashsize]

def Blake2_No_Key(ll, blocks, hashsize=64):
    for b in blocks:
        for i in b:
            print(i)
        print("----------------------")

    h = blake2b_iv.copy()
    h[0] = h[0] ^ Word(0x01010000^hashsize)
    dd = len(blocks)
    
    for i in range(0, dd-1):
        h = F(h, blocks[i], (i+1)*128, False) # bb = 128

    h = F(h, blocks[dd-1], ll, True)

    temp = bytearray()
    for i in h:
        temp.extend(i.toByteArray())
    return temp[0:hashsize]


for i in range(12):
    s = SIGMA[i % 10]

    print("x = " + str(s[ 0]) + ",  y = " + str(s[ 1]))
    print("x = " + str(s[ 2]) + ",  y = " + str(s[ 3]))
    print("x = " + str(s[ 4]) + ",  y = " + str(s[ 5]))
    print("x = " + str(s[ 6]) + ",  y = " + str(s[ 7]))

    print("x = " + str(s[ 8]) + ",  y = " + str(s[ 9]))
    print("x = " + str(s[10]) + ",  y = " + str(s[11]))
    print("x = " + str(s[12]) + ",  y = " + str(s[13]))
    print("x = " + str(s[14]) + ",  y = " + str(s[15]))

    print("--------------------------")


# Problem with extend -> two same values which were extended 
# (one was with .copy()) were being tangled together. To solve, 
# appended individual items with .copy()