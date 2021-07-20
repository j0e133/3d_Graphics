from vector import vector, vector3
from pygame.gfxdraw import filled_polygon, aapolygon
from pygame.draw import circle
from camera import camera3
from math import sin, cos, acos, tau


# color
OUTLINECOLOR = (30, 30, 30)
VERTEX = (200, 50, 50)

# constants
MIN = vector(-5000, -5000)
MAX = vector(5000, 5000)


class Vertex:
    def __init__(self, pos: vector3):
        self.pos = pos
        self.projection = vector.zero
        self.distToCameraSquared = 0
        self.visible = False

    def __bool__(self):
        return self.visible

    def update(self, camera: camera3):
        # store the projected position and distance to the camera for later use
        if vector3.dot((self.pos - camera.pos).normalize(), camera.normal) > 0:
            self.projection = camera.projection(self.pos)
            self.distToCameraSquared = vector3.distSquared(self.pos, camera.pos)
            self.visible = True
        else:
            self.visible = False



class Mesh:
    def __init__(self):
        self.vertices = list()
        self.faces = set()

    def load(self, filename: str):
        # load a .mesh file into an object
        with open(filename, 'r') as f:
            data = f.read().split('\n')[:-1]

        self.vertices = list()
        self.faces = set()

        for line in data:
            if line[0] == 'v': # vertex
                self.vertices.append(Vertex(vector3.fromIterable(tuple(map(float, line.split()[1:])))))
            elif line[0] == 'f': # face
                self.faces.add(tuple(map(int, line.split()[1:])))

    def getFaceNormal(self, face: tuple) -> vector3:
        # calculate lighting
        points = [self.vertices[i].pos for i in face]

        A = points[1] - points[0]
        B = points[2] - points[0]

        return vector3(
            A.y * B.z - A.z * B.y,
            A.z * B.x - A.x * B.z,
            A.x * B.y - A.y * B.x
            ).normalize()

    def copyToPos(self, pos: vector3, scale = 1.0):
        # duplicate the mesh to a position and scale
        out = Mesh()
        vertices = [Vertex((vertex.pos * scale) + pos) for vertex in self.vertices]
        faces = self.faces
        out.vertices = vertices
        out.faces = faces
        return out



class Face:
    def __init__(self, vertices: list, lightNormal: vector3, normal: vector3):
        self.vertices = vertices
        self.center = vector3.sum(vertex.pos for vertex in self.vertices) / len(self.vertices)

        if vector3.dot(normal, self.center.normalize()) < 0:
            self.normal = -normal
        else:
            self.normal = normal

        self.normalDraw = self.center + self.normal

        light = (vector3.dot(self.normal, lightNormal) + 1) * 100 + 27.5
        self.color = (light, light, light)

    def draw(self, surface, camera: camera3, outline: bool):
        # draw the face onto the screen if it is visible
        if all(self.vertices):
            projectedPoints = [vertex.projection.clamp(MIN, MAX).tup for vertex in self.vertices]
            filled_polygon(surface, projectedPoints, self.color) # face
            if outline:
                aapolygon(surface, projectedPoints, OUTLINECOLOR) # outline

    def sortKey(self):
        # sort the faces from back to front
        return max(vertex.distToCameraSquared for vertex in self.vertices)



def Object(mesh: Mesh, pos: vector3, scale: float, lightPos: vector3) -> list:
    # create an object at position and return all of it's faces
    mesh = mesh.copyToPos(pos, scale = scale)
    lightNormal = (lightPos - pos).normalize()

    faces = []
    for face in mesh.faces:
        vertices = [mesh.vertices[i] for i in face]
        normal = mesh.getFaceNormal(face)
        faces.append(Face(vertices, lightNormal, normal))

    return faces