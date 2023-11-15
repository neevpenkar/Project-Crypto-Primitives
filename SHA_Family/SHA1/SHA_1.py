from Block import *
from Word32 import *
from Word32 import Word32 as Word

'''
f(t;B,C,D) = (B AND C) OR ((NOT B) AND D)         ( 0 <= t <= 19)

f(t;B,C,D) = B XOR C XOR D                        (20 <= t <= 39)

f(t;B,C,D) = (B AND C) OR (B AND D) OR (C AND D)  (40 <= t <= 59)

f(t;B,C,D) = B XOR C XOR D                        (60 <= t <= 79).

'''


def f(t, B: Word, C: Word ,D: Word):
    if 0 <= t <= 19:
        return (B & C) | ((~B) & D)
    elif 20 <= t <= 39:
        return B ^ C ^ D
    elif 40 <= t <= 59:
        return (B & C) | (B & D) | (C & D)
    elif 60 <= t <= 79:
        return B ^ C ^ D

def K(t):
    if 0 <= t <= 19:
        return Word(0x5A827999)
    elif 20 <= t <= 39:
        return Word(0x6ED9EBA1)
    elif 40 <= t <= 59:
        return Word(0x8F1BBCDC)
    elif 60 <= t <= 79:
        return Word(0xCA62C1D6)

def SHA_1_Compression(block: Block):
    
    H0 = Word(0x67452301)
    H1 = Word(0xEFCDAB89)
    H2 = Word(0x98BADCFE)
    H3 = Word(0x10325476)
    H4 = Word(0xC3D2E1F0)

    W = [Word(0)]*80
    for i in range(0, 16):
        W[i] = block[i].copy()

    for t in range(16, 79+1):
        w = W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]
        W[t] = w.rotateLeft(1)

    A, B, C, D, E = H0.copy(),H1.copy(),H2.copy(),H3.copy(),H4.copy()
    for i in range(0, 79+1):
        tmp = A.rotateLeft(5) + f(i,B,C,D) + E + W[i] + K(i)
        E = D
        D = C
        C = B.rotateLeft(30)
        B = A
        A = tmp

    H0 = H0 + A
    H1 = H1 + B
    H2 = H2 + C
    H3 = H3 + D
    H4 = H4 + E

    t = [H0,H1,H2,H3,H4]
    return list2byterray(t)

tv = "abc".encode("utf-8")


out = PadAndBlockList(tv)
out[0].printBlock()
temp = SHA_1_Compression(out[0])

print(hex(int.from_bytes(temp, endian)))