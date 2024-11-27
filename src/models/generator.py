import pygame

from settings import *
from timerizer import Timer

class Generator:
    def __init__(self, screen):
        self.obj = None
        self.display_suface = screen
        self.color = 'red'
        
        self.frames = []
        self.import_assets()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (screen_width/2 - 90, screen_height/2 + 13))

        self.head_surf = pygame.image.load('imgs/gerador/head.png').convert_alpha()
        self.head_rect = self.head_surf.get_rect(center= (screen_width/2 - 2, screen_height/3 + 15))
        self.head_mask = pygame.mask.from_surface(self.head_surf)
        self.head = True
        self.timer_head = Timer(0.3)

        self.run = True
        self.move_speed = [0.1]
        
        self.camp_elet = None
        self.campo_elet_val = 0
        self.vel_cor = 0

    def import_assets(self):
        for i in range(5):
            path = f'imgs/gerador/{i}.png'
            self.frames.append(pygame.image.load(path).convert_alpha())

    def input(self, bas):
        mouse_surf = pygame.Surface((5, 5))
        mouse_rect = mouse_surf.get_rect(center = (pygame.mouse.get_pos()))
        mouse_mask = pygame.mask.from_surface(mouse_surf)

        offset_x = self.head_rect.left - mouse_rect.left
        offset_y = self.head_rect.top - mouse_rect.top
        if mouse_mask.overlap_area(self.head_mask, (offset_x, offset_y)) and not self.timer_head.run:
            if pygame.mouse.get_pressed()[0] and not bas.collide:
                self.head = not self.head
                self.timer_head.active()

    def animate(self, on):
        if self.move_speed[0] > 0 and on:
            self.frame_index += self.move_speed[0]
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, bas, on):
        self.input(bas)
        self.animate(on)
        if self.timer_head.run:
            self.timer_head.update()

    def circleSurface(self, color, radius):
            shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shape_surf, color, (radius, radius), radius)
            return shape_surf 

    def draw_circ(self):
        pygame.draw.circle(self.display_suface, 'green', (screen_width/2, screen_height/3 + 20), self.campo_val, 3) 

    def draw_backhead(self):
        if not self.head:
            self.display_suface.blit(self.head_surf, self.head_rect)     

    def draw(self):     
        self.obj = self.circleSurface(self.color, 125)
        self.obj_rect = self.obj.get_rect(center= (screen_width/2, screen_height/3 + 25))
        self.obj_mask = pygame.mask.from_surface(self.obj)   

        if 0.1 <= self.move_speed[0] < 0.2: 
            self.campo_val = 180 
        elif 0.2 <= self.move_speed[0] < 0.3:
            self.campo_val = 200
        elif 0.3 <= self.move_speed[0] < 0.4:
            self.campo_val = 220
        elif 0.4 <= self.move_speed[0] < 0.5:
            self.campo_val = 230
        else:
            self.campo_val = 0

        self.camp_elet = self.circleSurface('green', self.campo_val)
        self.camp_elet_rect = self.camp_elet.get_rect(center = ((screen_width/2, screen_height/3 + 20)))
        self.camp_elet_mask = pygame.mask.from_surface(self.camp_elet)
         
        self.display_suface.blit(self.image, self.rect)
        if self.head:
            self.display_suface.blit(self.head_surf, self.head_rect)