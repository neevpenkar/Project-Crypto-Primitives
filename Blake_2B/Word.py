from bitarray import bitarray

def int2bytearray(number: int, length=8):
    return bytearray(number.to_bytes(length, 'little'))

def bytearray2int(x):
    return int.from_bytes(x, 'little')

MASK = 0xFFFFFFFFFFFFFFFF

class Word(object):
    def __init__(self, val) -> None:
        if type(val) == int:
            #val = val % (2**64)
            val = val & MASK
            self.value = int2bytearray(val, 8)

        elif type(val) == bytearray:
            if len(val) != 8:
                raise ValueError("val is not 8 bytes in size!")
            self.value = val.copy()

        elif (type(val) == bytes) or (type(val) == list):
            if len(val) != 8:
                raise ValueError("val is not 8 bytes in size!")
            self.value = bytearray(val)

        self.hex = hex(self.toInt())
        return

    def __xor__(self, other):
        if len(self.value) != len(other.value):
            raise ValueError("In __xor__ arguments must have same size")
        temp = self.value.copy()
        for i in range(len(self.value)):
            temp[i] ^= other.value[i]
        return Word(temp)

    def toInt(self):
        return bytearray2int(self.value)

    def __add__(self, other):
        temp = self.toInt() + other.toInt() % (2**64)
        return Word(temp)

    def add(self, other1, other2):
        temp = (self.toInt() + other1.toInt() + other2.toInt()) % (2**64)
        return Word(temp)

    def __mod__(self, i=(2**64)):
        return Word(self.toInt() % i)

    def invert(self):
        for i in range(len(self.value)):
            self.value[i] ^= 0xFF
        return self

    def reverseBitsOfByte(self):
        temp = self.value.copy()
        for i in range(len(temp)):
            lower = (temp[i]) & 0xF
            upper = (temp[i] >> 4) & 0xF

            temp[i] = (lower << 4) | (upper)
        return Word(temp)

    def reverseOrder(self):
        temp = []
        for i in self.value:
            temp.insert(0, i)
        return Word(temp)

    def toByteArray(self):
        return self.value.copy()

    def rotateRight(self, i):
        temp = self.toInt()
        i = i % 64
        temp = ((temp>>i) | (temp << (64 - i)))
        return Word(temp)

    def copy(self):
        return Word(self.value.copy())

    def __str__(self):
        temp = bytearray(reversed(self.value.copy()))
        return ''.join('{:02x}'.format(a) for a in temp)

def makeBlock(longArray: bytes | bytearray, finalSize=16):
    '''
    This function can take in upto 128 bytes and return 1 padded block which
    consists of 16 words of 64 bits (8 bytes, 16*8 = 128) each
    '''
    blockSize=8
    wordcounter = 0
    longArray = bytearray(longArray)
    ll = len(longArray)
    
    for i in range(blockSize - (ll % blockSize)):
        longArray.append(0)
    block = []
    for i in range(0, ll + (ll % blockSize), blockSize):
        block.append(Word(longArray[i:i+blockSize]))
        wordcounter += 1

    for i in range(finalSize - wordcounter):
        block.append(Word(0))

    return ll, block

def printBlock(block):
    for i in block:
        temp = str(i)
        temp.removeprefix("0x")
        print(temp, end="")
    print()
    print()
    return

def padArrayBlock(array):
    ''' 
    This function will take in a bytearray, store its initial length,
    pad with necessary zeroes (till multiple of 128).
    m stores the modulus which will be used in the next function
    '''
    if len(array) == 0:
        return 0, 0, bytearray([0]*128)

    modder = 128
    ll = len(array)
    m = ll // modder
    if ll % modder != 0:
        for i in range(modder - (ll % modder)):
            array.append(0)
    return ll, m, array

def makeBlockList(data):
    ll, m ,padded = padArrayBlock(data)
    modder = 128
    temp1 = []

    # Group bytes into 128 byte blocks
    if m == 0:
        temp1.append(padded)
    else:
        i = 0
        if ll % modder != 0:
            m += 1
        while len(temp1) < m:
            temp1.append(padded[i:i+modder])
            i += modder

    finalBlocks = []
    for rawBlock in temp1:
        tempblock = []
        for i in range(16):
            tempblock.append(Word(rawBlock[8*i:8*i+8]))
        finalBlocks.append(tempblock)

    return ll, finalBlocks

#a = bytearray(b"a")
#ll, m, padded = padArrayBlock(a)
#b = makeBlockList(ll, m, padded)

#for i in b:
#    print(i)




############################################
#def tempFunction_1(vector):
#    '''
#    This function will take in a vector, flip it and after that will flip
#    two consecutive 4 bits of a byte
#    '''
#    vector = vector.copy()
#    for i in range(len(vector)):
#        vector[i] = vector[i].reverseOrder()
#        #vector[i] = vector[i].reverseBitsOfByte()
#    return vector


############################################

#operand1 = Word(0x6a09e667f2bdc948)
#operand2 = Word(0x510e527fade682d1)

#print(operand1)
#print(operand2)
#print(operand1 + operand2)
#print(operand1)
#print(operand2)

#test = b"0123456789abcdeffedcba9876543210"
##test = b"abbaabba"*16
#ll, block = makeBlock(test)

#printBlock(block)
#t = tempFunction_1(block)
#printBlock(t)


