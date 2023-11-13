from Word32 import *
from Crypto.Random import get_random_bytes
from math import floor
Word = Word32

'''
    The specification file:
    https://datatracker.ietf.org/doc/html/rfc7539#section-2.1
    The inputs to ChaCha20 are:

    o  A 256-bit key, treated as a concatenation of eight (words) 32-bit little-
        endian integers.

    o  A 96-bit nonce, treated as a concatenation of three (words) 32-bit little-
        endian integers.

     o  A 32-bit block count parameter, treated as a (one word) 32-bit little-endian
        integer.

    The output is 64 random-looking bytes.

'''
chachaconstants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

def printState(state):
    i = 0
    for word in state:
        if (i != 0) and (i % 4 == 0):
            print()
        print(hex(word.toInt()), end="\t")
        i += 1
    print()

    print()
    return
#def QuarterRound(a, b, c, d):
#    a = a + b
#    d = d ^ a
#    d = d.rotateLeft(16)
#    c = c + d
#    b = b ^ c
#    b = b.rotateLeft(12)
#    a = a + b
#    d = d ^ a
#    d = d.rotateLeft(8)
#    c = c + d
#    b = b ^ c
#    b = b.rotateLeft(7)
#    return a,b,c,d

def QuarterRound(state, a, b, c, d):
    state = state.copy()

    state[a] = state[a] + state[b]
    state[d] = state[d] ^ state[a]
    state[d] = state[d].rotateLeft(16)

    state[c] = state[c] + state[d]
    state[b] = state[b] ^ state[c]
    state[b] = state[b].rotateLeft(12)

    state[a] = state[a] + state[b]
    state[d] = state[d] ^ state[a]
    state[d] = state[d].rotateLeft(8)

    state[c] = state[c] + state[d]
    state[b] = state[b] ^ state[c]
    state[b] = state[b].rotateLeft(7)

    return state

def ChaChaBlockFunction(key: list, counter: Word, nonce: list):
    if len(key) != 8:
        raise ValueError("Key should be 8 words long")
    if len(nonce) != 3:
        raise ValueError("Nonce should be 3 words long")

    state = []
    
    # Init state with constants
    for constant in chachaconstants.copy():
        state.append(Word(constant))

    # Init state with key
    state.extend(key.copy())

    # Init state with counter
    state.append(counter)

    # Init state with nonce
    state.extend(nonce.copy())

    # Init initialstate
    initialstate = state.copy()

    for i in range(10):
        state = QuarterRound(state, 0, 4, 8,12)
        state = QuarterRound(state, 1, 5, 9,13)
        state = QuarterRound(state, 2, 6,10,14)
        state = QuarterRound(state, 3, 7,11,15)

        state = QuarterRound(state, 0, 5,10,15)
        state = QuarterRound(state, 1, 6,11,12)
        state = QuarterRound(state, 2, 7, 8,13)
        state = QuarterRound(state, 3, 4, 9,14)

    # Vector Addition as in the spec
    temp = [(state[i] + initialstate[i]) for i in range(16)]
    return temp

def ChaChaEncryption(key: bytearray, data: bytearray, nonce: bytearray):
    if len(key) != 32:
        raise ValueError("Key should be 32 byte long")
    
    key = makeWordListFromBytes(key, 4, 8)
    counter = Word(0x1)

    #nonce = get_random_bytes(3*4) # 3 Words of randomness
    nonce = makeWordListFromBytes(nonce, 4, 3)

    keystream = bytearray()

    # How many blocks [m (+1)] to encrypt
    statesize = 64
    m = floor(len(data) / 64)
    for i in range(m):
        temp = ChaChaBlockFunction(key, counter, nonce)
        keystream.extend(list2byterray(temp))
        counter = counter + Word(1)

    if (len(data) % statesize != 0):
        temp = ChaChaBlockFunction(key, counter, nonce)
        keystream.extend(list2byterray(temp)[0:len(data) % statesize])

    #return keystream
    return XOR(data, keystream)


def Test1():
    temp = [0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f]
    key = bytearray(temp)

    data = b'''Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it.'''

    # Note, the nonce provided was from the spec
    ct = ChaChaEncryption(key, bytearray(data))
    for i in range(len(ct)):
        print(hex(ct[i])[2:], end = " ")
    print()

