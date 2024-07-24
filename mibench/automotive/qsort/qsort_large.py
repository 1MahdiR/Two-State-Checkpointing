import sys
from math import sqrt

MAX_ARRAY = 60000

argv = [234, 443, 876, 3456, 854323, 232, 23432, 987887, 9040, 1287]


class My3DVertexClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.distance = sqrt(x ** 2 + y ** 2 + z ** 2)


def main():
    array = [My3DVertexClass(3,2,1), My3DVertexClass(56, 12, 1), My3DVertexClass(4,2,1),
    My3DVertexClass(35, 11, 9), My3DVertexClass(12, 0, 48), My3DVertexClass(123, 2, 1),
    My3DVertexClass(7, 88, 12), My3DVertexClass(24, 2, 17), My3DVertexClass(44, 22, 11),
    My3DVertexClass(18, 11, 9)]

    print("\nSorting {} vectors based on distance from the origin.\n".format(len(array)))
    array.sort(key=lambda a: a.distance)

    for item in array:
        print("{} {} {}".format(item.x, item.y, item.z))


if __name__ == "__main__":
    main()
