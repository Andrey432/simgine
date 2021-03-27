"""
import sys
import pygame
import engine
import numpy
from math import cos, sin


pygame.init()

RESOLUTION = [800, 600]
BACKGROUND = pygame.Color('black')
FRAMERATE = 0

YELLOW = pygame.Color('yellow')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')


def draw_line(line, end, color=GREEN):
    pygame.draw.line(win, color, line.origin, end)


def draw_circle(circle, color=BLUE):
    pygame.draw.circle(win, color, circle.center, circle.radius, 1)


def draw_point(point, color=RED):
    pygame.draw.circle(win, color, point, 2)


def draw_rect(rect, color=YELLOW):
    points = rect.sides()
    pygame.draw.polygon(win, color, [i.end for i in points], 1)


win = pygame.display.set_mode(RESOLUTION)
fps = pygame.time.Clock()

core = engine.EngineAPI()
core.init()
core.change_scene('SampleScene')


def update():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            core.shutdown()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            core.reload_code()


for _ in core.start():
    win.fill(BACKGROUND)
    update()
    pygame.display.update()
    fps.tick(FRAMERATE)
"""


if __name__ == '__main__':
    from engine.api import Engine

    app = Engine()
    app.init()
    app.change_scene('SampleScene')
    app.run_forever()
