import pygame
import math

from settings import *
from random import randint
from timerizer import Timer

class Light:
    def __init__(self, screen):
        self.display_surface = screen
        self.frames = []
        self.import_assets()
        self.rot_frames = self.frames[:]
        self.frame_index = 0
        self.inverse = False
        self.image = self.rot_frames[self.frame_index]
        self.rect = self.image.get_rect(center = (0, 0))
        
    def import_assets(self):
        for i in range(4):
            path = f'imgs/light/{i}.png'
            img_surf = pygame.image.load(path).convert_alpha()
            self.frames.append(pygame.transform.scale(img_surf, (img_surf.get_width()/2.5, img_surf.get_height()/2.5)))

    def draw(self):
        self.display_surface.blit(self.image, self.rect)
            
    def update(self, pos, ang, bas, obj_y):    
        self.rect = self.image.get_rect(center = (pos))
        self.rotate_frames(ang, bas, obj_y)
        self.animate()
    
    def rotate_frames(self, ang, bas, obj_y):
        for i in range(4):
            image_surf = self.frames[i]
            if bas.centerx > screen_width/2:
                image_surf = pygame.transform.flip(image_surf, True, False)
                self.inverse = True
            else:
                self.inverse = False

            ang_rot = ang * 180/math.pi
            if bas.centerx > screen_width/2 and bas.centery > obj_y:
                ang_rot = 180 - ang_rot 
            elif bas.centerx < screen_width/2 and bas.centery < obj_y:
                ang_rot = 180 - ang_rot

            self.rot_frames[i] = pygame.transform.rotate(image_surf, ang_rot)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.rot_frames):
            self.frame_index = 0
        self.image = self.rot_frames[int(self.frame_index)]
