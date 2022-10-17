import pygame
from settings import *
from random import randint
from timer import Timer
import math

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

        self.charge_list = [[charge[0] + self.contact_rect.centerx, charge[1] + self.contact_rect.centery] for charge in charge_bas]
        for i in range(len(self.charge_list)):
            if i%2 == 0:
                name = 'neg' if i != len(self.charge_list)-1 else 'pos'
                self.charge_list[i] = Charge(self.display_surface, self.charge_list[i], name, False)
            else:
                self.charge_list[i] = Charge(self.display_surface, self.charge_list[i], 'pos', False)
        
    def draw(self, on, time_pass, move_speed):
        self.display_surface.blit(self.image, self.rect)

        for i in range(len(self.charge_list)):
            self.charge_list[i].rect.center = [charge_bas[i][0] + self.contact_rect.centerx, 
                                                        charge_bas[i][1] + self.contact_rect.centery]
            
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


class Button:
    def __init__(self, screen, ref, pos, div, switch=False):
        self.reference = ref
        self.display_surface = screen
        self.timer_button = Timer(0.3)
        self.button_frames = []
        self.button_frame_index = 0
        self.div = div
        self.switch = switch
        self.import_assets()
        self.image = self.button_frames[0]
        self.rect = self.image.get_rect(center= (pos))

    def import_assets(self):
        if not self.switch:
            num = 4
            path = f'imgs/button_switch/button/'
        else:
            path = f'imgs/button_switch/switch/'
            num = 2
        self.image_surf = [pygame.image.load(path + f'{i}.png').convert_alpha() for i in range(num)]
        self.button_frames = [pygame.transform.scale(image, (image.get_width()/self.div, image.get_height()/self.div))
                                                                                                 for image in self.image_surf]

    def animate(self):
        if not self.switch:
            self.button_frame_index = 0 if self.reference[0] == 0 else int(self.reference[0]*10) - 1
            self.image = self.button_frames[self.button_frame_index]
        else:
            if self.reference[0]:
                self.image = self.button_frames[1]
            else:
                self.image = self.button_frames[0]

    def draw(self):
        self.display_surface.blit(self.image, self.rect)

    def update(self, bas):
        self.input(bas)
        if self.timer_button.run:
            self.timer_button.update()
        self.animate()

    def input(self, bas):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.timer_button.run:
            if pygame.mouse.get_pressed()[0] and not bas.collide:
                if not self.switch:
                    self.reference[0] += 0.1
                    if self.reference[0] > 0.4:
                        self.reference[0] = 0.1
                else:
                    self.reference[0] = not self.reference[0]

                self.timer_button.active()


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

    