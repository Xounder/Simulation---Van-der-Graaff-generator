import pygame

from settings import *
from random import randint
from timerizer import Timer

class GasCircle:
    def __init__(self, screen):
        self.display_surface = screen
        self.circles = []
        self.change = False
        self.timer_gas = Timer(0.2)

    def create_circles(self, line_gas):
        for i in range(8):
            circ = [line_gas[0] - randint(-40, 40),  line_gas[1] - randint(-40, 40)]
            self.circles.append(circ)
        
    def move_circles(self):
        move_speed = 2.5
        for circ in self.circles:
            if not self.change:
                circ[0] -= move_speed
                circ[1] -= move_speed
            else:
                circ[0] += move_speed
                circ[1] += move_speed

        self.change = not self.change

    def update(self):
        if self.timer_gas.run:
            self.timer_gas.update()
            if not self.timer_gas.run:
                self.circles.clear()

        self.move_circles()

    def draw(self):
        for circ in self.circles:
            pygame.draw.circle(self.display_surface, 'gray', (circ[0], circ[1]), 10)
