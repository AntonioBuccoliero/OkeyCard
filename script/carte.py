import os
import pygame

current_path = os.getcwd()
card_back_fold = os.path.join(current_path, 'Immagini/carte')
blu_fold = os.path.join(current_path, 'Immagini/carte/blu')
red_fold = os.path.join(current_path, 'Immagini/carte/rosso')
green_fold = os.path.join(current_path, 'Immagini/carte/verde')

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 740

blu_list = []
red_list = []
green_list = []
for i in range(1, 9):
    blu_list.append((i, os.listdir(blu_fold)[i-1]))
    red_list.append((i, os.listdir(red_fold)[i - 1]))
    green_list.append((i, os.listdir(green_fold)[i - 1]))

total_list = blu_list + green_list + red_list


class Carta(pygame.sprite.Sprite):
    def __init__(self, image_path, x):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.smoothscale(self.image, (130, 160))
        self.rect = self.image.get_rect(
            center=(x, SCREEN_HEIGHT - (SCREEN_HEIGHT*22)/100)
        )


class AvailCard(pygame.sprite.Sprite):
    def __init__(self, image_path,x,y,number,color):
        super().__init__()
        self.image_path=image_path
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.smoothscale(self.image, (60, 90))
        self.rect = self.image.get_rect(
            center=(x, y)
        )
        self.numero = number
        self.colore = color

    def move_up(self,chose_x_pos):
        self.rect.y = SCREEN_HEIGHT/2-SCREEN_HEIGHT/15
        self.rect.x = chose_x_pos

    def move_back(self,x_old,y_old):
        self.rect.y = y_old
        self.rect.x = x_old


