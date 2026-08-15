with open("map/rivers.bmp", "r+b") as f:
    f.seek(0x2F)
    f.write(b"\x00")
    f.seek(0x33)
    f.write(b"\x00")