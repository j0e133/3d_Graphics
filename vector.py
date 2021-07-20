from math import sin, cos, inf


class vector:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

        self.tup = (x, y)

    def __add__(self, o):
        return vector(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return vector(self.x - o.x, self.y - o.y)

    def __mul__(self, o: float):
        return vector(self.x * o, self.y * o)

    def __truediv__(self, o: float):
        try:
            return vector(self.x / o, self.y / o)
        except ZeroDivisionError:
            return vector(0, 0)

    def clamp(self, _min, _max):
        return vector(min(_max.x, max(_min.x, self.x)), min(_max.y, max(_min.y, self.y)))

    def flipY(self):
        return vector(self.x, -self.y)



class vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

        self.tup = (x, y, z)

    def __add__(self, o):
        return vector3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o):
        return vector3(self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, o: float):
        return vector3(self.x * o, self.y * o, self.z * o)

    def __truediv__(self, o: float):
        try:
            return vector3(self.x / o, self.y / o, self.z / o)
        except ZeroDivisionError:
            return vector3(0, 0, 0)

    def __neg__(self):
        return vector3(-self.x, -self.y, -self.z)

    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def normalize(self, magnitude = 1):
        return (self / self.magnitude() * magnitude) if magnitude else self / self.magnitude()

    def clamp(self, _min, _max):
        return vector3(max(_min.x, min(_max.x, self.x)), max(_min.y, min(_max.y, self.y)), max(_min.z, min(_max.z, self.z)))

    @staticmethod
    def pointOnSphere(angles, rad = 1):
        return vector3(sin(angles.y) * cos(angles.x), sin(-angles.x), cos(angles.y) * cos(angles.x))

    @staticmethod
    def dot(a, b) -> float:
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def sum(lst):
        out = vector3(0, 0, 0)
        for i in lst:
            out += i
        return out

    @staticmethod
    def distSquared(a, b) -> float:
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2

    @staticmethod
    def fromIterable(iterable):
        return vector3(iterable[0], iterable[1], iterable[2])


# add class variables
setattr(vector, 'zero', vector(0, 0))

setattr(vector3, 'up', vector3(0, 1, 0))
setattr(vector3, 'down', vector3(0, -1, 0))