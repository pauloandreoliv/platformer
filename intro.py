import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 400
TITLE = "Platformer do Paulo"

game_state = 'intro'
music_state = 'on'
effects_state = 'on'

start_rect = Rect(WIDTH//2 - 75, 162, 150, 36)
exit_rect = Rect(WIDTH//2 - 30, 202, 60, 36)
music_rect = Rect(340, 280, 45, 45)
effects_rect = Rect(420, 280, 45, 45)

class Player:
    def __init__(self):
        self.player = Actor('frog')
        self.player.x = 50
        self.player.y = 335
        self.player.vy = 0
        self.player.on_ground = False
        self.speed = 5 
    
    def update(self):
        self.player.vy += 1
        self.player.y += self.player.vy
        if self.player.y > 335:
            self.player.y = 335
            self.player.vy = 0
            self.player.on_ground = True

        if keyboard.D:
            self.player.x += self.speed
        if keyboard.A:
            self.player.x -= self.speed

        if self.player.x < 0:
            self.player.x = 10
        if self.player.x > WIDTH - 10:
            self.player.x = WIDTH - 10

    def jump(self):
        if self.player.on_ground:
            self.player.vy = -15
            self.player.on_ground = False

player = Player()
def update():
    if game_state == 'game':
        player.update()

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
    for x in range(0, WIDTH, 50):  
        screen.blit('ground', (x, 360))

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