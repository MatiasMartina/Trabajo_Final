from models.player.main_player import Jugador
import pygame as pg
from pygame.locals import *
from models.constantes import *
from world import *
from chronometer import Chronometer
from level import Level
from GUI_form_main import FormPrueba

pg.init()

screen_height = 800
screen_width = 800
initial_time = 10  # 3 minutos inicialmente (puedes ajustar esto según tus necesidades)

chronometer = Chronometer(initial_time)

clock = pg.time.Clock()
screen = pg.display.set_mode((screen_height, screen_width))
pg.display.set_caption("BA-ME-APRO")

img_background = pg.image.load('assets\img\\background\\background1.png')
scaled_background = pg.transform.scale(img_background, (1200, 800))

# INSTANCIAMOS
player = Jugador(50, 650, frame_rate=1, speed_walk=5, speed_run=10, gravity=5, delta_ms=1, speed_jump=50)
level_start = Level(actual_level)
enemies_list = pg.sprite.Group()
coins_list = []
trap_list = []
bullet_list = []
key_list = pg.sprite.Group()
game_over = 0

world = None
tile_list = pg.sprite.Group
running = True
paused = False
form_main = FormPrueba(screen, 0, 0, 900, 1200, "cyan", "yellow", 5, True, running)

while running:
    if not world:
        world_data = level_start.load_level()
        world = World(world_data, enemies_list, coins_list, trap_list, key_list)

        if DEBUG_LEVEL:
            print(f'{player.level}')

    pressed_key = pg.key.get_pressed()
    event_list = pg.event.get()
    form_main.update(event_list)

    for event in event_list:
        print("actualiza")
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused

    if not paused:
        screen.blit(scaled_background, scaled_background.get_rect())
        delta_ms = clock.tick(FPS)
        world.draw_grid(screen)

        if MAIN_MENU:
            form_main.update(event_list)
        else:
            world.draw(screen)

            for enemies in enemies_list:
                if game_over == 0:
                    enemies.update(screen, world, player)
                enemies.draw(screen)

            for trap in trap_list:
                trap.update(screen, player)

            for key in key_list:
                key.update(screen, player)

            for bullet in bullet_list:
                if game_over == 0:
                    bullet.update(delta_ms, tile_list, enemies_list, player, world)
                bullet.draw(screen, bullet_list)

            chronometer.update()
            chronometer.draw(screen)
            game_over = player.update(pressed_key, delta_ms, screen, world, trap_list, bullet_list, game_over)

    pg.display.update()
    if paused:
        pg.time.delay(100)

pg.quit()