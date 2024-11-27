import pygame

from settings import *
from timerizer import Timer

class Charge:
    def __init__(self, screen, pos, name, cor=True, change=False):
        self.display_surface = screen
        self.neg_charge = pygame.image.load('imgs/charge/neg.png').convert_alpha()
        self.neg_charge = pygame.transform.scale(self.neg_charge, (self.neg_charge.get_width()/6, self.neg_charge.get_height()/6))
        self.pos_charge = pygame.image.load('imgs/charge/pos.png').convert_alpha()
        self.pos_charge = pygame.transform.scale(self.pos_charge, (self.pos_charge.get_width()/6, self.pos_charge.get_height()/6))
        self.name = name

        if self.name == 'pos':
            image_surf = self.pos_charge
        else:
            image_surf = self.neg_charge
        self.image = image_surf
        self.rect = self.image.get_rect(center= (pos))

        self.cor = cor
        self.change = change
    
    def draw(self, on):
        if on:
            self.display_surface.blit(self.image, self.rect)
        
    def update(self, move_speed):
        self.move_charge(move_speed)

    def change_charge(self, name):
        self.name = name
        if self.name == 'pos':
            self.image = self.pos_charge
        else:
            self.image = self.neg_charge

    def move_charge(self, move_speed):
        if self.cor:
            if not self.change:
                self.rect.centery -= move_speed
            else:
                self.rect.centery += move_speed
    
            if not self.change:
                if self.rect.centery <= charge_cor_pos[3][1]:
                        self.rect.center = charge_cor_pos_right[3][:]
                        self.change = True
            else:
                if self.rect.centery >= charge_cor_pos_right[0][1]:
                    self.rect.center = charge_cor_pos[0][:]
                    self.change = False
        else:
            move_speed = round(0.5 * move_speed)
            if not self.change:
                self.rect.centery -= move_speed
                self.rect.centerx -= move_speed
                self.change = True
            else:
                self.rect.centery += move_speed
                self.rect.centerx += move_speed
                self.change = False
