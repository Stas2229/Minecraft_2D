import pygame

pygame.init()
frame_width =32
frame_height = 32
info = pygame.display.Info()
screen_height = info.current_h
screen_width = info.current_w
world_width = 32
world_height = 20
block_size =screen_height/world_height
grawity = 2
clock = pygame.time.Clock()
FPS = 60
