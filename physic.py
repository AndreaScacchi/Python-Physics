# import libraries
import pygame
import pymunk
import pymunk.pygame_util
import math

# initialize pygame
pygame.init()

# set the width and height of the window
WIDTH, HEIGHT = 1000, 750
window = pygame.display.set_mode((WIDTH, HEIGHT))

# define the calculate_distance function
def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

# define the calculate_angle function
def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

# define the drw function
def draw(space, window, draw_options, line):
    window.fill("white")

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)

    space.debug_draw(draw_options)
    pygame.display.update()

# define the create_boundaries function
def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

# define the create_structure function
def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, height - 120), (40, 200), BROWN, 100],
        [(900, height - 120), (40, 200), BROWN, 100],
        [(750, height - 240), (340, 40), BROWN, 150]
    ]

    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius = 2)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

# define the create_swinging_ball function
def create_swinging_ball(space):
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300, 270)

    body = pymunk.Body()
    body.position = (300, 300)
    line = pymunk.Segment(body, (0, 0), (255, 0), 5)
    circle = pymunk.Circle(body, 40, (255, 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)

# define the create_ball function
def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

# define the run function
def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)
    
    # call the functions
    create_boundaries(space, width, height)
    create_structure(space, width, height)
    create_swinging_ball(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None

    # using while loop to check events and based on that call different functions to create ball, calculate angle, distance and so on
    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None

        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)

    # quit pygame
    pygame.quit()

# boilerplate code
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)