import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        clock.tick(fps)