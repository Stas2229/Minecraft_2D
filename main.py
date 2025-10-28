import random
import pygame
import json
import os
from clases import*
from settings import screen_width,screen_height,info,world_width,world_height,clock,FPS

pygame.init()



def main():
    size = (info.current_w, info.current_h)
    x = 10
    y = 8
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Minecraft_2d")

    minecraft_main_text = Photo("images/minecraft_text_image.png", (size[0] / 3, size[1] / 4.5), (604, 103))

    main_play_button = Button("images/minecraft_button.png", (size[0] / 3, size[1] / 3), (640, 80), "Play")
    main_setting_button = Button("images/minecraft_button.png", (size[0] / 3, size[1] / 2.3), (640, 80), "Setting")

    quit_button = Quit_button("images/minecraft_button.png",(0,0),(50,50),"X",(225,0,0))

    game_menu_play_button = Button("images/minecraft_button.png",(size[0]/3,size[1]/3),(640,80),"Play no save")
    game_menu_return_button  =Button("images/minecraft_button.png",(0, 0),(50,50),"<--")
    world_1_button = Button("images/minecraft_button.png",(size[0]/3,size[1]/3+100),(640,80),"World 1")
    world_2_button = Button("images/minecraft_button.png", (size[0] / 3, (size[1] / 3)+200), (640, 80), "World 2")
    world_3_button = Button("images/minecraft_button.png", (size[0] / 3, (size[1] / 3)+300), (640, 80), "World 3")

    delete_1 = Button("images/minecraft_button.png",(size[0]/3+700,(size[1]/3)+100),(80,80),"Delete",text_color=(255,0,0))
    delete_2 = Button("images/minecraft_button.png", (size[0] / 3 + 700, (size[1] / 3)+200), (80, 80), "Delete",
                      text_color=(255, 0, 0))
    delete_3 = Button("images/minecraft_button.png", (size[0] / 3 + 700, (size[1] / 3)+300), (80, 80), "Delete",
                      text_color=(255, 0, 0))

    quit_menu_quit_button = Button("images/minecraft_button.png",(screen_width-screen_width/3.5, screen_height*0.735),(100,50),"Yes",(0,225,0))
    quit_menu_return_button  = Button("images/minecraft_button.png",(screen_width-screen_width*0.7, screen_height*0.735),(50,50),"No",(225,0,0))
    return_to_menu_button  =Button("images/minecraft_button.png",(((screen_width-screen_width/3.5)+(screen_width-screen_width*0.7))/2, screen_height*0.735),(100,50),"Menu")

    player = Player(x*block_size,y*block_size)

    minecraft_bg_1 = Background("images/minecraft_main_bg.png")
    minecraft_bg_2 = Background("images/minecraft_worlds_menu_bg.png")

    Dirt = Block("images/Dirt.png", block_size)
    Stone = Block("images/Stone.png", block_size)
    Leaf = Block("images/Leaf.png", block_size)
    Wood = Block("images/Wood.png", block_size)
    Grass = Block("images/Grass.png", block_size)
    Coal = Block("images/Coal.png", block_size)
    Iron = Block("images/Iron.png", block_size)
    Diamond  = Block("images/Diamond.png", block_size)
    block_list = {
        "1": Grass,
        "2": Dirt,
        "3": Stone,
        "4": Wood,
        "5": Leaf,
        "6": Coal,
        "7": Iron,
        "8": Diamond
    }
    running = True
    game_run = False
    show_quit_menu = False
    stop = False
    current_screen = "Menu"
    whitch_world = 1
    world = ""
    button_font = pygame.font.Font(None, 32)
    quit_font  =pygame.font.Font(None,40)
    quit_text  ="Want to leave?"
    Blocks = [0,1,2,3,4,5,6,7,8]
    menues = {
        "Menu": {
            "bg": minecraft_bg_1.image
        },
        "Worlds_menu": {
            "bg": minecraft_bg_2.image
        }
    }

    def generate_world():
        world = [[Blocks[0] for _ in range(world_height)] for _ in  range(world_width)]

        surface_heights = []
        base_height = world_height // 2

        for x in range(world_width):
            offset = random.randint(-2,0)
            height = base_height + offset
            surface_heights.append(height)

            for y in range(world_height):
                if y < height:
                    world[x][y]=Blocks[0]
                elif y == height:
                    world[x][y] = Blocks[1]
                elif y > height +3:
                    if random.random()<0.15:
                        world[x][y] = Blocks[6]
                    elif random.random()<0.06:
                        world[x][y] = Blocks[7]
                    elif random.random()<0.02:
                        world[x][y] = Blocks[8]
                    else:
                        world[x][y] = Blocks[3]
                else:
                    world[x][y] = Blocks[2]
        for x in range(world_width):
            if random.random()<0.1:
                h = surface_heights[x]
                if h > 2 and h < world_height - 6:
                    for i in range(3):
                        world[x][h-i] = Blocks[4]
                    for dx in [-1,0,1]:
                        for dy in [-3,-4]:
                            if 0 <= x+dx < world_width:
                                world[x+dx][h+dy] = Blocks[5]


        return  world

    def save_world(world,whitch_world):
        if whitch_world !=0:
            world_file = f'worlds/world_{str(whitch_world)}.json'
            with open(world_file,'w',encoding="utf-8") as f:
                json.dump(world,f)
    def delete_world(whitch_world):
        try:
            os.remove(whitch_world)
        except FileNotFoundError:
            pass

    while running:
        clock.tick(FPS)

        if current_screen == "Menu":

            screen.blit(menues[current_screen]["bg"], (0, 0))
            minecraft_main_text.draw(screen)
            main_play_button.draw(button_font, screen)
            #main_setting_button.draw(button_font, screen)
            quit_button.draw(button_font,screen)
            quit_button.quit_menu(screen,quit_font,quit_text)

            if quit_button.show_menu:
                quit_menu_quit_button.draw(button_font,screen)
                quit_menu_return_button.draw(button_font,screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if quit_button.show_menu:
                            if quit_menu_quit_button.is_click(mouse_pos):
                                running = False
                            elif quit_menu_return_button.is_click(mouse_pos):
                                stop = False
                                quit_button.show_menu = False

                        if not stop:
                            if main_play_button.is_click(mouse_pos):
                                current_screen = "Worlds_menu"
                            #elif main_setting_button.is_click(mouse_pos):
                            #    current_screen = "Settings"
                            elif quit_button.is_click(mouse_pos):
                                stop = True
                                quit_button.show_menu  =True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if quit_button.show_menu:
                            stop = False
                            quit_button.show_menu = False
                        else:
                            stop = True
                            quit_button.show_menu = True

        elif current_screen == "Worlds_menu":
            screen.blit(menues[current_screen]["bg"], (0, 0))
            game_menu_play_button.draw(button_font,screen)
            game_menu_return_button.draw(button_font,screen)
            world_1_button.draw(button_font,screen)
            world_2_button.draw(button_font, screen)
            world_3_button.draw(button_font, screen)
            delete_1.draw(button_font,screen)
            delete_2.draw(button_font,screen)
            delete_3.draw(button_font,screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if game_menu_play_button.is_click(mouse_pos):

                            if os.path.exists("worlds/world.json"):
                                with open("worlds/world.json", "r") as f:
                                    world = json.load(f)
                            else:
                                world = generate_world()
                            whitch_world = 0
                            current_screen = "Game"

                        elif world_1_button.is_click(mouse_pos):
                            if os.path.exists("worlds/world_1.json"):
                                with open("worlds/world_1.json", "r") as f:
                                    world = json.load(f)
                            else:
                                world = generate_world()
                            whitch_world = 1
                            current_screen = "Game"

                        elif world_2_button.is_click(mouse_pos):
                            if os.path.exists("worlds/world_2.json"):
                                with open("worlds/world_2.json", "r") as f:
                                    world = json.load(f)
                            else:
                                world = generate_world()
                            whitch_world = 2
                            current_screen = "Game"

                        elif world_3_button.is_click(mouse_pos):
                            if os.path.exists("worlds/world_3.json"):
                                with open("worlds/world_3.json", "r") as f:
                                    world = json.load(f)
                            else:
                                world = generate_world()
                            whitch_world = 3
                            current_screen = "Game"

                        elif delete_1.is_click(mouse_pos):
                            delete_world("worlds/world_1.json")
                        elif delete_2.is_click(mouse_pos):
                            delete_world("worlds/world_2.json")
                        elif delete_3.is_click(mouse_pos):
                            delete_world("worlds/world_3.json")

                        elif game_menu_return_button.is_click(mouse_pos):
                            current_screen = "Menu"

        elif current_screen == "Game":
            screen.fill((135, 206, 235))
            keys = pygame.key.get_pressed()
            for x in range(world_width):
                for y in range(world_height):
                    tile = world[x][y]
                    if tile != 0:
                        block_list[str(tile)].draw(screen,(x*block_size,y*block_size))

            player.show_fast_inventory(screen, block_list)
            player.draw(screen)
            player.update(keys, world, screen)

            quit_button.draw(button_font, screen)
            quit_button.quit_menu(screen, quit_font, quit_text)
            if quit_button.show_menu:
                quit_menu_quit_button.draw(button_font, screen)
                quit_menu_return_button.draw(button_font, screen)
                return_to_menu_button.draw(button_font, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    player.change_chosen_block(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if quit_button.show_menu:
                            if quit_menu_quit_button.is_click(mouse_pos):
                                running = False
                                save_world(world,whitch_world)
                            if quit_menu_return_button.is_click(mouse_pos):
                                stop = False
                                quit_button.show_menu = False
                            if return_to_menu_button.is_click(mouse_pos):
                                current_screen = "Worlds_menu"
                                quit_button.show_menu = False
                                stop = False
                                save_world(world, whitch_world)

                        if not quit_button.show_menu:
                            if quit_button.is_click(mouse_pos):
                                stop = True
                                quit_button.show_menu = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if quit_button.show_menu:
                            stop = False
                            quit_button.show_menu = False
                        else:
                            stop = True
                            quit_button.show_menu = True


        if current_screen == "Game":
            save_world(world, whitch_world)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

