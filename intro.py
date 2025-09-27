import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 400
TITLE = "Platformer do Paulo"

TILE_WIDTH = 50
TILE_HEIGHT = 46

game_state = 'intro'
music_state = 'on'
effects_state = 'on'

start_rect = Rect(WIDTH//2 - 75, 162, 150, 36)
exit_rect = Rect(WIDTH//2 - 30, 202, 60, 36)
music_rect = Rect(340, 280, 45, 45)
effects_rect = Rect(420, 280, 45, 45)
back_to_menu_rect = Rect(WIDTH//2 - 100, 222, 200, 36)
next_level_rect = Rect(WIDTH//2 - 125, 192, 250, 36)
win_menu_rect = Rect(WIDTH//2 - 80, 242, 160, 36)

LEVEL_MAPS = [
    [
        "                ",
        "                ",
        "              F ", 
        "            TTT ", 
        " T        T     ",
        "      E T       ",
        "    T           ",
        "  T      E      ",
        "TTTTTTTTTTTTTTTT",
    ],
    [
        "                ",
        "                ",
        "                ",
        "    T  E     F  ",
        "T           TTTT",
        "      T         ",
        "  TT  E   TTT   ",
        "                ",
        "TTTTTTTTTTTTTTTT",
    ],
    [
        "             F  ",
        "       T     T  ",
        "    T     T     ",
        " T       E      ",
        "       T T      ",
        "     T     T    ",
        "   T    E    T  ",
        "                ",
        "TTTTTTTTTTTTTTTT",
    ],
    [
        "                ",
        "  F             ",
        "  TT            ",
        "       T T     E",
        "              TT",
        "            T    ",
        "        T       ",
        "     T   E T    ",
        "TTTTTTTTTTTTTTTT",
    ]
]

tiles = []
enemies = []
flag = None

def setup_level():
    global flag
    level_map = random.choice(LEVEL_MAPS)
    
    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            if cell == 'T':
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT
                tile = Actor('ground', topleft=(x, y))
                tiles.append(tile)
            if cell == 'E':
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT
                enemy = Actor('enemy_right', topleft=(x, y))
                enemy.direction = 1
                enemy.speed = 0.5
                enemy.start_x = x - 120
                enemy.end_x = x + 120
                enemies.append(enemy)
            if cell == 'F':
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT
                flag = Actor('exit', topleft=(x, y))

class Player:
    def __init__(self):
        self.player = Actor('frog')
        self.player.x = 50
        self.player.y = 200
        self.vy = 0
        self.on_ground = False
        self.speed = 4
        self.player.direction = 'right'
        self.player.lifecount = 3

    def set_frog_normal_right(self): self.player.image = 'frog'
    def set_frog_normal_left(self): self.player.image = 'frog_left'

    def update(self, tiles_list, enemies_list):
        prev_x = self.player.x
        if keyboard.D:
            self.player.x += self.speed
            self.player.image = 'frog_jump_right'
            clock.schedule_unique(self.set_frog_normal_right, 0.25)
            self.player.direction = 'right'
        if keyboard.A:
            self.player.x -= self.speed
            self.player.image = 'frog_jump_left'
            clock.schedule_unique(self.set_frog_normal_left, 0.25)
            self.player.direction = 'left'

        for tile in tiles_list:
            if self.player.colliderect(tile):
                self.player.x = prev_x
                break
        self.vy += 1
        if self.vy > 10: self.vy = 10
        self.player.y += self.vy

        self.on_ground = False
        for tile in tiles_list:
            if self.player.colliderect(tile):
                if self.vy > 0:
                    self.player.bottom = tile.top
                    self.on_ground = True
                    self.vy = 0
                elif self.vy < 0:
                    self.player.top = tile.bottom
                    self.vy = 0
                break
        
        for enemy in enemies_list:
            if self.player.colliderect(enemy):
                self.player.x = 50; self.player.y = 200; self.vy = 0
                if effects_state == 'on': sounds.jingles_steel07.play()
                self.player.lifecount -= 1
                break
        
        if self.player.left < 0: self.player.left = 0
        if self.player.right > WIDTH: self.player.right = WIDTH

    def jump(self):
        if self.on_ground:
            if effects_state == 'on': sounds.jump.play()
            self.vy = -15
            self.on_ground = False

def start_new_game():
    global game_state, player, flag
    player = Player()
    tiles.clear()
    enemies.clear()
    flag = None
    setup_level()
    game_state = 'game'
    if music_state == 'on':
        music.play('music')
        music.set_volume(0.3)

player = Player()

def update():
    if game_state == 'game':
        player.update(tiles, enemies)
        for enemy in enemies:
            enemy.x += enemy.speed * enemy.direction
            if enemy.right > enemy.end_x or enemy.left < enemy.start_x:
                enemy.direction *= -1
                enemy.image = 'enemy_right' if enemy.direction == 1 else 'enemy_left'

def draw():
    screen.clear()
    screen.blit('bg', (0, 0))
    
    if game_state == 'game' or game_state == 'win' or game_state == 'game_over':
        draw_game_elements()

    if game_state == 'intro':
        draw_menu()
    elif game_state == 'win':
        draw_win_screen()
    elif game_state == 'game_over':
        draw_game_over()

def draw_game_elements():
    player.player.draw()
    for tile in tiles: tile.draw()
    for enemy in enemies: enemy.draw()
    if flag:
        flag.draw()
    screen.blit("heart", (10,10))
    screen.draw.text(str(player.player.lifecount), center=(42, 45), fontsize=50, color="white")
    check_game_status()

def check_game_status():
    global game_state
    if flag and player.player.colliderect(flag):
        music.stop()
        if effects_state == 'on' and game_state != 'win':
            sounds.jingles_sax10.play()
        game_state = 'win'
    if player.player.lifecount <= 0 and game_state == 'game':
        music.stop()
        game_state = 'game_over'


music_clicked = False
def draw_menu():
    screen.blit('logo', (250, 20))
    screen.draw.text("Iniciar jogo", center=(WIDTH//2, 180), fontsize=30, color="white")
    screen.draw.text("Sair", center=(WIDTH//2, 220), fontsize=30, color="white")
    global music_clicked
    if music_state == 'on':
        screen.blit('btn_music_on', (340, 280))
        if not music_clicked:
            music.play('music'); music.set_volume(0.3); music_clicked = True
    elif music_state == 'off':
        screen.blit('btn_music_off', (340, 280))
        if music_clicked:
            music.stop(); music_clicked = False
    screen.blit('btn_effects_on' if effects_state == 'on' else 'btn_effects_off', (420, 280))

def draw_win_screen():
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 150))
    screen.draw.text("VOCÊ VENCEU!", center=(WIDTH//2, 120), fontsize=60, color="yellow")
    screen.draw.text("Jogar novamente", center=(WIDTH//2, 210), fontsize=30, color="white")
    screen.draw.text("Menu principal", center=(WIDTH//2, 260), fontsize=30, color="white")

def draw_game_over():
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 150))
    screen.draw.text("VOCÊ PERDEU", center=(WIDTH//2, 150), fontsize=60, color="red")
    screen.draw.text("Voltar ao Menu", center=(WIDTH//2, 240), fontsize=30, color="white")

def on_key_down(key):
    if game_state == 'game' and key == keys.W:
        player.jump()

def on_mouse_down(pos):
    global game_state, music_state, effects_state
    
    if game_state == 'intro':
        if start_rect.collidepoint(pos):
            start_new_game()
        elif exit_rect.collidepoint(pos):
            quit()
        elif music_rect.collidepoint(pos):
            music_state = 'off' if music_state == 'on' else 'on'
        elif effects_rect.collidepoint(pos):
            effects_state = 'off' if effects_state == 'on' else 'on'
            
    elif game_state == 'game_over':
        if back_to_menu_rect.collidepoint(pos):
            game_state = 'intro'

    elif game_state == 'win':
        if next_level_rect.collidepoint(pos):
            start_new_game()
        elif win_menu_rect.collidepoint(pos):
            game_state = 'intro'

def animate_frog():
    if game_state != 'game': return
    if not keyboard.A and not keyboard.D and player.on_ground:
        if player.player.direction == 'right':
            player.player.image = 'frog_closed_eyes_right' if player.player.image == 'frog' else 'frog'
        else:
            player.player.image = 'frog_closed_eyes_left' if player.player.image == 'frog_left' else 'frog_left'

def animate_enemies():
    if game_state != 'game': return
    for enemy in enemies:
        if enemy.direction == 1:
            enemy.image = 'enemy_right_closed' if enemy.image == 'enemy_right' else 'enemy_right'
        else:
            enemy.image = 'enemy_left_closed' if enemy.image == 'enemy_left' else 'enemy_left'

clock.schedule_interval(animate_frog, 0.3)
clock.schedule_interval(animate_enemies, 0.2)

pgzrun.go()