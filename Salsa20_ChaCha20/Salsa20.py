from Word32 import *
from Crypto.Random import get_random_bytes
from math import floor
Word = Word32

def quarterround(y0, y1, y2, y3):
    z1 = y1 ^ (y0 + y3).rotateLeft(7)
    z2 = y2 ^ (z1 + y0).rotateLeft(9)
    z3 = y3 ^ (z2 + z1).rotateLeft(13)
    z0 = y0 ^ (z3 + z2).rotateLeft(18)

    return z0, z1, z2, z3

def rowround(y):
    if len(y) != 16:
        raise ValueError("State size must be 16 words (512 bits)")

    z = [0] * len(y)
    z[0], z[1], z[2], z[3] = quarterround(y[0], y[1], y[2], y[3])
    z[5], z[6], z[7], z[4] = quarterround(y[5], y[6], y[7], y[4])
    z[10], z[11], z[8], z[9] = quarterround(y[10], y[11], y[8], y[9])
    z[15], z[12], z[13], z[14] = quarterround(y[15], y[12], y[13], y[14])

    return z

def columnround(x):
    if len(x) != 16:
        raise ValueError("State size must be 16 words (512 bits)")

    y = [0] * len(x)
    y[0], y[4], y[8], y[12] = quarterround(x[0], x[4], x[8], x[12])
    y[5], y[9], y[13], y[1]= quarterround(x[5], x[9], x[13], x[1])
    y[10] , y[14], y[2], y[6]= quarterround(x[10], x[14], x[2], x[6 ])
    y[15] , y[3], y[7], y[11] = quarterround(x[15], x[3], x[7], x[11])
    return y

def doubleround(x):
    return rowround(columnround(x))

def Salsa20HashFunction(x: bytearray):
    if len(x) != 64:
        raise ValueError("x is not 64 bytes")

    v = makeWordListFromBytes(x, 4, 16)
    z = doubleround(v)

    for i in range(10-1):
        z = doubleround(z)

    toret = [0]*16
    for i in range(16):
        toret[i] = (z[i] + v[i])

    return list2byterray(toret)

def Salsa20ExpansionFunction(key: bytearray, nonce: bytearray, counter: Word32, counter2=None):
    # Note that counter is two words long. For simplicity, 
    # only one word will be used

    constant = b"expand 32-byte k"
    key0, key1 = key[0:16], key[16:32]
    n = nonce
    if counter2 is None:
        n.extend(bytearray([0]*4))
    else:
        n.extend(counter2.toByteArray())
    n.extend(counter.toByteArray())

    x = bytearray()
    x.extend(constant[0:4])
    x.extend(key0)
    x.extend(constant[4:8])
    x.extend(n)
    x.extend(constant[8:12])
    x.extend(key1)
    x.extend(constant[12:16])

    return Salsa20HashFunction(x.copy())

def Salsa20EncryptionFunction(key: bytearray, data: bytearray):
    nonce = get_random_bytes(4*2)
    keystream = bytearray()
    counter = Word(1)
    statesize = 64

    for i in range(len(data) // statesize):
        temp = Salsa20ExpansionFunction(key, nonce, counter)
        keystream.extend(temp)
        counter = counter + Word(1)

    if len(data) % statesize != 0:
        temp = Salsa20ExpansionFunction(key, nonce, counter)
        keystream.extend(temp)

    return XOR(data, keystream[0:len(data)])


def finalKeystreamTest():
    #a = [101,120,112, 97, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    #    13, 14, 15, 16,110,100, 32, 51,101,102,103,104,105,106,107,108,
    #    109,110,111,112,113,114,115,116, 50, 45, 98,121,201,202,203,204,
    #    205,206,207,208,209,210,211,212,213,214,215,216,116,101, 32,107]

    key = bytearray([i for i in range(1, 17)])
    key.extend(bytearray([i for i in range(201, 217)]))
    #n = bytearray([i for i in range(101, 117)])
    nonce = bytearray([i for i in range(101, 109)])
    counter0 = Word([i for i in range(109, 109+4)])
    counter1 = Word([i for i in range(109 + 4, 109+8)])
    b = Salsa20ExpansionFunction(key, nonce, counter1, counter0)

    for i in b:
        print(i, end=", ")
    print()

    return

def expansionFuncTest():
    k = [i for i in range(1, 17)]
    k.extend([i for i in range(201, 217)])
    n =  [i for i in range(101, 117)]

    test = [69, 37, 68, 39, 41, 15,107,193,255,139,122, 6,170,233,217, 98,
            89,144,182,106, 21, 51,200, 65,239, 49,222, 34,215,114, 40,126,
            104,197, 7,225,197,153, 31, 2,102, 78, 76,176, 84,245,246,184,
            177,160,133,130, 6, 72,149,119,192,195,132,236,234,103,246, 74  ]

    test = bytearray(test)

    b = Salsa20ExpansionFunction(k, n)
    print(b == test)

def hashfunctest():
    datain = [211,159, 13,115, 76, 55, 82,183, 3,117,222, 37,191,187,234,136,
    49,237,179, 48, 1,106,178,219,175,199,166, 48, 86, 16,179,207,
    31,240, 32, 63, 15, 83, 93,161,116,147, 48,113,238, 55,204, 36,
    79,201,235, 79, 3, 81,156, 47,203, 26,244,243, 88,118,104, 54]

    test = [109, 42,178,168,156,240,248,238,168,196,190,203, 26,110,170,154,
    29, 29,150, 26,150, 30,235,249,190,163,251, 48, 69,144, 51, 57,
    118, 40,152,157,180, 57, 27, 94,107, 42,236, 35, 27,111,114,114,
    219,236,232,135,111,155,110, 18, 24,232, 95,158,179, 19, 48,202]
    test = bytearray(test)
    datain = bytearray(datain)

    dout = Salsa20HashFunction(datain)

    cont = []
    for i in range(64):
        cont.append(dout[i] == test[i])

    print(all(cont))
    return

def row_column_roundTest():
    q = [0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365,
         0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6,
        0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e,
        0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a]
    a = [0xa890d39d, 0x65d71596, 0xe9487daa, 0xc8ca6a86,
        0x949d2192, 0x764b7754, 0xe408d9b9, 0x7a41b4d1,
        0x3402e183, 0x3c3af432, 0x50669f96, 0xd89ef0a8,
        0x0040ede5, 0xb545fbce, 0xd257ed4f, 0x1818882d]
    q = [Word(i) for i in q]
    a = [Word(i) for i in a]
    z = rowround(q)
    print(a==z)
    return


