import pygame
from pygame.locals import *
from math import sin, cos
from vector import vector, vector3
from mesh import Mesh, Object
from camera import camera3

# initiate pygame
pygame.init()


# function for drawing all of the faces
def draw():
    # clear the screen
    screen.fill(BLACK)

    # project the vertices to the screen
    for vertex in vertices:
        vertex.update(camera)

    # draw all of the faces
    faces.sort(key = lambda face: face.sortKey(), reverse = True)

    for face in faces:
        face.draw(screen, camera, showOutline)

    # draw the light
    if vector3.dot((lightPos - camera.pos).normalize(), camera.normal) > 0:
        pygame.draw.circle(screen, (255, 255, 0), camera.projection(lightPos).tup, min(30, max(1, 500 / vector3.distSquared(camera.pos, lightPos) ** 0.5)))

    # draw the crosshair
    pygame.draw.line(screen, (200, 200, 200), (CENTER.x, CENTER.y - 5), (CENTER.x, CENTER.y + 5), 3)
    pygame.draw.line(screen, (200, 200, 200), (CENTER.x - 5, CENTER.y), (CENTER.x + 5, CENTER.y), 3)

    # update screen
    pygame.display.flip()


# input functions
def w():
    return foward
def a():
    return left
def s():
    return -foward
def d():
    return -left
def space():
    return vector3.up
def shift():
    return vector3.down
def end():
    pygame.quit()
    raise SystemExit


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# settings
FOV = 90
FPS = 60
SPEED = 0.05
RESOLUTIONSCALE = 16 / 9
RESOLUTIONP = 720
RESOLUTION = vector(int(RESOLUTIONP * RESOLUTIONSCALE), RESOLUTIONP)
CENTER = RESOLUTION / 2

# camera
camera = camera3(vector3(0, 0, -50), CENTER, FOV)
cameraMove = vector3(0, 0, 0)

# light
lightPos = vector3(0, 15, 0)

# add sphere to the scene
mesh = Mesh()
mesh.load('3dObjects/sphere.mesh')

faces = Object(mesh, vector3(0, 0, 0), 5, lightPos)

vertices = {vertex for face in faces for vertex in face.vertices}

# input
pressed = {
K_w: False,
K_a: False,
K_s: False,
K_d: False,
K_UP: False,
K_DOWN: False,
K_LEFT: False,
K_RIGHT: False,
K_ESCAPE: False,
K_SPACE: False,
K_LSHIFT: False,
}

funcs = {
K_w: w,
K_a: a,
K_s: s,
K_d: d,
K_UP: w,
K_DOWN: s,
K_LEFT: a,
K_RIGHT: d,
K_ESCAPE: end,
K_SPACE: space,
K_LSHIFT: shift,
}

showOutline = True

# screen and fps
screen = pygame.display.set_mode(RESOLUTION.tup)
clock = pygame.time.Clock()
dt = clock.tick()

# center mouse 
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(*CENTER.tup)


# gameloop
while True:
    # handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            end()
        elif event.type == KEYDOWN and event.key == K_f:
            showOutline = not showOutline
        elif event.type in {KEYDOWN, KEYUP} and event.key in pressed:
            pressed[event.key] = not pressed[event.key]

    # rotate the camera
    x, y = pygame.mouse.get_pos()
    camera.rotate(vector3((y - CENTER.y) * 0.15, (x - CENTER.x) * 0.15, 0), dt, 1)

    pygame.mouse.set_pos(*CENTER.tup)

    # move the camera
    foward = vector3(sin(camera.rotation.y), 0, cos(camera.rotation.y))
    left = vector3(-foward.z, 0, foward.x)

    camera.pos += vector3.sum(funcs[key]() * SPEED * dt for key in pressed if pressed[key])

    # draw scene
    draw()

    # limit fps
    dt = clock.tick(FPS)