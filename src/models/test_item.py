import pygame
import math

from settings import *
from timerizer import Timer
from models.gas_circle import GasCircle
from models.light import Light
from models.charge import Charge

class TestItem:
    def __init__(self, screen):   
        self.display_surface = screen   
        self.image_surf = pygame.image.load('imgs/staff.png').convert_alpha()  
        self.image_surf = pygame.transform.scale(self.image_surf, (self.image_surf.get_width()/2, self.image_surf.get_height()/2))
        self.rotated_img = pygame.transform.flip(self.image_surf, True, False)      
        self.image = self.image_surf
        self.rect = self.image.get_rect(center = (300, 200))

        # sound
        self.elet_sound = pygame.mixer.Sound('sound/electricity.mp3')

        self.move_x = -40
        self.move_y = 78
        self.contact_surf = self.circleSurface('black', 58)
        self.contact_rect = self.contact_surf.get_rect(center= (self.rect.topleft[0] + self.rect.size[0]/2 + self.move_x, 
                                                                                                    self.rect.topleft[1] + self.move_y))
        self.contact_mask = pygame.mask.from_surface(self.contact_surf)

        self.collide = False
        self.collide_camp = False
        self.collide_obj = False

        self.gas = GasCircle(self.display_surface)
        self.create_gas = False

        self.light = False
        self.line_gas = None
        self.light_flash = Light(self.display_surface)

        self.obj = None

        self.charge_list = [[charge[0] + self.contact_rect.centerx, charge[1] + self.contact_rect.centery] for charge in charge_bas]
        for i in range(len(self.charge_list)):
            name = charge_bas_col[0][i]
            self.charge_list[i] = Charge(self.display_surface, self.charge_list[i], name, False)
         
        
    def draw(self, on, time_pass, move_speed):
        self.display_surface.blit(self.image, self.rect)

        for i in range(len(self.charge_list)):
            self.charge_list[i].rect.center = [charge_bas[i][0] + self.contact_rect.centerx, 
                                                        charge_bas[i][1] + self.contact_rect.centery]
            # modificando as cargas do bastão
            if self.collide_obj and on and time_pass:
                self.charge_list[i].change_charge('pos')
            elif self.collide_camp and on:
                d_x = 75
                if self.rect.centerx < screen_width/2 - d_x:
                    self.charge_list[i].change_charge(charge_bas_col[1][i])
                elif self.rect.centerx > screen_width/2 + d_x:
                    self.charge_list[i].change_charge(charge_bas_col[2][i])
                elif screen_width/2 - d_x < self.rect.centerx <= screen_width/2 + d_x and self.rect.centery > self.obj.centery:
                    self.charge_list[i].change_charge(charge_bas_col[3][i])
                elif screen_width/2 - d_x < self.rect.centerx <= screen_width/2 + d_x and self.rect.centery < self.obj.centery:
                    self.charge_list[i].change_charge(charge_bas_col[4][i])
            else:
                self.charge_list[i].change_charge(charge_bas_col[0][i])
            
            if i != len(self.charge_list)-1 or self.collide_obj and time_pass:
                if time_pass:
                    self.charge_list[i].update(move_speed/2)

                self.charge_list[i].draw(True)
            

        if self.gas.circles and on:
            self.gas.draw()
            self.elet_sound.play(-1)
        
        if self.light and on and not self.gas.timer_gas.run:
            self.light_flash.draw()
            self.elet_sound.play(-1)
        elif not self.light or not on:
            self.elet_sound.stop()
    
    def update(self, gen): 
        self.obj = gen.obj_rect
        if self.create_gas:
            if not self.gas.circles and not self.gas.timer_gas.run and not self.light:
                self.gas.create_circles(self.line_gas.center)
                self.gas.timer_gas.active()
                self.light = True
            self.gas.update()
                 
        if self.light and not self.gas.timer_gas.run:
            self.light_flash.update(self.line_contact.center, self.ang, self.rect, gen.obj_rect.centery)
        
        self.input()
        self.line_gas = pygame.draw.line(self.display_surface, 'red', self.rect.center, gen.obj_rect.center, 1)
        self.line_contact = pygame.draw.line(self.display_surface, 'red', self.contact_rect.center, gen.obj_rect.center, 1)

        # pegando o cateto adjacente e hipotenusa
        quad_surf = pygame.Surface(self.line_gas.size)
        quad_rect = quad_surf.get_rect(center = (self.line_gas.center))

        cat_ad = quad_rect.size[0]
        dist_euc = (gen.obj_rect.center[0] - self.rect.center[0])**2 + (gen.obj_rect.center[1] - self.rect.center[1])**2
        hip = math.sqrt(dist_euc)
        try:
            self.ang = math.acos(cat_ad/hip)
        except Exception as e:
            self.ang = 0

        self.inverse()
        self.contact_rect = self.contact_surf.get_rect(center= (self.rect.topleft[0] + self.rect.size[0]/2 + self.move_x, 
                                                                                                    self.rect.topleft[1] + self.move_y))
        self.colision(gen)
            
    def inverse(self):
        if self.rect.centerx < screen_width/2:
            self.move_x = 40
            self.image = self.rotated_img
        else:
            self.move_x = -40
            self.image = self.image_surf        
        
    def input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.rect.center = pygame.mouse.get_pos()
                self.collide = True
        else:
            self.collide = False    

    def colision(self, gen):
        offset_x_camp = gen.camp_elet_rect.left - self.contact_rect.left
        offset_y_camp = gen.camp_elet_rect.top - self.contact_rect.top

        offset_x_obj = gen.obj_rect.left - self.contact_rect.left
        offset_y_obj = gen.obj_rect.top - self.contact_rect.top

        if self.contact_mask.overlap(gen.obj_mask, (offset_x_obj, offset_y_obj)):
            self.create_gas = False
            self.gas.circles.clear()
            self.light = False

            self.collide_obj = True
            self.collide_camp = False
        elif self.contact_mask.overlap(gen.camp_elet_mask, (offset_x_camp, offset_y_camp)):
            self.create_gas = True

            self.collide_obj = False
            self.collide_camp = True
        else:
            self.create_gas = False
            self.gas.circles.clear()
            self.light = False

            self.collide_obj = False
            self.collide_camp = False

    def circleSurface(self, color, radius):
            shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shape_surf, color, (radius, radius), radius)
            return shape_surf 