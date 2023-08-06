

def adc_pack(id, value):
    bs = []
    bs.append((value >> 24) & 0xFF)
    bs.append((value >> 16) & 0xFF)
    bs.append((value >>8) & 0xFF)
    bs.append((value >> 0) & 0xFF)
    bs.append(len(id))
    for i,c in enumerate(id):
        bs.append(ord(c))
    return bytearray(bs)