from turtle import back
import pygame
import sys
from settings import *
from sprites import Generator, TestItem, Button, Charge
from timer import Timer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Simulação - Gerador de Van Der Graaff')
        self.clock = pygame.time.Clock()
        self.on = [False]
        
        self.gen = Generator(self.screen)
        self.test_item = TestItem(self.screen)
        self.button_speed = Button(self.screen, self.gen.move_speed, (screen_width/2 - 280, screen_height/2 + 200), 3)
        self.button_switch = Button(self.screen, self.on, (screen_width/2 - 180, screen_height/2 + 205), 3, True)

        back_surf = pygame.image.load('imgs/background.jpg').convert()
        self.background_surf =pygame.transform.scale(back_surf, (back_surf.get_width()*1.3, back_surf.get_height()*1.3))
        self.background_rect = self.background_surf.get_rect(topleft = (-200,0))
        #carga da correia do objeto
        self.charge_list = []
        for i in range(4):
            self.charge_list.append(Charge(self.screen, charge_cor_pos[i][:], 'pos'))
            self.charge_list.append(Charge(self.screen, charge_cor_pos_right[i][:], 'pos', change=True))
        # carga do objeto(cabeça)
        self.charge_head = []
        for i in range(len(charge_head)):
            self.charge_head.append(Charge(self.screen, charge_head[i], 'pos', False))

        self.change_charge = [False, False, False]
        self.contact_timer = Timer(0.5)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('blue')
            
            self.gen.update(self.test_item, self.on[0])
            self.gen.draw()
            self.test_item.update(self.gen)
            self.screen.blit(self.background_surf, self.background_rect)
            self.button_switch.update(self.test_item)
            self.button_speed.update(self.test_item)
            if self.on[0]:
                self.gen.draw_circ()
            else:
                self.button_speed.button_frame_index = 0
                self.button_speed.animate()

            self.gen.draw_backhead()
            for charge in self.charge_list:
                charge.update(self.gen.move_speed[0]*10)
                charge.draw(self.on[0])

            # verificando quanto tempo o bastão permanece enconstado no objeto
            if self.test_item.collide_obj and not self.change_charge[0] and not self.contact_timer.run and self.on[0]:
                if not self.change_charge[2]:
                    self.contact_timer.active()
                    self.change_charge[0] = True
            else:
                self.change_charge[2] = False

            if self.contact_timer.run:
                self.contact_timer.update()
                if not self.contact_timer.run:
                    self.change_charge[0] = False
                    self.change_charge[2] = True

            for i ,charges in enumerate(self.charge_head):
                if not self.change_charge[2]:
                    if self.test_item.collide_obj and i%2 == 0:
                        charges.change_charge('neg')
                    else:
                        charges.change_charge('pos')
                else:
                    charges.change_charge('pos')
               
                charges.update(self.gen.move_speed[0]*10)
                charges.draw(self.on[0])


            self.gen.draw()
            self.button_speed.draw()
            self.button_switch.draw()
            self.test_item.draw(self.on[0], self.change_charge[2], self.gen.move_speed[0]*10)
                    
            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()