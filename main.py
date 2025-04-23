import pygame
import os
import math
import random
from script.carte import *
import time

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 740
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
back_obj = os.path.join(current_path, 'Immagini/sfondo')

clock = pygame.time.Clock()
running = True

x_pos = SCREEN_WIDTH/100*15
all_sprites = pygame.sprite.Group()
card_sprites = pygame.sprite.Group()
used_sprites = pygame.sprite.Group()


for i in range(1, 6):
    rand = random.choice(total_list)
    total_list.remove(rand)
    colore = rand[1].split('_')[1].split('.')[0]
    num = rand[1].split('_')[0].split('carta')[1]
    percorso = card_back_fold + '/' + colore + '/' + rand[1]
    y_pos = SCREEN_HEIGHT-(SCREEN_HEIGHT*78)/100
    card_add = AvailCard(percorso, x=x_pos, y=y_pos,color=colore,number=num)
    all_sprites.add(card_add)
    card_sprites.add(card_add)
    x_pos = SCREEN_WIDTH / 100 * 15 + (i * 63)
    print(total_list)

list_used = []
bg = pygame.image.load(os.path.join(back_obj, 'sfondo3.png'))
bg = pygame.transform.smoothscale(bg, screen.get_size())
x_mazzo= SCREEN_WIDTH/2
mazzo= pygame.sprite.Group()
carta = Carta(os.path.join(card_back_fold, 'retro.png'), x_mazzo)
mazzo.add(carta)
all_sprites.add(carta)

slot_used = []
free_y = []
free_x = []
punteggio = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            for item in card_sprites:
                if item.rect.collidepoint(event.pos):
                    free_x.append(item.rect.x)
                    free_y.append(item.rect.y)
                    card_sprites.remove(item)
                    all_sprites.remove(item)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifica se il clic è avvenuto all'interno della bounding box dello sprite
            for el in card_sprites:
                if el.rect.collidepoint(event.pos):
                    if len(used_sprites) == 0:
                        x_pos = SCREEN_WIDTH / 2 - SCREEN_WIDTH / 4
                        free_y.append(el.rect.y)
                        free_x.append(el.rect.x)
                        el.move_up(x_pos)
                        used_sprites.add(el)
                        card_sprites.remove(el)
                        all_sprites.remove(el)
                    elif len(used_sprites) == 1:
                        x_pos = SCREEN_WIDTH / 2 - SCREEN_WIDTH / 15
                        free_y.append(el.rect.y)
                        free_x.append(el.rect.x)
                        el.move_up(x_pos)
                        used_sprites.add(el)
                        card_sprites.remove(el)
                        all_sprites.remove(el)
                    elif len(used_sprites) == 2:
                        x_pos = SCREEN_WIDTH / 2 + SCREEN_WIDTH / 8
                        free_y.append(el.rect.y)
                        free_x.append(el.rect.x)
                        el.move_up(x_pos)
                        used_sprites.add(el)
                        card_sprites.remove(el)
                        all_sprites.remove(el)

            for el in used_sprites:
                if el.rect.collidepoint(event.pos):
                    if len(free_x) == 0:
                        pass
                    elif len(free_x) == 1:
                        x_pos = free_x[0]
                        y_pos = free_y[0]
                        free_y.pop(0)
                        free_x.pop(0)
                        el.move_back(x_pos,y_pos)
                        card_sprites.add(el)
                        all_sprites.add(el)
                        used_sprites.remove(el)
                    elif len(free_x) == 2:
                        x_pos = free_x[0]
                        y_pos = free_y[0]
                        free_y.pop(0)
                        free_x.pop(0)
                        el.move_back(x_pos,y_pos)
                        card_sprites.add(el)
                        all_sprites.add(el)
                        used_sprites.remove(el)
                    elif len(free_x) == 3:
                        x_pos = free_x[0]
                        y_pos = free_y[0]
                        free_y.pop(0)
                        free_x.pop(0)
                        el.move_back(x_pos,y_pos)
                        card_sprites.add(el)
                        all_sprites.add(el)
                        used_sprites.remove(el)

            for item in mazzo:
                if item.rect.collidepoint(event.pos):
                    if len(card_sprites) + len(used_sprites) < 5:
                        if len(total_list)>=5-len(card_sprites) + len(used_sprites):
                            giri = 5-len(card_sprites) + len(used_sprites)
                        else:
                            giri = len(total_list)
                        for i in range(giri):

                            rand = random.choice(total_list)
                            total_list.remove(rand)
                            colore = rand[1].split('_')[1].split('.')[0]
                            num = rand[1].split('_')[0].split('carta')[1]
                            percorso = card_back_fold + '/' + colore + '/' + rand[1]
                            y_pos = SCREEN_HEIGHT - (SCREEN_HEIGHT * 78) / 100
                            x_pos = free_x[0] + SCREEN_WIDTH / 100 * 8
                            #y_pos = free_y[0]
                            free_y.pop(0)
                            free_x.pop(0)
                            card_add = AvailCard(percorso, x=x_pos, y=y_pos, color=colore, number=num)
                            all_sprites.add(card_add)
                            card_sprites.add(card_add)

    screen.blit(bg, (0, 0))
    all_sprites.update()
    used_sprites.draw(screen)
    all_sprites.draw(screen)
#text up
    font = pygame.font.Font('font/SingleDay-Regular.ttf', 32)
    white = (255, 255, 255)
    text_render_white = font.render('PUNTEGGIO: '+ str(punteggio), True, white)
    text_rect = text_render_white.get_rect()
    text_rect.center = (SCREEN_WIDTH-SCREEN_WIDTH*0.32, SCREEN_HEIGHT-SCREEN_HEIGHT*0.95)
    screen.blit(text_render_white, text_rect)

    missing_card= font.render(''+ str(len(total_list)), True, white)
    miss_card=missing_card.get_rect()
    miss_card.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.06)
    screen.blit(missing_card, miss_card)

    pygame.display.flip()
     # limits FPS to 60

    if len(used_sprites)==3:
        time.sleep(0.5)
        list_number=[
            used_sprites.sprites()[0].numero,
            used_sprites.sprites()[1].numero,
            used_sprites.sprites()[2].numero
        ]
        list_color=[
            used_sprites.sprites()[0].colore,
            used_sprites.sprites()[1].colore,
            used_sprites.sprites()[2].colore

        ]
        list_number.sort()

        if int(list_number[0])+1==int(list_number[1]) and int(list_number[1])+1==int(list_number[2]):
            if list_color[0]==list_color[1]==list_color[2]:
                punteggio=punteggio + (sum([int(el) for el in list_number])*5)
                print('scala colore')
                print(punteggio)
                used_sprites.empty()
            else:
                punteggio=punteggio + (sum([int(el) for el in list_number]))
                print('scala no colore')
                print(punteggio)
                used_sprites.empty()
        if list_number[0]==list_number[1]==list_number[2]:
            punteggio = punteggio + (sum([int(el) for el in list_number]))*3
            used_sprites.empty()
            print('tris')
            print(punteggio)
    if len(total_list)==0:
        for item in mazzo:
            all_sprites.remove(item)

    clock.tick(60)
pygame.quit()