# Version: Prototype
from cmath import rect
from dis import dis
from re import T
import pygame, sys, os
import random
import data.engine as e

clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512) # parameters: (frequency, size, channels, buffer)... This buffers the sfx so it is not delayed.

pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Kid-Oni')

WINDOW_SIZE = (1600,900)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((320,180)) # used as the surface for rendering, which is scaled later on

# physics variables:
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
jump_counter = 0
true_scroll = [0,0]
scroll_x_divisor = 20
scroll_y_divisor = 20
screen_shake = 0
dash_counter = 0
dash_counter_cooldown = 0
player_dash = 10
background_objects = [0.25,[]]

def blit_parallax_bg(objects=[]):
    i = 0
    if not objects is []:
        for object in objects: 
            pygame.draw(rect, )
        
# loc is a list of 2 numbers which represent the x and y axis respectively, eg: [2,-2]
def image_outline(img,loc,surf=display): 
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface(setcolor=(30,30,30),unsetcolor=(0,0,0))
    mask_surf.set_colorkey((0,0,0))
    surf.blit(mask_surf,(loc[0]+1,loc[1]+1),special_flags=BLEND_RGB_SUB)
    surf.blit(mask_surf,(loc[0]+2,loc[1]+1),special_flags=BLEND_RGB_SUB)
    surf.blit(mask_surf,(loc[0]+1,loc[1]+2),special_flags=BLEND_RGB_SUB)

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

e.load_animations('data/images/entities/')

level_1 = load_map('data/map')

main_background = pygame.image.load('data/images/other_assets/main_background.png').convert()

# Loading the tileset:
tile_1 = pygame.image.load('data/images/tiles/tile_1.png').convert()
tile_1.set_colorkey((255,255,255))
tile_2 = pygame.image.load('data/images/tiles/tile_2.png').convert()
tile_2.set_colorkey((255,255,255))
tile_3 = pygame.image.load('data/images/tiles/tile_3.png').convert()
tile_3.set_colorkey((255,255,255))
tile_5 = pygame.image.load('data/images/tiles/tile_5.png').convert()
tile_5.set_colorkey((255,255,255))
tile_7 = pygame.image.load('data/images/tiles/tile_7.png').convert()
tile_7.set_colorkey((255,255,255))
tile_9 = pygame.image.load('data/images/tiles/tile_9.png').convert()
tile_9.set_colorkey((255,255,255))
tile_a = pygame.image.load('data/images/tiles/tile_a.png').convert()
tile_a.set_colorkey((255,255,255))
tile_c = pygame.image.load('data/images/tiles/tile_c.png').convert()
tile_c.set_colorkey((255,255,255))

# audio loading
footstep_sounds_timer = 0
jump_sound = pygame.mixer.Sound('data/audio/jump_0.wav')
footstep_sounds = [pygame.mixer.Sound('data/audio/footsteps_0.wav'), pygame.mixer.Sound('data/audio/footsteps_1.wav'), pygame.mixer.Sound('data/audio/footsteps_2.wav'), pygame.mixer.Sound('data/audio/footsteps_3.wav')]
sword_slash = pygame.mixer.Sound('data/audio/sword_slice_0.wav')

sword_slash.set_volume(0.1)
jump_sound.set_volume(0.5)
footstep_sounds[0].set_volume(0.3)
footstep_sounds[1].set_volume(0.3)
footstep_sounds[2].set_volume(0.3)
footstep_sounds[3].set_volume(0.3)

player_x_offset = 144
player_y_offset = 106
player = e.entity(80,100,6,16,'player')

while True: # game loop
    display.fill((168,181,178)) # clear screen by filling it with the bg color. This serves as the background

    # timers
    if footstep_sounds_timer > 0:
        footstep_sounds_timer -= 1
    if screen_shake > 0:
        screen_shake -= 1

    # scroll managers
    true_scroll[0] += (player.x-true_scroll[0]-player_x_offset)/scroll_x_divisor
    true_scroll[1] += (player.y-true_scroll[1]-player_y_offset)/scroll_y_divisor
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    # screen shake parameters
    if screen_shake:
        scroll[0] += random.randint(0,2) - 1
        scroll[0] += random.randint(0,2) - 1
        scroll[1] += random.randint(0,2) - 1
        scroll[1] += random.randint(0,2) - 1

    # tile rendering
    display.blit(main_background,(0,0))
    tile_rects = []
    y = 0
    for layer in level_1:
        x = 0
        for tile in layer:
            if tile == '1':
                image_outline(tile_1,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_1,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                image_outline(tile_2,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_2,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '3':
                image_outline(tile_3,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_3,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '4':
                image_outline(pygame.transform.flip(tile_3,True,False),(x*16-scroll[0],y*16-scroll[1]))
                display.blit(pygame.transform.flip(tile_3,True,False),(x*16-scroll[0],y*16-scroll[1]))
            if tile == '5':
                image_outline(tile_5,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_5,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '6':
                image_outline(pygame.transform.flip(tile_5,True,False),(x*16-scroll[0],y*16-scroll[1]))
                display.blit(pygame.transform.flip(tile_5,True,False),(x*16-scroll[0],y*16-scroll[1]))
            if tile == '7':
                image_outline(tile_7,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_7,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '8':
                image_outline(pygame.transform.flip(tile_7,True,False),(x*16-scroll[0],y*16-scroll[1]))
                display.blit(pygame.transform.flip(tile_7,True,False),(x*16-scroll[0],y*16-scroll[1]))
            if tile == '9':
                image_outline(tile_9,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_9,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'a':
                image_outline(tile_a,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_a,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'b':
                image_outline(pygame.transform.flip(tile_a,True,False),(x*16-scroll[0],y*16-scroll[1]))
                display.blit(pygame.transform.flip(tile_a,True,False),(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'c':
                image_outline(tile_a,(x*16-scroll[0],y*16-scroll[1]))
                display.blit(tile_c,(x*16-scroll[0],y*16-scroll[1]))
            if tile == 'd':
                image_outline(pygame.transform.flip(tile_c,True,False),(x*16-scroll[0],y*16-scroll[1]))
                display.blit(pygame.transform.flip(tile_c,True,False),(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

            x += 1
        y += 1

    # DASH MECHANICS
    if dash_counter_cooldown > 0:
        dash_counter_cooldown -= 1
    if dash_counter > 1:
        dash_counter = 1
    if dash_counter < 0:
        dash_counter = 0
    if dash_counter_cooldown is 0: 
        dash_counter = 1
    if player_dash > 0:
        player_dash -= 1
    elif player_dash < 0:
        player_dash += 1

    # dash is added to player's x movement
    player_movement = [0,0]
    
    if player.flip is False:
        if player_dash > 0:
            player_movement[0] = player_dash
        elif moving_right:
            player_movement[0] += 2
    if player.flip is True:
        if player_dash < 0:
            player_movement[0] = player_dash
        elif moving_left:
            player_movement[0] -= 2

    player_movement[1] += vertical_momentum
    vertical_momentum += 0.23
    if vertical_momentum > 6: vertical_momentum = 6

    # animation handling/changing
    if air_timer > 6:
        player.set_action('jump')
    elif player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(False)
        if air_timer < 12:
            player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(True)
        if air_timer < 12:
            player.set_action('run')

    # handling player colissions
    collisions_types = player.move(player_movement,tile_rects)

    # If the player is touching the floor
    if collisions_types['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        jump_counter = 0
        if player_movement[0] != 0 and (player_movement[0] > 1 or player_movement[0] < -1):
            if footstep_sounds_timer == 0:
                footstep_sounds_timer = 25
                random.choice(footstep_sounds).play()
    else:
        air_timer += 1
        # if the player hits the bottom of a tile rect, they won't stay stuck for a few frames. This simulates that the player bonked his head onto the tile.
        if collisions_types['top']:
            vertical_momentum += 1

    player.change_frame(1)
    player.display(display,scroll)

    for event in pygame.event.get(): # event loop to check for events such as keyboard input
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                jump_counter += 1
                if jump_counter is 1: 
                    vertical_momentum = -5.4
                    jump_sound.play()
                    if air_timer > 10:
                        jump_counter += 1
                elif jump_counter is 2:
                    vertical_momentum = -5.2
                    jump_sound.play()
            if event.key == K_d:
                moving_right = True
                player.flip = False
            if event.key == K_a:
                moving_left = True
                player.flip = True
            if event.key == K_SPACE:
                    if dash_counter == 1:
                        dash_counter_cooldown = 60
                        vertical_momentum = 0
                        if player.flip == True:
                            sword_slash.play()
                            player_dash = -11
                            screen_shake = 11
                        elif player.flip == False:
                            sword_slash.play()
                            player_dash = 11
                            screen_shake = 11
                        dash_counter -= 1  
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    # blits the display screen and resizes it to the bigger screen res
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
