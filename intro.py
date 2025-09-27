import pgzrun
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


level_map = [
    "                ",
    "                ",
    "    E            ",
    "    T            ",
    "     T          ",
    "   T            ",
    "                ",
    "  F             ",
    "TTTTTTTTTTTTTTTT",
]

tiles = []
enemies = []
flag = None

def setup_level():
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
                enemy = Actor('enemy', topleft=(x, y))
                enemies.append(enemy)
            if cell == 'F':
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT
                global flag
                flag = Actor('exit', topleft=(x, y))

class Player:
    def __init__(self):
        self.player = Actor('frog')
        self.player.x = 50

        self.player.y = 200
        self.vy = 0
        self.on_ground = False
        self.speed = 4 

    def set_frog_normal_right(self):
        self.player.image = 'frog'

    def set_frog_normal_left(self):
        self.player.image = 'frog_left'

    def update(self, tiles_list, enemies_list):
        prev_x = self.player.x
        prev_y = self.player.y

        if keyboard.D:
            self.player.x += self.speed
            if keyboard.W:
                self.player.image = 'frog_rest_right'
            else:
                self.player.image = 'frog_jump_right'
            clock.schedule_unique(self.set_frog_normal_right, 0.25)
        if keyboard.A:
            self.player.x -= self.speed
            if keyboard.W:
                self.player.image = 'frog_rest_left'
            else:
                self.player.image = 'frog_jump_left'
            clock.schedule_unique(self.set_frog_normal_left, 0.25)

        for tile in tiles_list:
            if self.player.colliderect(tile):
                self.player.x = prev_x
                break

        self.vy += 1
        if self.vy > 10:
            self.vy = 10
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
                self.player.x = 50
                self.player.y = 200
                self.vy = 0
                break
        
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > WIDTH:
            self.player.right = WIDTH

    def jump(self):
        if self.on_ground:
            if effects_state == 'on':
                sounds.jump.play()
            self.vy = -15
            self.on_ground = False

player = Player()
setup_level()
def update():
    if game_state == 'game':
        player.update(tiles, enemies)

def draw():
    screen.clear()
    if game_state == 'intro':
        screen.blit('bg', (0, 0))
        draw_menu()
    elif game_state == 'game':
        screen.blit('bg', (0, 0))
        draw_game()

music_clicked = False
def draw_menu():
    screen.blit('logo', (250, 20))
    screen.draw.text("Iniciar jogo", center=(WIDTH//2, 180), fontsize=30, color="white")
    screen.draw.text("Sair", center=(WIDTH//2, 220), fontsize=30, color="white")

    global music_clicked
    if music_state == 'on':
        screen.blit('btn_music_on', (340, 280))
        if not music_clicked:
            music.play('music')
            music_clicked = True
    elif music_state == 'off':
        screen.blit('btn_music_off', (340, 280))
        if music_clicked:
            music.stop()
            music_clicked = False

    if effects_state == 'on':
        screen.blit('btn_effects_on', (420, 280))
    else:
        screen.blit('btn_effects_off', (420, 280))

def draw_game():
    player.player.draw()
    for tile in tiles:
        tile.draw()
    for enemy in enemies:
        enemy.draw()
    flag.draw()
    if player.player.colliderect(flag):
        print('You win!')

def on_key_down(key):
    if game_state == 'game' and key == keys.W:
        player.jump()

def on_mouse_down(pos):
    global game_state, music_state, effects_state
    if start_rect.collidepoint(pos):
        game_state = 'game'
    elif exit_rect.collidepoint(pos):
        quit()
    elif music_rect.collidepoint(pos):
        if music_state == 'on':
            music_state = 'off'
        else:
            music_state = 'on'
    elif effects_rect.collidepoint(pos):
        if effects_state == 'on':
            effects_state = 'off'
        else:
            effects_state = 'on'

pgzrun.go()