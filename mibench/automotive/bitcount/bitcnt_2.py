def bitcount(number):
    number = ((number & 0xAAAAAAAA) >> 1) + (number & 0x55555555)
    number = ((number & 0xCCCCCCCC) >> 2) + (number & 0x33333333)
    number = ((number & 0xF0F0F0F0) >> 4) + (number & 0x0F0F0F0F)
    number = ((number & 0xFF00FF00) >> 8) + (number & 0x00FF00FF)
    number = ((number & 0xFFFF0000) >> 16) + (number & 0x0000FFFF)
    return int(number)


if __name__ == "__main__":
    argv = [234, 443, 876, 3456, 854323, 232, 23432, 987887, 9040, 1287]

    for arg in argv:
        n = int(arg)
        i = bitcount(n)
        print("{} contains {} bit{} set".format(n, i, "s" if i != 1 else ""))
