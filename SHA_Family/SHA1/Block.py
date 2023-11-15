from Word32 import Word32 as Word
from Word32 import *
from SHA1_Padding import SHA_Padding
class Block:
    BSIZE = 16
    WSIZE = Word.SIZE

    def __init__(self, data):
        self.makeBlock(data)
        return

    def makeBlock(self, data: bytearray):
        if len(data) > Block.BSIZE * Block.WSIZE:
            raise ValueError("Data needs to be 16*4 bytes long")

        self.value = makeWordListFromBytes(data, Block.WSIZE, Block.BSIZE)
        return

    def __getitem__(self, index):
        return self.value[index]

    def printBlock(self):
        for word in self.value:
            print(word)
        return
    pass

def PadAndBlockList(data):
    WSIZE = 4
    BSIZE = 16
    data = SHA_Padding(data).pad()
    blockList = []
    for i in range(0, len(data), BSIZE * WSIZE):
        blockList.append(Block(data[i: i+BSIZE * WSIZE]))

    return blockList


def testVector1():
    from bitarray import bitarray
    tv = bitarray('01100001 01100010 01100011 01100100 01100101')
    tv = tv.tobytes()
    out = PadAndBlockList(tv)
    for o in out:
        o.printBlock()
        print()
    return

#testVector1()