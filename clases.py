import pygame
from settings import frame_width,frame_height,screen_width,screen_height,grawity,block_size
import math

class Sprite:
    def __init__(self,sprite_sheet):
        self.sheet = pygame.image.load(sprite_sheet).convert_alpha()

    def get_image(self,width,height,row,col,scale=1):
        image = pygame.Surface((width,height),pygame.SRCALPHA)
        image.blit(self.sheet,(0,0),(col*width,row*height,width,height))
        image = pygame.transform.scale(image,(width*scale,height*scale))
        return image
class Photo:
    def __init__(self, image_name, pos, size):
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Block:
    def __init__(self, image_name, size):
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()

    def draw(self, surface, pos):
        self.rect.center = pos
        surface.blit(self.image, self.rect.center)

class Button:
    def __init__(self, image_name, pos, size, text,text_color=(0, 0, 0)):
        self.text = text
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=pos)
        self.message_pos = (pos[0] + size[0] / 2, pos[1] + size[1] / 2)
        self.text_color = text_color

    def draw(self, font, screen):
        message = font.render(self.text, True, self.text_color)
        screen.blit(self.image, self.rect.topleft)
        message_rect = message.get_rect(center=(self.message_pos))
        screen.blit(message, message_rect)

    def is_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Background:
    def __init__(self, image_name):
        pygame.init()
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        steave_sheet = Sprite("images/Steave.png")

        scale_size = int((block_size * 2) // 32)

        self.animations = {
            "walk_right": [
                steave_sheet.get_image(frame_width, frame_height, 0, i, scale=scale_size)
                for i in range(5)
            ],
            "walk_left": [
                steave_sheet.get_image(frame_width, frame_height, 1, i, scale=scale_size)
                for i in range(5)
            ],
            "jump_right": [
                steave_sheet.get_image(frame_width, frame_height, 2, i, scale=scale_size)
                for i in range(2)
            ],
            "jump_left": [
                steave_sheet.get_image(frame_width, frame_height, 3, i, scale=scale_size)
                for i in range(2)
            ],
            "break_right": [
                steave_sheet.get_image(frame_width, frame_height, 4, i, scale=scale_size)
                for i in range(3)
            ],
            "break_left": [
                steave_sheet.get_image(frame_width, frame_height, 5, i, scale=scale_size)
                for i in range(3)
            ],
            "idle_right": [
                steave_sheet.get_image(frame_width, frame_height, 6, 0, scale=scale_size)
            ],
            "idle_left": [
                steave_sheet.get_image(frame_width, frame_height, 7, 0, scale=scale_size)
            ],
        }

        self.state = "walk_right"
        self.frame = 0
        self.direction = "right"
        self.animation_speed = 0.15
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4
        self.on_ground = True
        self.inventory = []
        self.font = pygame.font.Font(None,40)
        self.block = 0
        self.chosen_block = 0
    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.frame = 0
    def is_on_ground(self,world):
        try:
            if world[int((self.rect.topleft[0]+block_size) // block_size)][int((self.rect.topleft[1]+block_size*2) // block_size)] != 0:
                return False
            else:
                return True
        except:
            return False

    def show_fast_inventory(self,screen,block_list):
        inventury_surface = pygame.Surface(
            (screen_width - screen_width / 3, screen_height * 0.05), pygame.SRCALPHA
        )
        inventury_surface.fill((255, 255, 255, 0))

        surface = pygame.Surface(
            (screen_width - screen_width / 3, screen_height * 0.05), pygame.SRCALPHA
        )
        surface.fill((255, 255, 255, 100))

        block_distance = (screen_width - screen_width / 3) / len(block_list)

        for i,block in block_list.items():

            size = block.rect.size
            pos_x = (self.chosen_block - 1) * block_distance
            pos_y = 5
            if int(i)==self.chosen_block:
                block_rect = pygame.Rect(pos_x, pos_y, size[0] + 10, size[1] + 10)
                pygame.draw.rect(inventury_surface, (255, 0, 0), block_rect)

            text = self.font.render(str(self.inventory.count(int(i))),True,(0,0,0))
            text_rect = text.get_rect(center=((int(i)-1)*block_distance+5+block_size,10))
            block_list[i].draw(inventury_surface,((int(i) - 1) * block_distance+5,10))
            inventury_surface.blit(text, text_rect)

        screen.blit(inventury_surface,(screen_width*0.15,screen_height-screen_height*0.1))
        screen.blit(surface,(screen_width*0.15,screen_height-screen_height*0.1))

    def show_inventory(self,screen):
        inventury_surface  =pygame.Surface((screen_width-screen_width/3,screen_height/1.67),pygame.SRCALPHA)
        inventury_surface.fill((255,255,255,200))
        screen.blit(inventury_surface,(screen_width / 2 - (screen_width - screen_width / 1.5),screen_height / 2 - (screen_height / 4)))
    def change_chosen_block(self,event):
        self.chosen_block += event.y
        self.block += event.y

        self.chosen_block %= 10
        self.block %=10
    def update(self, keys,world,screen):
        moving = False
        new_pos = list(self.rect.topleft)
        mouse_pos = pygame.mouse.get_pos()
        distance = math.sqrt((self.rect.x - mouse_pos[0]) ** 2 + (self.rect.y - mouse_pos[1]) ** 2)
        can_place_block = not world[int(mouse_pos[0] // block_size)][
            int(mouse_pos[1] // block_size)] and not self.rect.collidepoint(mouse_pos) and distance<block_size*4
        can_break_block = distance < block_size*4 and world[int(mouse_pos[0]//block_size)][int(mouse_pos[1]//block_size)]

        if keys[pygame.K_d]:
            self.set_state("walk_right")
            if not self.is_on_ground(world):
                new_pos[0] += self.speed
            else:
                new_pos[0] += self.speed * 0.75
            self.direction = "right"
            moving = True
        elif keys[pygame.K_a]:
            self.set_state("walk_left")
            if not self.is_on_ground(world):
                new_pos[0] -= self.speed
            else:
                new_pos[0] -= self.speed*0.75
            self.direction = "left"
            moving = True
        if not self.is_on_ground(world):
            if keys[pygame.K_SPACE]:
                if self.direction == "right":
                    self.set_state("jump_right")
                elif self.direction == "left":
                    self.set_state("jump_left")
                new_pos[1] -= block_size*1.5
                moving = True
        try:
            if self.direction == "left":
                if world[int((new_pos[0]+block_size*0.5)//block_size)][int(new_pos[1]//block_size)] == 0 and world[int((new_pos[0]+block_size*0.5)//block_size)][int((new_pos[1]+block_size)//block_size)] == 0:
                    self.rect.topleft = new_pos
            else:
                if world[int((new_pos[0]+block_size*1.5)//block_size)][int(new_pos[1]//block_size)] == 0 and world[int((new_pos[0]+block_size*1.5)//block_size)][int((new_pos[1]+block_size)//block_size)] == 0:
                    self.rect.topleft = new_pos
        except:
            pass
        for i in range (0,9):
            if 0<i<9:
                if keys[getattr(pygame,f'K_{i}')]:
                    self.chosen_block = i
                    self.block = i
        if keys[pygame.K_e]:
            if self.direction == "right":
                self.set_state("break_right")
            elif self.direction == "left":
                self.set_state("break_left")
            if can_break_block:
                self.inventory.append(world[int(mouse_pos[0]//block_size)][int(mouse_pos[1]//block_size)])
                world[int(mouse_pos[0]//block_size)][int(mouse_pos[1]//block_size)] = 0
                moving = True


        if keys[pygame.K_q]:
            #if self.direction == "right":
            #    self.set_state("break_right")
            #elif self.direction == "left":
            #    self.set_state("break_left")
            if self.block:
                if can_place_block:
                    if self.block in self.inventory:
                        self.inventory.remove(self.block)
                        world[int(mouse_pos[0]//block_size)][int(mouse_pos[1]//block_size)] = self.block
        if keys[pygame.K_TAB]:
            self.show_inventory(screen)
            print(" ".join(map(str,self.inventory)))
        if not moving:
            if self.state.startswith("walk_right") or self.state.startswith("break_right"):
                self.set_state("idle_right")
            elif self.state.startswith("walk_left") or self.state.startswith("break_left"):
                self.set_state("idle_left")

        if self.is_on_ground(world):
            self.rect.y += grawity

        self.frame += self.animation_speed
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0
            if self.state == "jump_right"or self.state == "jump_left":
                if self.direction == "right":
                    self.set_state("idle_right")
                else:
                    self.set_state("idle_left")
        self.image = self.animations[self.state][int(self.frame)]


    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Quit_button(Button):
    def __init__(self, image_name, pos, size, text,text_color=(0, 0, 0)):
        super().__init__(image_name, pos, size, text,text_color)
        self.show_menu = False

    def quit_menu(self,screen,font,text):
        if self.show_menu:
            quit_surface = pygame.Surface((screen_width-screen_width/3,screen_height/1.67),pygame.SRCALPHA)
            quit_surface.fill((255,255,255,200))
            message = font.render(text, True, (0, 0, 0))
            message_rect = message.get_rect(center=((quit_surface.get_width()/2,quit_surface.get_height()/2)))
            quit_surface.blit(message, message_rect)
            screen.blit(quit_surface,(screen_width / 2 - (screen_width - screen_width / 1.5), screen_height / 2 - (screen_height / 4)))