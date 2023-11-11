from Blake2_V3_2 import *

try:
    t = "5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555"
    test = bytearray(t, "ascii")#(b"a")
    ll, blocks = makeBlockList(bytearray(test))
    block = blocks#[0]

    pro = Blake2_No_Key(ll, blocks)
    temp = ''.join('{:02x}'.format(a) for a in pro)
    print(temp)

finally:
    logger.close()



#pro = Blake2NoKey(ll, block, 64)
#pro2 = bytearray(reversed(pro))
#temp = ''.join('{:02x}'.format(a) for a in pro)
#print(temp)
