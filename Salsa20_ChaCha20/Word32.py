from bitarray import bitarray
class Word32:
    '''
    A Cha Cha word is a 32 bit unsigned integer
    As seen in the spec, the endianness is little
    '''
    SIZE = 4
    def __init__(self, data) -> None:
        if type(data) == int:
            data %= (2**32)
            self.value = bytearray(int(data).to_bytes(Word32.SIZE, 'little'))
            return

        elif type(data) == bytearray:
            if len(data) != Word32.SIZE:
                raise ValueError("Bytearray in constructor not 4 bytes: "
                                 + str(len(data)))
            self.value = data.copy()
            return

        elif type(data) == list:
            if len(data) != Word32.SIZE:
                raise ValueError("Bytearray in constructor not 4 bytes: "
                                 + str(len(data)))
            self.value = bytearray(data.copy())
            return

        elif type(data) == Word32:
            self.value = data.value.copy()
        return

    def __xor__(self, other):
        if type(other) != type(self):
            raise TypeError("other is not of correct type")

        temp = bytearray()
        for i in range(Word32.SIZE):
            temp.append(self.value[i] ^ other.value[i])
        return Word32(temp)

    def __add__(self, other):
        return Word32(self.toInt() + other.toInt())

    def toInt(self):
        return int.from_bytes(self.value, 'little')

    def toByteArray(self):
        return self.value.copy()

    def __str__(self):
        temp = bytearray(reversed(self.value.copy()))
        return ''.join('{:02x}'.format(a) for a in temp)

    def rotateRight(self, i=1):
        i = i % 32
        temp = self.toInt()
        return Word32((temp >> i) | (temp << (32 - i)))

    def rotateLeft(self, i=1):
        i = i % 32
        return self.rotateRight(32 - i)

    def __eq__(self, other):
        return (self.toInt() == other.toInt())

    pass

def makeWordListFromBytes(data, wordsize = 4, maxsize = 8):
    data = bytearray(data)
    while (len(data) % wordsize) != 0:
        data.append(0)

    if len(data) > (wordsize * maxsize):
        raise ValueError("Data after padding exceeds maxsize")
    l = []
    for i in range(0, len(data), wordsize):
        l.append(Word32(data[i:i + wordsize]))

    for i in range(maxsize - len(l)):
        l.append(Word32(0))
    return l

def list2int(state: list):
    temp = bytearray(0)
    for word in state:
        temp.extend(Word32(word).toByteArray())
    return int.from_bytes(temp, 'little')

def list2byterray(block: list):
    temp = bytearray()
    for word in block:
        temp.extend(word.toByteArray())
    return temp

def int2list(number: int):
    temp = number.to_bytes(64, 'little')
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