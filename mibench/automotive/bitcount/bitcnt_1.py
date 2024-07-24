def bit_count(x):
    count = 0
    while x:
        count += 1
        x = x & (x - 1)
    return count

if __name__ == "__main__":
    argv = [234, 443, 876, 3456, 854323, 232, 23432, 987887, 9040, 1287]
	
    for arg in argv:
        n = int(arg)
        i = bit_count(n)
        print("{} contains {} bit{} set".format(n, i, "s" if i != 1 else ""))
