import pygame
import sys
import os
import random
import math
import time
import json

pygame.init()
WIDTH, HEIGHT = SIZE = 800, 600
screen = pygame.display.set_mode(SIZE)
# FPS = 60
# WIDTH, HEIGHT = SIZE = 800, 600
# PLAYER_SPEED = 10
# ENEMY_SPEED = 8
# SPELL_SPEED = 70
# POINT_MULTIPLY = 10
# DAMAGE_MULTIPLY = 1

def update_music():
    global music_queue, UPDATE_MUSIC_QUEUE
    music_list = [f"media/{i}.mp3" for i in range(9)]
    if not music_queue:
        music_queue = music_list.copy()
        random.shuffle(music_queue)
    current_music = music_queue.pop()
    pygame.mixer.music.load(current_music)
    print(f"{current_music} is playing now")
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(UPDATE_MUSIC_QUEUE)

def load_image(name, path='data', colorkey=None):
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def main_menu():
    pygame.mixer.music.load('main.mp3')
    pygame.mixer.music.play(-1)
    
    background = pygame.transform.scale(load_image('background.png', 'sprites'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    
    start_button = Button(menu_buttons)
    start_button.image = pygame.transform.scale(load_image('start_text.png', 'sprites'), (300, 100))
    start_button.rect = start_button.image.get_rect()
    start_button.rect = start_button.rect.move(250, 220)
    shop_button = Button(menu_buttons) # MUTATIONS
    shop_button.image = pygame.transform.scale(load_image('shop_text.png', 'sprites'), (300, 100))
    shop_button.rect = shop_button.image.get_rect()
    shop_button.rect = shop_button.rect.move(250, 370)
    running = True
    menu_buttons.draw(screen)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    for sprite in menu_buttons:
                        all_sprites.remove(sprite)
                    return
                if shop_button.rect.collidepoint(event.pos):
                    for sprite in menu_buttons:
                        all_sprites.remove(sprite)
                    mutations_menu()
        pygame.display.flip()
    
def pause_menu():
    global time_count, pause_time_start
    background = pygame.transform.scale(load_image('lvl_up_menu.png', 'sprites'), (400, 500))
    pause_menu_group = pygame.sprite.Group()
    bg_group = pygame.sprite.Group()
    menu = pygame.sprite.Sprite(bg_group)
    menu.image = background
    menu.image.set_alpha(240)
    menu.rect = background.get_rect().move(200, 50)
    
    button1 = Button(pause_menu_group)
    button1.rect = pygame.Rect(240, 142, 312, 92)
    button2 = Button(pause_menu_group)
    button2.rect = pygame.Rect(240, 275, 312, 88)
    button3 = Button(pause_menu_group)
    button3.rect = pygame.Rect(240, 398, 312, 88)
    
    bg_group.draw(screen)
    pause_menu_group.draw(screen)
    buttons_text = ['Continue', 'Switch sound', 'Exit']
    coords = [142, 275, 398]
    for i in range(3):
        font = pygame.font.Font(None, 40)
        text = font.render(buttons_text[i], True, 'white')
        text_x = 240 + 156 - text.get_width() // 2
        text_y = coords[i] + 45 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
    
    running = True
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                for sprite in pause_menu_group.sprites():
                    sprite.kill()
                running = False
                time_count += (time.time() - pause_time_start)
            if event.type == UPDATE_MUSIC_QUEUE:
                update_music()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.rect.collidepoint(event.pos):
                    for sprite in pause_menu_group.sprites():
                        sprite.kill()
                    running = False
                    time_count += (time.time() - pause_time_start)
                if button2.rect.collidepoint(event.pos):
                    if pygame.mixer.music.get_volume():
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.3)
                if button3.rect.collidepoint(event.pos):
                    for sprite in all_sprites.sprites():
                        sprite.kill()
                    main()
                    
def level_up_menu():
    global time_count, pause_time_start
    background = pygame.transform.scale(load_image('lvl_up_menu.png', 'sprites'), (400, 500))
    level_up_menu_group = pygame.sprite.Group()
    menu = pygame.sprite.Sprite(level_up_menu_group)
    menu.image = background
    menu.image.set_alpha(240)
    menu.rect = background.get_rect().move(200, 50)
    running = True
    
    button1 = Button(level_up_menu_group)
    # button1.image = pygame.transform.scale(button1.image, (312, 92))
    button1.rect = pygame.Rect(240, 142, 312, 92)
    button2 = Button(level_up_menu_group)
    # button2.image = pygame.transform.scale(button1.image, (312, 88))
    button2.rect = pygame.Rect(240, 275, 312, 88)
    button3 = Button(level_up_menu_group)
    # button3.image = pygame.transform.scale(button1.image, (316, 88))
    button3.rect = pygame.Rect(240, 398, 312, 88)
    current_upgrades = random_upgrade_choice()
    if not current_upgrades:
        hero.max_level = True
        for sprite in level_up_menu_group:
            sprite.kill()
        return
    if len(current_upgrades) < 3:
        hero.upgrades[random.choice(current_upgrades)][2]()
        for sprite in level_up_menu_group:
            sprite.kill()
        return
    
    level_up_menu_group.draw(screen)
    coords = [142, 275, 398]
    for i in range(3):
        font = pygame.font.Font(None, 40)
        text = font.render(current_upgrades[i], True, 'white')
        text_x = 240 + 156 - text.get_width() // 2
        text_y = coords[i] + 45 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
    
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == UPDATE_MUSIC_QUEUE:
                update_music()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.rect.collidepoint(event.pos):
                    for sprite in level_up_menu_group:
                        sprite.kill()
                    hero.upgrades[current_upgrades[0]][2]()
                    running = False
                    time_count += (time.time() - pause_time_start)
                if button2.rect.collidepoint(event.pos):
                    for sprite in level_up_menu_group:
                        sprite.kill()
                    hero.upgrades[current_upgrades[1]][2]()
                    running = False
                    time_count += (time.time() - pause_time_start)
                if button3.rect.collidepoint(event.pos):
                    for sprite in level_up_menu_group:
                        sprite.kill()
                    hero.upgrades[current_upgrades[2]][2]()
                    running = False
                    time_count += (time.time() - pause_time_start)

def draw_mutations_menu():    
    prices = [457, 2000, 4000, 10_000]
    status = {0: "available", 1:"selected"}
    data = json.load(open("data.json"))
    availability_status = data["mutations_inventory"]
    
    font = pygame.font.Font(None, 30)
    text = font.render("EXIT", True, 'white')
    screen.blit(text, (40, 25))
    font = pygame.font.Font(None, 30)
    text = font.render(str(prices[0]) + '$' if availability_status[0] == -1 else
                       status[availability_status[0]], True, 'white')
    screen.blit(text, (205, 70))
    font = pygame.font.Font(None, 40)
    text = font.render("Chill guy", True, 'white')
    screen.blit(text, (190, 120))
    font = pygame.font.Font(None, 30)
    text = font.render("Just a chill guy", True, 'white')
    screen.blit(text, (175, 210))


    font = pygame.font.Font(None, 30)
    text = font.render(str(prices[1]) + '$'if availability_status[1] == -1 else
                       status[availability_status[1]], True, 'white')
    screen.blit(text, (520, 70))
    font = pygame.font.Font(None, 40)
    text = font.render(f"Collector", True, 'white')
    screen.blit(text, (490, 120))
    font = pygame.font.Font(None, 30)
    text = font.render(f"+15% xp", True, 'white')
    screen.blit(text, (510, 210))
    
    font = pygame.font.Font(None, 30)
    text = font.render(str(prices[2]) + '$' if availability_status[2] == -1 else
                       status[availability_status[2]], True, 'white')
    screen.blit(text, (220, 310))
    font = pygame.font.Font(None, 40)
    text = font.render(f"Warrior", True, 'white')
    screen.blit(text, (200, 360))
    font = pygame.font.Font(None, 30)
    text = font.render(f"+20% damage", True, 'white')
    screen.blit(text, (180, 440))

    font = pygame.font.Font(None, 30)
    text = font.render(str(prices[3]) + '$' if availability_status[3] == -1 else
                       status[availability_status[3]], True, 'white')
    screen.blit(text, (515, 310))
    font = pygame.font.Font(None, 40)
    text = font.render(f"Absolute", True, 'white')
    screen.blit(text, (490, 360))
    font = pygame.font.Font(None, 25)
    text = font.render(f"+1 max spell level", True, 'white')
    screen.blit(text, (475, 440))
    
    font = pygame.font.Font(None, 40)
    text = font.render(str(data['balance']) + '$', True, 'white')
    screen.blit(text, (700, 10))
    
    pygame.display.flip()

def mutations_menu():
    pygame.mixer.music.stop()
    data = json.load(open('data.json'))
    mutations_menu_group = pygame.sprite.Group()
    screen.fill('black')
    image = pygame.transform.scale(load_image('mutation_button.png', 'sprites'), (160, 200))
    exit_button = Button(mutations_menu_group)
    exit_button.image = pygame.transform.scale(image, (70, 40))
    exit_button.rect = image.get_rect().move(30, 15)
    chill_guy_button = Button(mutations_menu_group)
    chill_guy_button.image = image
    chill_guy_button.rect = image.get_rect().move(170, 60)
    collector_button = Button(mutations_menu_group)
    collector_button.image = image
    collector_button.rect = image.get_rect().move(470, 60)
    warrior_button = Button(mutations_menu_group)
    warrior_button.image = image
    warrior_button.rect = image.get_rect().move(170, 300)
    absolute_button = Button(mutations_menu_group)
    absolute_button.image = image
    absolute_button.rect = image.get_rect().move(470, 300)
    mutations_menu_group.draw(screen)
    
    draw_mutations_menu()
    
    prices = [457, 2000, 4000, 10_000]
    availability_status = data["mutations_inventory"]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.rect.collidepoint(event.pos):
                    running = False
                    main()
                if chill_guy_button.rect.collidepoint(event.pos) and availability_status[0] != 1:
                    answer = accept_menu()
                    if answer and not availability_status[0]:
                        availability_status[availability_status.index(1)] = 0
                        availability_status[0] = 1
                        data["mutations_inventory"] = availability_status
                        json.dump(data, open('data.json', 'w'), indent=4)
                if collector_button.rect.collidepoint(event.pos) and availability_status[1] != 1:
                    answer = accept_menu()
                    if answer and not availability_status[1]:
                        availability_status[availability_status.index(1)] = 0
                        availability_status[1] = 1
                    if answer and availability_status[1] == -1:
                        if data['balance'] >= prices[1]:
                            data['balance'] -= prices[1]
                            availability_status[availability_status.index(1)] = 0
                            availability_status[1] = 1
                        else:
                            pass
                    data["mutations_inventory"] = availability_status
                    json.dump(data, open('data.json', 'w'), indent=4)
                if warrior_button.rect.collidepoint(event.pos) and availability_status[2] != 1:
                    answer = accept_menu()
                    if answer and not availability_status[2]:
                        availability_status[availability_status.index(1)] = 0
                        availability_status[2] = 1
                    if answer and availability_status[2] == -1:
                        if data['balance'] >= prices[2]:
                            data['balance'] -= prices[2]
                            availability_status[availability_status.index(1)] = 0
                            availability_status[2] = 1                            
                        else:
                            pass
                    data["mutations_inventory"] = availability_status
                    json.dump(data, open('data.json', 'w'), indent=4)
                if absolute_button.rect.collidepoint(event.pos) and availability_status[3] != 1:
                    answer = accept_menu()
                    if answer and not availability_status[3]:
                        availability_status[availability_status.index(1)] = 0
                        availability_status[3] = 1
                    if answer and availability_status[3] == -1:
                        if data['balance'] >= prices[3]:
                            data['balance'] -= prices[3]
                            availability_status[availability_status.index(1)] = 0
                            availability_status[3] = 1
                        else:
                            pass
                    data["mutations_inventory"] = availability_status
                    json.dump(data, open('data.json', 'w'), indent=4)
            screen.fill('black')
            all_sprites.draw(screen)
            draw_mutations_menu()
            pygame.display.flip()


def accept_menu():
    accept_buttons_group = pygame.sprite.Group()
    accept_bg = pygame.sprite.Group()
    background = pygame.sprite.Sprite(all_sprites, accept_bg)
    background.image = load_image("accept_bg.png", 'sprites')
    background.rect = background.image.get_rect().move(200, 100)
    
    yes_button = pygame.sprite.Sprite(all_sprites, accept_buttons_group)
    yes_button.image = load_image('accept_button.png', 'sprites')
    yes_button.rect = yes_button.image.get_rect().move(250, 300)
    
    no_button = pygame.sprite.Sprite(all_sprites, accept_buttons_group)
    no_button.image = load_image('accept_button.png', 'sprites')
    no_button.rect = yes_button.image.get_rect().move(450, 300)
    accept_bg.draw(screen)
    accept_buttons_group.draw(screen)
    
    font = pygame.font.Font(None, 50)
    text = font.render("Are you sure?", True, 'white')
    screen.blit(text, (280, 150))
    font = pygame.font.Font(None, 50)
    text = font.render("YES", True, 'white')
    screen.blit(text, (265, 305))
    font = pygame.font.Font(None, 50)
    text = font.render("NO", True, 'white')
    screen.blit(text, (475, 305))
    
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                for sprite in accept_buttons_group:
                    sprite.kill()
                background.kill()
                screen.fill('black')
                all_sprites.draw(screen)
                draw_mutations_menu()
                pygame.display.flip()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.rect.collidepoint(event.pos):
                    running = False
                    for sprite in accept_buttons_group:
                        sprite.kill()
                    background.kill()
                    screen.fill('black')
                    all_sprites.draw(screen)
                    draw_mutations_menu()
                    pygame.display.flip()
                    return True
                if no_button.rect.collidepoint(event.pos):
                    running = False
                    for sprite in accept_buttons_group:
                        sprite.kill()
                    background.kill()
                    screen.fill('black')
                    all_sprites.draw(screen)
                    draw_mutations_menu()
                    pygame.display.flip()
                    return False

def lose_screen():
    global end_game_reward, enemies_killed
    pygame.mixer.music.load('game_over.mp3')
    pygame.mixer.music.play()
    bg_screen_group = pygame.sprite.Group()
    bg_screen = pygame.sprite.Sprite(bg_screen_group)
    bg_screen.image = pygame.transform.scale(load_image('game_over.png', 'sprites'), (800, 600))
    bg_screen.rect = bg_screen.image.get_rect()
    bg_screen_group.draw(screen)

    data = json.load(open("data.json"))
    font = pygame.font.Font(None, 40)
    text = font.render('You earned', True, 'white')
    screen.blit(text, (310, 520))
    text = font.render(str(int(end_game_reward)) + '$', True, 'white')
    screen.blit(text, (370, 560))
    text = font.render(f"You've killed {enemies_killed} enemies", True, 'white')
    screen.blit(text, (230, 470))
    data['balance'] += int(end_game_reward)
    
    json.dump(data, open("data.json", 'w'), indent=4)
    
    pygame.display.flip()
    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if time.time() - start_time > 271:
                running = False
    main()

def terminate():
    pygame.quit()
    sys.exit()

def update_progress_bar():
    progress_bar.rect.x = 150
    progress_bar.rect.y = 32
    progress_bar_frame.rect.x = 110
    progress_bar_frame.rect.y = 20
    if hero.max_level:
        progress_bar.image = pygame.transform.scale(progress_image, (500, 15))
        return
    if not hero.xp:
        length = 0
    else:
        length = hero.xp / hero.aim_xp * 500
        while hero.xp >= hero.aim_xp:
            hero.current_level += 1
            hero.xp -= hero.aim_xp
            hero.aim_xp += 3 * hero.current_level
    
            progress_bar.image = pygame.transform.scale(progress_image, (500, 15))
            draw_sprites()
            global pause_time_start
            pause_time_start = time.time()
            level_up_menu()
    progress_bar.image = pygame.transform.scale(progress_image, (length, 15))

def draw_sprites():
    screen.fill('black')
    background = pygame.transform.scale(load_image('background.png', 'sprites'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    enemy_group.draw(screen)
    priority_spell_group.draw(screen)
    static_group.draw(screen)
    super_priority_group.draw(screen)
    show_timer()
    show_hp()
    pygame.display.flip()

def random_upgrade_choice():
    avaible_upgrades = [upgrade for upgrade in hero.upgrades.keys() if
                        hero.upgrades[upgrade][0] != hero.upgrades[upgrade][1]]
    current_upgrades = random.sample(avaible_upgrades, min(3, len(avaible_upgrades)))
    return current_upgrades
    
def show_timer():
    font = pygame.font.Font(None, 40)
    seconds = int(time.time() - time_count)
    text = font.render(f"{seconds // 60:02}:{seconds % 60:02}", True, 'white')
    screen.blit(text, (10, 25))
    
def show_hp():
    font = pygame.font.Font(None, 40)
    text = font.render(f"{hero.hp} hp", True, 'white')
    screen.blit(text, (10, 55))

def spawn_enemy(time):
    global ENEMY_SPEED
    spawn_rules = {
        0: ((100, 0, 0, 0, 0, 0), 2000),
        60: ((80, 20, 0, 0, 0, 0), 1000),
        180: ((50, 20, 30, 0, 0, 0), 600),
        300: ((20, 20, 30, 30, 0, 0), 400),
        480: ((0, 5, 30, 50, 15, 0), 300),
        600: ((0, 0, 10, 39, 50, 1), 200)
        }
    time_level = max([x for x in spawn_rules.keys() if x <= time])
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, spawn_rules[time_level][1])
    # print(time_level)
    if time > 600:
        ENEMY_SPEED = 7 + 0.015 * (time - 600)
    chances = spawn_rules[time_level][0]
    enemy_lvl = 0
    chance_value = 0
    enemy_lvl_value = random.randint(1, 100)
    while chance_value < enemy_lvl_value:
        chance_value += chances[enemy_lvl]
        enemy_lvl += 1
    enemy_lvl -= 1
    
    t = random.randint(0, 1)
    if t:
        x = random.choice([random.randint(-400, -100), random.randint(900, 1300)])
        y = random.randint(-400, 1300)
    else:
        x = random.randint(-400, 1300)
        y = random.choice([random.randint(-400, -100), random.randint(900, 1300)])
    Enemy(x, y, enemy_lvl)
    

def clear_rubbish():
    for sprite in all_sprites:
        if abs(sprite.rect.x - hero.rect.x) > 5_000 or abs(sprite.rect.y - hero.rect.y) > 5_000:
            sprite.kill()
            
def spawn_point(time):
    spawn_rules = {
        0: ((100, 0, 0, 0, 0, 0), 6000),
        60: ((90, 10, 0, 0, 0, 0), 3000),
        240: ((70, 29, 1, 0, 0, 0), 2400),
        480: ((65, 31, 3, 1, 0, 0), 1600),
        }
    
    time_level = max([x for x in spawn_rules.keys() if x <= time])
    pygame.time.set_timer(POINT_SPAWN_EVENT, spawn_rules[time_level][1])
    
    chances = spawn_rules[time_level][0]
    point_lvl = 0
    chance_value = 0
    point_lvl_value = random.randint(1, 100)
    while chance_value < point_lvl_value:
        chance_value += chances[point_lvl]
        point_lvl += 1
    point_lvl -= 1
    
    x = random.randint(-400, 1300)
    y = random.randint(-400, 1300)
    XpPoint(x, y, point_lvl)


class StaticGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        
    def move(self, x, y):
        for sprite in self.sprites():
            sprite.rect = sprite.rect.move(x, y)


class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups):
        super().__init__(all_sprites, player_group, *groups)
        self.image = load_image('player1.png', 'sprites')
        self.rect = self.image.get_rect()
        self.xp = 0
        self.aim_xp = 100
        self.hp = 100
        self.current_level = 1
        self.rage_mode_is_active = False
        self.rage_mode = None
        self.max_level = False
        
        self.upgrades = {
            "Laser": (0, 6, self.upgrade_laser),
            "Bullet": (0, 6, self.upgrade_bullet),
            "Cleaving spear": (0, 6, self.upgrade_cleaving_blade),
            "Laser field": (0, 6, self.upgrade_laser_field),
            "Earthquake": (0, 6, self.upgrade_earthquake),
            "Extermination": (0, 6, self.upgrade_extermination),
            "Tornado": (0, 6, self.upgrade_tornado),
            "Rage mode": (0, 6, self.upgrade_rage_mode),
            "Magic amplification": (1, 4, self.upgrade_magic_amplification),
            "Movement speed": (1, 4, self.upgrade_movement_speed),
            "Xp obtaining": (1, 4, self.upgrade_xp_obtaining)
        }
    
    def update_field(self, dx, dy):
        for sprite in all_sprites:
            sprite.rect.x += dx
            sprite.rect.y += dy
        
    
    def chechk_for_picking_point(self):
        if (sprites := pygame.sprite.spritecollide(self, points_group, 1)):
            for sprite in sprites:
                self.xp += sprite.xp[sprite.point_level] * POINT_MULTIPLY
                
    def upgrade_laser(self):
        if not self.upgrades["Laser"][0]:
            self.laser = Laser(0)
        else:
            self.laser.spell_level += 1
        self.upgrades["Laser"] = (self.upgrades["Laser"][0] + 1,) + (self.upgrades["Laser"][1:])
            
    
    def upgrade_bullet(self):
        if not self.upgrades["Bullet"][0]:
            pygame.time.set_timer(KNIFE_THROWING, 800)
            self.bullet_level = 0
        else:
            self.bullet_level += 1
        self.upgrades["Bullet"] = (self.upgrades["Bullet"][0] + 1,) + (self.upgrades["Bullet"][1:])
    
    def upgrade_cleaving_blade(self):
        if not self.upgrades["Cleaving spear"][0]:
            pygame.time.set_timer(CLEAVING_SPEAR_THROWING, 1100)
            self.cleaving_spear_level = 0
        else:
            self.cleaving_spear_level += 1
        self.upgrades["Cleaving spear"] = (self.upgrades["Cleaving spear"][0] + 1,) +\
            (self.upgrades["Cleaving spear"][1:])
    
    def upgrade_laser_field(self):
        if not self.upgrades["Laser field"][0]:
            self.laser_field = LaserField(0, priority_spell_group)
        else:
            self.laser_field.spell_level += 1
        self.upgrades["Laser field"] = (self.upgrades["Laser field"][0] + 1,) +\
            (self.upgrades["Laser field"][1:])
    
    def upgrade_earthquake(self):
        if not self.upgrades["Earthquake"][0]:
            pygame.time.set_timer(EARTHQUAKE_SPAWN, 2000)
        self.upgrades["Earthquake"] = (self.upgrades["Earthquake"][0] + 1,) + (self.upgrades["Earthquake"][1:])
    
    def upgrade_extermination(self):
        self.upgrades["Extermination"] = (self.upgrades["Extermination"][0] + 1,) +\
            (self.upgrades["Extermination"][1:])
        pygame.time.set_timer(EXTERMINATION_SPAWN, Extermination.lvl_cooldown[self.upgrades["Extermination"][0]] * 1000)
    
    def upgrade_tornado(self):
        if not self.upgrades["Tornado"][0]:
             pygame.time.set_timer(TORNADO_SPAWN, 2400)
        self.upgrades["Tornado"] = (self.upgrades["Tornado"][0] + 1,) + (self.upgrades["Tornado"][1:])
    
    def upgrade_rage_mode(self):
        self.upgrades["Rage mode"] = (self.upgrades["Rage mode"][0] + 1,) + (self.upgrades["Rage mode"][1:])
        pygame.time.set_timer(RAGE_MODE_ENABLE, RageMode.lvl_cooldown[self.upgrades["Rage mode"][0]] * 1000)
        
    
    def upgrade_magic_amplification(self):
        global DAMAGE_MULTIPLY
        DAMAGE_MULTIPLY *= 1.08
        self.upgrades["Magic amplification"] = (self.upgrades["Magic amplification"][0] + 1,) +\
            (self.upgrades["Magic amplification"][1:])
    
    def upgrade_movement_speed(self):
        global PLAYER_SPEED
        PLAYER_SPEED = PLAYER_SPEED * 1.05
        self.upgrades["Movement speed"] = (self.upgrades["Movement speed"][0] + 1,) +\
            (self.upgrades["Movement speed"][1:])
    
    def upgrade_xp_obtaining(self):
        global POINT_MULTIPLY
        POINT_MULTIPLY *= 1.07
        self.upgrades["Xp obtaining"] = (self.upgrades["Xp obtaining"][0] + 1,) +\
            (self.upgrades["Xp obtaining"][1:])
            
        
class ChillGuy(Player):
    afk_image = load_image('player/chill_guy/afk.png', 'sprites')
    right_image = load_image('player/chill_guy/right.png', 'sprites')
    left_image = load_image('player/chill_guy/left.png', 'sprites')
    
    def __init__(self, *groups):
        super().__init__(*groups)


class Collector(Player):
    afk_image = load_image('player/collector/afk.png', 'sprites')
    right_image = load_image('player/collector/right.png', 'sprites')
    left_image = load_image('player/collector/left.png', 'sprites')
    
    def __init__(self, *groups):
        super().__init__(*groups)
        global POINT_MULTIPLY
        POINT_MULTIPLY *= 1.15
        
        
class Warrior(Player):
    afk_image = load_image('player/warrior/afk.png', 'sprites')
    right_image = load_image('player/warrior/right.png', 'sprites')
    left_image = load_image('player/warrior/left.png', 'sprites')
    
    def __init__(self, *groups):
        super().__init__(*groups)
        global DAMAGE_MULTIPLY
        DAMAGE_MULTIPLY *= 1.2
        

class Absolute(Player):
    afk_image = load_image('player/absolute/afk.png', 'sprites')
    right_image = load_image('player/absolute/right.png', 'sprites')
    left_image = load_image('player/absolute/left.png', 'sprites')
    
    def __init__(self, *groups):
        super().__init__(*groups)
        for spell, stats in self.upgrades.items():
            self.upgrades[spell] = (stats[0], stats[1] + 1, stats[2])
            
# Сквозные пули - CleavingSpear
# Поле вокруг героя - Laser field
# Лазер-присоска - Laser
# Торнадо - Tornado
# Тотальная аннигиляция - Extermination
# Магический круг - Magic Circle
# Статичное поле с уроном - Earthquake
class Spell(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(all_sprites, *groups)
        self.image = load_image('test_spell.png', 'sprites')
        self.rect = self.image.get_rect()
        self.spell_level = 0
    
    def change_image(self, image_name): 
        self.image = load_image(image_name, 'sprites')
    
    def find_closest_enemy():
        correct_enemies = [enemy for enemy in enemy_group.sprites() if 0 < enemy.rect.x < 800 and 0 < enemy.rect.y < 600]
        if not correct_enemies:
            return
        closest_enemy = min(correct_enemies, key=lambda enemy:
            ((hero.rect.x - enemy.rect.x) ** 2 + (hero.rect.y - enemy.rect.y) ** 2) ** 0.5)
        return closest_enemy
    
            
class Button(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(all_sprites, *groups)
        self.image = load_image('test_button.png', 'sprites')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (312, 88))
        

class Enemy(pygame.sprite.Sprite):
    enemies_health = {0: 5, 1: 2, 2: 20, 3: 35, 4:55, 5:500}
    enemies_frames = {
        0: 4,
        1: 10,
        2: 6,
        3: 6,
        4: 10,
        5: 10,
        }
    kill_reward = {0: 2, 1: 3, 2: 5, 3: 6, 4: 8, 5: 30}
    enemy_damage = {0: 2, 1: 5, 2: 4, 3: 8, 4: 10, 5: 10}
    
    def __init__(self, x, y, enemy_lvl, *groups):
        super().__init__(all_sprites, enemy_group, *groups)
        self.frame = 0
        self.enemy_level = enemy_lvl
        self.image = load_image(f'enemies/enemy{self.enemy_level}/{self.frame}.png', 'sprites')
        self.rect = self.image.get_rect().move(x, y)
        self.hp = Enemy.enemies_health[enemy_lvl]
        self.damage = Enemy.enemy_damage[enemy_lvl]
    
    def update(self, *args):
        if args and args[0].type == MOVE:
            self.frame = (self.frame + 1) % (self.enemies_frames[self.enemy_level] * 2)
            self.image = load_image(f'enemies/enemy{self.enemy_level}/{self.frame // 2}.png', 'sprites')
            x = self.rect.x - hero.rect.x
            y = self.rect.y - hero.rect.y
            s = (x ** 2 + y ** 2) ** 0.5
            if s:
                self.rect = self.rect.move(-ENEMY_SPEED * x / s + random.randint(-3, 3),
                                           -ENEMY_SPEED * y / s + random.randint(-3, 3))
    
    def kill(self):
        global end_game_reward, enemies_killed
        money_reward = {0: 0.4, 1: 0.6, 2:0.8, 3:1, 4:1.2, 5:10}
        if random.randint(1, 5) == 1:
            XpPoint(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2,
                       self.enemy_level % 2)
        hero.xp += self.kill_reward[self.enemy_level] * POINT_MULTIPLY
        end_game_reward += money_reward[self.enemy_level]
        enemies_killed += 1
        super().kill()

class XpPoint(pygame.sprite.Sprite):
    xp = {
        0: 20,
        1: 50,
        2: 200,
        3: 400
    }
    
    def __init__(self, x, y, point_level, *groups):
        super().__init__(all_sprites, points_group, *groups)
        self.image = load_image(f'point{point_level}.png', 'sprites')
        self.rect = self.image.get_rect().move(x, y)
        self.point_level = point_level


class Bullet(Spell):
    lvl_damage = {
        0: 5,
        1: 7,
        2: 9,
        3: 15,
        4: 20,
        5: 25,
        6: 45,
    }
    
    def __init__(self, level, *groups):
        super().__init__(*groups)
        self.spell_level = level
        
        closest_enemy = Spell.find_closest_enemy()
        x = (closest_enemy.rect.x + closest_enemy.rect.width // 2) - (hero.rect.x + hero.rect.width // 2)
        y = (closest_enemy.rect.y + closest_enemy.rect.height // 2) - (hero.rect.y + hero.rect.height // 2)
        s = (x ** 2 + y ** 2) ** 0.5
        self.direction = (x / s, y / s)
        
        self.change_image('bullet1.png')
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x + hero.rect.width // 2 + self.direction[0] * 25
        self.rect.y = hero.rect.y + hero.rect.height // 2 + self.direction[1] * 25
    
    def update(self, *args):
        if args and args[0].type == MOVE:
            hitted_enemies = pygame.sprite.spritecollide(self, enemy_group, 0)
            if hitted_enemies:
                hitted_enemies[0].hp -= self.lvl_damage[self.spell_level] * DAMAGE_MULTIPLY
                if hitted_enemies[0].hp <= 0:
                    hitted_enemies[0].kill()
                self.kill()
                return
            self.rect.x = self.rect.x + self.direction[0] * SPELL_SPEED * 0.7
            self.rect.y = self.rect.y + self.direction[1] * SPELL_SPEED * 0.7


class CleavingSpear(Spell):
    lvl_damage = {
        0: 2,
        1: 4,
        2: 7,
        3: 10,
        4: 15,
        5: 23,
        6: 30,
    }
    def __init__(self, level, *groups):
        super().__init__(*groups)
        self.spell_level = level

        closest_enemy = Spell.find_closest_enemy()
        x = (closest_enemy.rect.x + closest_enemy.rect.width // 2) - (hero.rect.x + hero.rect.width // 2)
        y = (closest_enemy.rect.y + closest_enemy.rect.height // 2) - (hero.rect.y + hero.rect.height // 2)
        s = (x ** 2 + y ** 2) ** 0.5
        self.direction = (x / s, y / s)
        
        if y == 0:
            self.angle = 90
        else:
            self.angle = math.degrees(math.atan(x / y))
        self.image = load_image('cleaving_bullet.png', 'sprites').convert_alpha()
        self.rect = self.image.get_rect()
        # self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.rotate(self.image, self.angle + 90 + 180 * bool(y > 0))
        self.mask = pygame.mask.from_surface(self.image)
        
        l = (5 ** 2 + 120 ** 2) ** 0.5
        self.rect.x = hero.rect.x + hero.rect.width // 2 - abs(l * math.sin(math.radians(self.angle))) // 2
        self.rect.y = hero.rect.y + hero.rect.height // 2 - abs(l * math.cos(math.radians(self.angle))) // 2
    
    def update(self, *args):
        if args and args[0].type == MOVE:
            hitted_enemies = [enemy for enemy in enemy_group.sprites() if pygame.sprite.collide_mask(self, enemy)]
            if hitted_enemies:
                hitted_enemies[0].hp -= self.lvl_damage[self.spell_level] * DAMAGE_MULTIPLY
                if hitted_enemies[0].hp <= 0:
                    hitted_enemies[0].kill()
            self.rect.x = self.rect.x + self.direction[0] * SPELL_SPEED * 1.25
            self.rect.y = self.rect.y + self.direction[1] * SPELL_SPEED * 1.25
    

class LaserField(Spell):
    lvl_damage = {
        0: 1,
        1: 3,
        2: 6,
        3: 12,
        4: 16,
        5: 24,
        6: 30,
    }
    def __init__(self, level, *groups):
        super().__init__(*groups)
        self.spell_level = level
        
        self.image = pygame.transform.scale(load_image('laser_field.png', 'sprites'), (300, 300))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = hero.rect.x + hero.rect.w // 2 - self.rect.w // 2
        self.rect.y = hero.rect.y + hero.rect.h // 2 - self.rect.h // 2
    
    def update(self, *args):
        if args and args[0].type == FIELD_HIT:
            hitted_enemies = [enemy for enemy in enemy_group.sprites() if pygame.sprite.collide_rect(self, enemy)]
            if hitted_enemies:
                hitted_enemies[0].hp -= self.lvl_damage[self.spell_level] * DAMAGE_MULTIPLY
                if hitted_enemies[0].hp <= 0:
                    hitted_enemies[0].kill()
        self.rect.x = hero.rect.x + hero.rect.w // 2 - self.rect.w // 2
        self.rect.y = hero.rect.y + hero.rect.h // 2 - self.rect.h // 2
        

class Laser(Spell):
    lvl_damage = {
        0: 1,
        1: 3,
        2: 5,
        3: 10,
        4: 15,
        5: 20,
        6: 28,
    }
    def __init__(self, level, *groups):
        super().__init__(priority_spell_group, *groups)
        Laser.image = load_image('0.png', 'sprites/laser').convert_alpha()
        self.image = pygame.transform.scale(Laser.image, (0, 0))
        self.rect = self.image.get_rect()
        self.spell_level = level
        self.frame = 0
        
    def update(self, *args):
        self.frame = (self.frame + 2) % 8
        Laser.image = load_image(f'{self.frame // 2}.png', 'sprites/laser').convert_alpha()
        correct_enemies = [enemy for enemy in enemy_group.sprites() if 0 < enemy.rect.x < 800 and 0 < enemy.rect.y < 600]
        if not correct_enemies:
            self.image = pygame.transform.scale(self.image, (0, 0))
        if args and args[0].type == UPDATE_LASER_AIM:
            correct_enemies = [enemy for enemy in enemy_group.sprites() if 0 < enemy.rect.x < 800 and 0 < enemy.rect.y < 600]
            if not correct_enemies:
                return
            strongest_enemy = max(correct_enemies, key=lambda x:x.enemy_level)
            x = (strongest_enemy.rect.x + strongest_enemy.rect.width // 2) - (hero.rect.x + hero.rect.width // 2)
            y = (strongest_enemy.rect.y + strongest_enemy.rect.height // 2) - (hero.rect.y + hero.rect.height // 2)

            if y == 0:
                self.angle = 90
            else:
                self.angle = math.degrees(math.atan(x / y)) % 180 + 180 * bool(x > 0)
            
            self.image = pygame.transform.rotate(pygame.transform.scale(Laser.image, ((x ** 2 + y ** 2) ** 0.5, 20)).convert_alpha(), self.angle + 90)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = hero.rect.x + hero.rect.w // 2 - bool(x < 0) * self.rect.w
            self.rect.y = hero.rect.y + hero.rect.h // 2 - bool(y < 0) * self.rect.h
            
        if args and args[0].type == LASER_HIT:
            correct_enemies = [enemy for enemy in enemy_group.sprites() if 0 < enemy.rect.x < 800 and 0 < enemy.rect.y < 600]
            if not correct_enemies:
                return
            strongest_enemy = max(correct_enemies, key=lambda x:x.enemy_level)
            strongest_enemy.hp -= self.lvl_damage[self.spell_level]
            if strongest_enemy.hp < 0:
                strongest_enemy.kill()
                
                
class Earthquake(Spell):
    lvl_lifetime = {
        1: 3,
        2: 3,
        3: 4,
        4: 4,
        5: 5,
        6: 5,
        7: 6
    }
    lvl_damage = {
        1: 3,
        2: 5,
        3: 7,
        4: 10,
        5: 14,
        6: 19,
        7: 24
    }
    
    def __init__(self, level, *groups):
        super().__init__(*groups)
        self.spell_level = level
        self.lifetime = time.time()
        self.rotation_angle = random.randint(1, 360)
        self.image = pygame.transform.rotate(load_image('1.png', 'sprites/earthquake'),
                                                 self.rotation_angle)
        self.rect = self.image.get_rect()
        self.frame = 2
        
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = random.randint(0, HEIGHT - self.rect.h)
    
    def update(self, *args):
        if args and args[0].type == MOVE:
            self.frame = min(self.frame + 1, 12)
            self.image = pygame.transform.rotate(load_image(f'{self.frame // 2}.png', 'sprites/earthquake'),
                                                 self.rotation_angle)
            if time.time() - self.lifetime > self.lvl_lifetime[self.spell_level]:
                self.kill()
class Extermination(Spell):
    lvl_cooldown = {        1: 95,
        2: 90,
        3: 80,
        4: 70,
        5: 60,
        6: 50,
        7: 30
    }
    
    def __init__(self, level, *groups):
        super().__init__(priority_spell_group, *groups)
        self.spell_level = level
        self.image = load_image('1.png', 'sprites/extermination')
        self.frame = 3
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 80
        self.mini_graves_group = pygame.sprite.Group()
    
    
    def update(self, *args):
        if args and args[0].type == MOVE:
            for crucifix in self.mini_graves_group:
                crucifix.update_image()
            if self.frame <= 57:
                if self.frame % 3:
                    Crucifix(random.randint(-26 + 13 * self.frame, -13 + 13 * self.frame), 
                        random.randint(40, 460), self.mini_graves_group)
                    sound = pygame.mixer.Sound('extermination.wav')
                    sound.set_volume(0.5)
                    sound.play()
            self.frame += 1
            self.image = load_image(f"{min(self.frame // 3, 8)}.png", 'sprites/extermination')
            if self.frame == 4:
                spawn_sound = pygame.mixer.Sound('extermination.wav')
                spawn_sound.play()
            if self.frame == 24:
                for enemy in enemy_group.sprites():
                    enemy.kill()
            if self.frame == 69:
                for crucifix in self.mini_graves_group:
                    crucifix.kill()
                self.kill()
        

class Crucifix(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(all_sprites, priority_spell_group, *groups)
        self.image = pygame.transform.scale(load_image(f'1.png', 'sprites/extermination'),
                                            (100, 175))
        self.frame = 1
        self.rect = self.image.get_rect().move(x, y)
    
    def update_image(self):
        self.frame += 1
        if self.frame < 9:
            self.image = pygame.transform.scale(load_image(f'{min(self.frame, 8)}.png', 'sprites/extermination'),
                                                (100, 175))
        if self.frame == 8:
            for enemy in enemy_group.sprites():
                    enemy.kill()

        

class Tornado(Spell):
    lvl_lifetime = {
        1: 1,
        2: 1,
        3: 2,
        4: 3,
        5: 3,
        6: 4,
        7: 5
    }
    lvl_damage = {
        1: 4,
        2: 6,
        3: 7,
        4: 8,
        5: 10,
        6: 12,
        7: 15
    }
    def __init__(self, level, *groups):
        super().__init__(priority_spell_group, *groups)
        self.spell_level = level
        self.lifetime = time.time()
        self.image = load_image('tornado.png', 'sprites')
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = random.randint(0, HEIGHT - self.rect.h)
    
    def update(self, *args):
        if args and args[0].type == MOVE:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.rect.move(random.randint(-20, 20), random.randint(-20, 20))
            if time.time() - self.lifetime > self.lvl_lifetime[self.spell_level]:
                self.kill()


class RageMode:
    afk_images = [load_image(f'rage_mode/default/afk{i}.png', 'sprites') for i in range(4)]
    right_images = [load_image(f'rage_mode/default/right{i}.png', 'sprites') for i in range(4)]
    left_images = [load_image(f'rage_mode/default/left{i}.png', 'sprites') for i in range(4)]
    lvl_duration = {
        1: 10,
        2: 14,
        3: 14,
        4: 14,
        5: 14,
        6: 14,
        7: 14
    }
    lvl_cooldown = {
        1: 15,
        2: 15,
        3: 15,
        4: 15,
        5: 15,
        6: 15,
        7: 15
    }
    def __init__(self, level):
        self.spell_level = level
        self.frame = 0
        global DAMAGE_MULTIPLY, POINT_MULTIPLY, PLAYER_SPEED
        DAMAGE_MULTIPLY *= (1 + 0.1 * self.spell_level)
        POINT_MULTIPLY *= (1 + 0.05 * self.spell_level)
        PLAYER_SPEED *= (1 + 0.03 * self.spell_level)
        pygame.time.set_timer(RAGE_MODE_DISABLE, self.lvl_duration[self.spell_level] * 1_000)
        
    
    def disable(self):
        global DAMAGE_MULTIPLY, POINT_MULTIPLY, PLAYER_SPEED
        DAMAGE_MULTIPLY /= (1 + 0.1 * self.spell_level)
        POINT_MULTIPLY /= (1 + 0.05 * self.spell_level)
        PLAYER_SPEED /= (1 + 0.03 * self.spell_level)
        pygame.time.set_timer(RAGE_MODE_ENABLE, self.lvl_cooldown[self.spell_level] * 1_000)
        pygame.time.set_timer(RAGE_MODE_DISABLE, 0)


def main():
    
    def move_bg_images(dx, dy):
        for image_sprite in bg_images:
            image_sprite.rect.x += dx
            image_sprite.rect.y += dy
            image_sprite.rect.x += 1600 * (image_sprite.rect.x < 0)
            image_sprite.rect.x += -1600 * (image_sprite.rect.x > 800)
            image_sprite.rect.y += 1200 * (image_sprite.rect.y < 0)
            image_sprite.rect.y += -1200 * (image_sprite.rect.y > 600)
    global FPS, WIDTH, HEIGHT, SIZE, ENEMY_SPEED, SPELL_SPEED, POINT_MULTIPLY, DAMAGE_MULTIPLY, PLAYER_SPEED
    global screen, hero, end_game_reward, enemies_killed, music_queue
    global MOVE, POINT_SPAWN_EVENT, ENEMY_SPAWN_EVENT, KNIFE_THROWING, FIELD_HIT, LASER_HIT
    global CLEAVING_SPEAR_THROWING, ENEMY_HIT, EARTHQUAKE_HIT, EARTHQUAKE_SPAWN, EXTERMINATION_SPAWN
    global TORNADO_SPAWN, TORNADO_HIT, RAGE_MODE_DISABLE, RAGE_MODE_ENABLE, CLEANER, UPDATE_LASER_AIM, UPDATE_MUSIC_QUEUE
    global all_sprites, menu_buttons, player_group, points_group, enemy_group, earthquake_group, static_group
    global priority_spell_group, super_priority_group
    
    FPS = 60
    PLAYER_SPEED = 6
    ENEMY_SPEED = 7
    SPELL_SPEED = 70
    POINT_MULTIPLY = 1
    DAMAGE_MULTIPLY = 1
    end_game_reward = 0
    enemies_killed = 0
    music_queue = []
    
    all_sprites = pygame.sprite.Group()
    menu_buttons = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    points_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    earthquake_group = pygame.sprite.Group()
    tornado_group = pygame.sprite.Group()
    static_group = StaticGroup()
    cleaving_spear_group = pygame.sprite.Group()
    priority_spell_group = pygame.sprite.Group()
    super_priority_group = pygame.sprite.Group()
    
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 70)
        
    POINT_SPAWN_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(POINT_SPAWN_EVENT, 600)

    ENEMY_SPAWN_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, 800)
    
    KNIFE_THROWING = pygame.USEREVENT + 4
    pygame.time.set_timer(KNIFE_THROWING, 0)
    
    FIELD_HIT = pygame.USEREVENT + 5
    pygame.time.set_timer(FIELD_HIT, 300)
    
    LASER_HIT = pygame.USEREVENT + 6
    pygame.time.set_timer(LASER_HIT, 300)
    
    CLEAVING_SPEAR_THROWING = pygame.USEREVENT + 7
    pygame.time.set_timer(CLEAVING_SPEAR_THROWING, 0)
    
    ENEMY_HIT = pygame.USEREVENT + 8
    pygame.time.set_timer(ENEMY_HIT, 300)
    
    EARTHQUAKE_SPAWN = pygame.USEREVENT + 9
    pygame.time.set_timer(EARTHQUAKE_SPAWN, 0)
    
    EARTHQUAKE_HIT = pygame.USEREVENT + 10
    pygame.time.set_timer(EARTHQUAKE_HIT, 300)
    
    EXTERMINATION_SPAWN = pygame.USEREVENT + 11
    pygame.time.set_timer(EXTERMINATION_SPAWN, 0)
    
    TORNADO_SPAWN = pygame.USEREVENT + 12
    pygame.time.set_timer(TORNADO_SPAWN, 0)
    
    TORNADO_HIT = pygame.USEREVENT + 13
    pygame.time.set_timer(TORNADO_HIT, 300)
    
    RAGE_MODE_ENABLE = pygame.USEREVENT + 14
    pygame.time.set_timer(RAGE_MODE_ENABLE, 0)
    
    RAGE_MODE_DISABLE = pygame.USEREVENT + 15
    pygame.time.set_timer(RAGE_MODE_DISABLE, 0)
    
    CLEANER = pygame.USEREVENT + 16
    pygame.time.set_timer(CLEANER, 1000)
    
    UPDATE_LASER_AIM = pygame.USEREVENT + 17
    pygame.time.set_timer(UPDATE_LASER_AIM, 100)
    
    UPDATE_MUSIC_QUEUE = pygame.USEREVENT + 18
    pygame.mixer.music.set_endevent(UPDATE_MUSIC_QUEUE)
    
    pygame.display.set_caption("Happy dreams")
    running = True
    
    main_menu()
    screen.fill('black')
    bg_images = [pygame.sprite.Sprite(all_sprites) for _ in range(4)]
    for bg_image in bg_images:
        bg_image.image = pygame.transform.scale(load_image('grass_bg.png', 'sprites'), (800, 600))
    bg_images[0].rect = bg_images[0].image.get_rect()
    bg_images[1].rect = bg_images[1].image.get_rect().move(800, 0)
    bg_images[2].rect = bg_images[2].image.get_rect().move(0, 600)
    bg_images[3].rect = bg_images[3].image.get_rect().move(800, 600)
    
    
    data = json.load(open("data.json"))
    heroes = [ChillGuy, Collector, Warrior, Absolute]
    
    hero = heroes[data["mutations_inventory"].index(1)](static_group, super_priority_group)
    hero.rect = hero.rect.move(380, 220)
    
    global progress_image, progress_bar, progress_bar_frame
    progress_bar_frame = pygame.sprite.Sprite(all_sprites, super_priority_group)
    progress_bar_frame.image = load_image('progress_bar_frame.png', 'sprites')
    progress_bar_frame.rect = progress_bar_frame.image.get_rect().move(110, 20)
    
    progress_bar = pygame.sprite.Sprite(all_sprites, super_priority_group)
    progress_image = load_image('progress_bar.png', 'sprites')
    progress_bar.image = progress_image
    progress_bar.rect = progress_bar.image.get_rect().move(150, 32)    
    
    all_sprites.draw(screen)
    pygame.display.flip()
    global time_count
    time_count = time.time()
    update_music()
    # for _ in range(7):
    #     hero.upgrade_bullet()
    #     hero.upgrade_laser()
    #     hero.upgrade_tornado()
    #     hero.upgrade_earthquake()
    #     hero.upgrade_cleaving_blade()
    #     hero.upgrade_laser_field()
    #     hero.upgrade_rage_mode()
    #     hero.upgrade_extermination()
    hero.upgrade_bullet()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == MOVE:
                keys = pygame.key.get_pressed()
                if not hero.rage_mode_is_active:  
                    hero.image = hero.afk_image
                else:
                    rage_mode.frame = (rage_mode.frame + 1) % 4
                    hero.image = rage_mode.afk_images[rage_mode.frame]
                if keys[pygame.K_LEFT]:
                    if not keys[pygame.K_RIGHT]:
                        if not hero.rage_mode_is_active:
                            hero.image = hero.left_image
                        else:
                            rage_mode.frame = (rage_mode.frame + 1) % 4
                            hero.image = rage_mode.left_images[rage_mode.frame]
                    if hero.rect.x < 200:
                        static_group.move(int(-PLAYER_SPEED), 0)
                        hero.update_field(int(PLAYER_SPEED), 0)
                        move_bg_images(int(PLAYER_SPEED), 0)
                    else:
                        hero.rect.x -= int(PLAYER_SPEED)  
                    hero.chechk_for_picking_point()
                if keys[pygame.K_RIGHT]:
                    if not keys[pygame.K_LEFT]:
                        if not hero.rage_mode_is_active:
                            hero.image = hero.right_image
                        else:
                            rage_mode.frame = (rage_mode.frame + 1) % 4
                            hero.image = rage_mode.right_images[rage_mode.frame]
                    if hero.rect.x > 600 - hero.rect.width:
                        static_group.move(int(PLAYER_SPEED), 0)
                        hero.update_field(int(-PLAYER_SPEED), 0)
                        move_bg_images(int(-PLAYER_SPEED), 0)
                    else:
                        hero.rect.x += int(PLAYER_SPEED)  
                    hero.chechk_for_picking_point()
                if keys[pygame.K_UP]:
                    if hero.rect.y < 100:
                        static_group.move(0, int(-PLAYER_SPEED))
                        hero.update_field(0, int(PLAYER_SPEED))
                        move_bg_images(0, int(PLAYER_SPEED))
                    else:
                        hero.rect.y -= int(PLAYER_SPEED)  
                    hero.chechk_for_picking_point()
                if keys[pygame.K_DOWN]:
                    if hero.rect.y > 500 - hero.rect.height:
                        static_group.move(0, int(PLAYER_SPEED))
                        hero.update_field(0, int(-PLAYER_SPEED))
                        move_bg_images(0, int(-PLAYER_SPEED))
                    else:
                        hero.rect.y += int(PLAYER_SPEED)  
                    hero.chechk_for_picking_point()

            if event.type == POINT_SPAWN_EVENT:
                spawn_point(time.time() - time_count)
            if event.type == ENEMY_SPAWN_EVENT:
                x = random.choice([random.randint(-400, -100), random.randint(900, 1300)])
                y = random.choice([random.randint(-400, -100), random.randint(900, 1300)])
                spawn_enemy(time.time() - time_count)
            if event.type == KNIFE_THROWING: 
                correct_enemies = [enemy for enemy in enemy_group.sprites() if 0 < enemy.rect.x < 800 and 0 < enemy.rect.y < 600]
                if correct_enemies:
                    Bullet(hero.bullet_level)
            if event.type == CLEAVING_SPEAR_THROWING:
                for sprite in cleaving_spear_group:
                    sprite.kill()
                correct_enemies = [enemy for enemy in enemy_group.sprites() if 0 < enemy.rect.x < 800 and 0 < enemy.rect.y < 600]
                if correct_enemies:
                    CleavingSpear(hero.cleaving_spear_level, cleaving_spear_group)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                global pause_time_start
                pause_time_start = time.time()
                pause_menu()
            if event.type == ENEMY_HIT:
                for enemy in pygame.sprite.spritecollide(hero, enemy_group, 0):
                    hero.hp -= enemy.damage
                    if False:
                        hero.hp = 0
                        draw_sprites()
                        lose_screen()

            if event.type == EARTHQUAKE_SPAWN:
                Earthquake(hero.upgrades['Earthquake'][0], earthquake_group)
            if event.type == EARTHQUAKE_HIT:
                for earthquake in earthquake_group.sprites():
                    for enemy in pygame.sprite.spritecollide(earthquake, enemy_group, 0):
                        enemy.hp -= earthquake.lvl_damage[earthquake.spell_level]
                        if enemy.hp <= 0:
                            enemy.kill()
            if event.type == EXTERMINATION_SPAWN:
                Extermination(hero.upgrades["Extermination"][0])
            if event.type == TORNADO_SPAWN:
                Tornado(hero.upgrades["Tornado"][0], tornado_group)
            if event.type == TORNADO_HIT:
                for tornado in tornado_group.sprites():
                    for enemy in pygame.sprite.spritecollide(tornado, enemy_group, 0):
                        enemy.hp -= tornado.lvl_damage[tornado.spell_level]
                        if enemy.hp <= 0:
                            enemy.kill()
            if event.type == RAGE_MODE_ENABLE:
                rage_mode = RageMode(hero.upgrades["Rage mode"][0])
                hero.rage_mode_is_active = True
            if event.type == RAGE_MODE_DISABLE:
                hero.rage_mode_is_active = False
                rage_mode.disable()
            if event.type == CLEANER:
                clear_rubbish()
            if event.type == UPDATE_MUSIC_QUEUE:
                update_music()
            
            all_sprites.update(event)
        progress_bar.rect.x = 150
        progress_bar.rect.y = 32
        progress_bar_frame.rect.x = 110
        progress_bar_frame.rect.y = 20
        draw_sprites()
        update_progress_bar()
        

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.05)
    main()  