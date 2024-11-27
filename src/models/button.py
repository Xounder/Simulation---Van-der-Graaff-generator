import pygame

from settings import *
from timerizer import Timer

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
