import pygame
from pymunk import pygame_util as pmg
import pymunk
import random

pmg.positive_y_is_up = False  # единая СК, II четверть(ЮВ)

w, h = 700, 660
fps = 60

a, b, c, d = 2, 8, 30, 137
x1, x2, x3, x4 = a, w // 2 - b, w // 2 + b, w - a
y1, y2, y3, y4 = 0, c, d - c, d
L1, L2, L3, L4 = (x1, y1), (x1, y2), (x2, y3), (x2, y4)
R1, R2, R3, R4 = (x4, y1), (x4, y2), (x3, y3), (x3, y4)

pygame.init()
window = pygame.display.set_mode(size=(w, h))
pygame.display.set_caption("Halton Board")
timer = pygame.time.Clock()
options = pmg.DrawOptions(window)

space = pymunk.Space()  # область симуляции
space.gravity = 0, 666


def create_box(pos):
    mass, size = 10, (66, 66)
    moment = pymunk.moment_for_box(mass, size)
    box_body = pymunk.Body(mass, moment)
    box_body.position = pos

    box_polygon = pymunk.Poly.create_box(box_body, size)
    box_polygon.elasticity = 0.3
    box_polygon.friction = 0.2
    box_polygon.color = [random.randrange(256) for i in range(4)]
    return space.add(box_body, box_polygon)


def create_ball(space, pos):
    ball_mass, ball_radius = 10, 3.2
    moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    body = pymunk.Body(ball_mass, moment)
    body.position = pos
    body.color = [random.randrange(256) for i in range(4)]
    ball = pymunk.Circle(body, ball_radius)
    ball.color = [random.randrange(256) for i in range(4)]
    ball.elasticity = 0.1
    ball.friction = 0.2
    space.add(body, ball)
    return body


def create_stick(A, B):
    stick = pymunk.Segment(space.static_body, A, B, 4)
    stick.elasticity = 0.2
    stick.friction = 0.2
    return space.add(stick)

def create_broken(*args):
    for i in range(len(args) - 1):
        create_stick(args[i], args[i + 1])

def create_peg(x, y, color):
    peg = pymunk.Circle(space.static_body, radius=3, offset=(x, y))
    peg.elasticity = 0.1
    peg.friction = 0.8
    peg.color = color
    return space.add(peg)
def create_triangle_Pascal(space, lin):
    y = h//5+5
    a = 20
    for line in range(1, lin):
        x = w//2
        y += a
        x -= a * (line - 1)
        for column in range(1, line+1):
            if x == w//2:
                create_peg(x, y, [0, 0, 0, 0])
            else:
                create_peg(x, y, pygame.color.THECOLORS['orange'])
            x += 2*a
def create_floor_up(a):
    x1, x2 = w//2, w//2
    while 0 <= x1 or x2 <= w:
        create_stick((x1, h), (x1, h - 150))
        create_stick((x2, h), (x2, h - 150))
        x1 -= a
        x2 += a

create_triangle_Pascal(space, 18)
create_floor_up(20)

create_broken(L1, L2, L3, L4, (0, h-120-60))
create_broken(R1, R2, R3, R4, (w, h-120-60))

floor = pymunk.Segment(space.static_body, (0, h), (w, h), 10)
floor.elasticity = 0.1
floor.friction = 0.9

# poly = pymunk.Poly.create_box(body)
# space.add(body, poly)

space.add(floor)
# print_options = pymunk.SpaceDebugDrawOptions()  # For easy printing
#balls = [([random.randrange(256) for i in range(3)], create_ball(space, (random.randint(x1,x4), random.randint(y1,y2)))) for j in range(300)]
balls = []
x = 0
while True:
    window.fill(pygame.Color('gray'))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_ball(space, i.pos)
    x += 1
    if x % 20 == 0:
        balls.append(create_ball(space, (random.randint(x1, x4), random.randint(y1, y2))))
        x = 0

    #if x<=w: create_ball((x, 0))
    space.step(1 / fps)
    space.debug_draw(options)
    [pygame.draw.circle(window, ball.color, (int(ball.position[0]), int(ball.position[1])), 4) for ball in balls]

    pygame.display.flip()
    timer.tick(fps)
