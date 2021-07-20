from vector import vector, vector3
from math import sin as sine, cos as cosine, tan, radians, inf



class camera3:
    def __init__(self, pos: vector3, resolution: vector, fov = 90):
        self.pos = pos
        self.rotation = vector3(0, 0, 0)
        self.offset = vector(resolution.x, resolution.y)
        self.depth = 1 / tan(radians(fov) / 2) * (resolution.x + resolution.y) * 0.5
        self.updateNormal()

    def projection(self, point: vector3) -> vector:
        # function for projecting a point in 3d onto the screen
        difference = self.pos - point

        sin = vector3(sine(self.rotation.x), sine(self.rotation.y), sine(self.rotation.z))
        cos = vector3(cosine(self.rotation.x), cosine(self.rotation.y), cosine(self.rotation.z))

        cameraTransform = vector3(
            cos.y * (sin.z * difference.y + cos.z * difference.x) - sin.y * difference.z,
            sin.x * (cos.y * difference.z + sin.y * (sin.z * difference.y + cos.z * difference.x)) + cos.x * (cos.z * difference.y - sin.z * difference.x),
            cos.x * (cos.y * difference.z + sin.y * (sin.z * difference.y + cos.z * difference.x)) - sin.x * (cos.z * difference.y - sin.z * difference.x)
        )

        return (vector(cameraTransform.x, cameraTransform.y) * self.depth / cameraTransform.z).flipY() + self.offset

    def updateNormal(self):
        # updates the directin that the camera is facing
        self.normal = vector3.pointOnSphere(self.rotation)

    def rotate(self, rot: vector3, dt: float, speed: float):
        # rotate the camera
        self.rotation += rot * (dt * speed * 0.001)
        self.rotation = self.rotation.clamp(vector3(-1.5708, -inf, -inf), vector3(1.5708, inf, inf))
        self.updateNormal()

    def move(self, movement: vector3):
        # move the camera
        self.pos += movement