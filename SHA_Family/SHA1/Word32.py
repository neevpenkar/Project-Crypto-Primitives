from bitarray import bitarray
endian = 'big'
class Word32:
    '''
    A SHA_1 is a 32 bit unsigned integer
    As seen in the spec, the endianness is big
    '''
    SIZE = 4
    def __init__(self, data) -> None:
        if type(data) == int:
            data %= (2**32)
            self.value = bytearray(int(data).to_bytes(Word32.SIZE, endian))
            self.updateHex()
            return

        elif type(data) == bytearray:
            if len(data) != Word32.SIZE:
                raise ValueError("Bytearray in constructor not 4 bytes: "
                                 + str(len(data)))
            self.value = data.copy()
            self.updateHex()
            return

        elif type(data) == list:
            if len(data) != Word32.SIZE:
                raise ValueError("Bytearray in constructor not 4 bytes: "
                                 + str(len(data)))
            self.value = bytearray(data.copy())
            self.updateHex()
            return

        elif type(data) == Word32:
            self.value = data.value.copy()
            self.updateHex()
        
        self.updateHex()
        return

    def updateHex(self):
        self.hex = hex(self.toInt())

    def __xor__(self, other):
        if type(other) != type(self):
            raise TypeError("other is not of correct type")

        temp = bytearray()
        for i in range(Word32.SIZE):
            temp.append(self.value[i] ^ other.value[i])
        return Word32(temp)

    def __and__(self, other):
        if type(other) != type(self):
            raise TypeError("other is not of correct type")

        temp = bytearray()
        for i in range(Word32.SIZE):
            temp.append(self.value[i] & other.value[i])
        return Word32(temp)

    def __or__(self, other):
        if type(other) != type(self):
            raise TypeError("other is not of correct type")

        temp = bytearray()
        for i in range(Word32.SIZE):
            temp.append(self.value[i] | other.value[i])
        return Word32(temp)

    def __invert__(self):
        temp = bytearray()
        for i in range(Word32.SIZE):
            temp.append(self.value[i] ^ 0xFF)
        return Word32(temp)

    def __add__(self, other):
        return Word32(self.toInt() + other.toInt())

    def toInt(self):
        return int.from_bytes(self.value, endian)

    def toByteArray(self):
        return self.value.copy()

    def __str__(self):
        if endian == 'little':
            temp = bytearray(reversed(self.value.copy()))
        else:
            temp = self.value.copy()
        return "0x" + ''.join('{:02x}'.format(a) for a in temp)

    def rotateRight(self, i=1):
        i = i % 32
        temp = self.toInt()
        return Word32((temp >> i) | (temp << (32 - i)))

    def rotateLeft(self, i=1):
        i = i % 32
        return self.rotateRight(32 - i)

    def __eq__(self, other):
        return (self.toInt() == other.toInt())

    def copy(self):
        return Word32(self.toInt())

    pass


def makeWordListFromBytes(data, wordsize = 4, blocksize = 8):
    data = bytearray(data)
    while (len(data) % wordsize) != 0:
        data.append(0)

    if len(data) > (wordsize * blocksize):
        raise ValueError("Data after padding exceeds maxsize")
    l = []
    for i in range(0, len(data), wordsize):
        l.append(Word32(data[i:i + wordsize]))

    for i in range(blocksize - len(l)):
        l.append(Word32(0))
    return l

def list2int(state: list):
    temp = bytearray(0)
    for word in state:
        temp.extend(Word32(word).toByteArray())
    return int.from_bytes(temp, endian)

def list2byterray(block: list):
    temp = bytearray()
    for word in block:
        temp.extend(word.toByteArray())
    return temp

def int2list(number: int):
    temp = number.to_bytes(64, endian)
    return makeWordListFromBytes(temp, 4, 8)

def XOR(op1, op2):
    if len(op1) != len(op2):
        raise ValueError("XOR needs arrays of equal length")

    temp = op1.copy()
    for i in range(len(op1)):
        temp[i] ^= op2[i]
    return temp

#a = b"123"
#after = makeWordListFromBytes(a)

#bb = list2int(after)