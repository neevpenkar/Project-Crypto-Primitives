from Word32 import makeWordListFromBytes
endian = 'big'
class Counter:
    def __init__(self, num: int):
        self.value = num
        return

    def __add__(self, i: int):
        return self.value + i

    def to_bytes(self, order=endian):
        self.value *= 8
        return bytearray(self.value.to_bytes(8, order))

    def to_wordList(self, order=endian):
        return makeWordListFromBytes(self.to_bytes(), 4, 2)

    pass

class SHA_Padding:
    def __init__(self, data):
        self.length = len(data)
        self.data = bytearray(data)
        return

    def pad(self):
        WSIZE = 4
        BSIZE = 16

        # to pad = 64 - len(data) % 64
        topad = len(self.data) % (BSIZE * WSIZE)
        topad = BSIZE * WSIZE - topad

        # If topad is greater than 56 bytes, pad with another (63 - 8) zeroes
        if topad < 8:
            self.data.append(0x80)
            self.data.extend(bytearray(0) * (63-8))

        # If topad is lesser than 56 bytes, pad remaining zeroes
        if topad >= 8:
            topad -= (1 + 8)
            if topad < 0:
                raise RuntimeError("Bro what the hell")#Shouldn't happen by design

            self.data.append(0x80)
            self.data.extend(bytearray([0] * topad))

        counter = Counter(self.length)
        self.data.extend(counter.to_bytes())

        return self.data
    
