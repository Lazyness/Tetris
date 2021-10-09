import pygame
from copy import deepcopy
from random import choice, randrange
import random
import datetime

# игровое поле
WIDTH = 15
HEIGHT = 24
#размер клеточки
CELL = 30
# size window (all)
GAME_RES = WIDTH*CELL,HEIGHT*CELL

# добавим главное окно
BIG_RES = 820,730
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
# заголовок игры
pygame.display.set_caption("Dark Tetris")

# voice
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

g_b = pygame.mixer.Sound("sounds/glass_break.wav")
m = pygame.mixer.Sound("sounds/monster.wav")
# window for game BIG_RES
window_big = pygame.display.set_mode(BIG_RES)

# window for games
# window = pygame.display.set_mode(GAME_RES)
window = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
# разметка поля
grid = [pygame.Rect(x * CELL, y * CELL, CELL, CELL) for x in range(WIDTH) for y in range(HEIGHT)]
# двумерный список
figures_pos = [[(0, 0), (-1, 0), (0, 1), (-1, -1)],
[(-1, 0), (-2, 0), (0, 0), (1, 0)],
[(0, -1), (-1, -1), (-1, 0), (0, 0)],
[(0, 0), (0, -1), (0, 1), (-1, 0)],
[(-1, 0), (-1, 1), (0, 0), (0, -1)],
[(0, 0), (0, -1), (0, 1), (-1, -1)],
[(0, 0), (0, -1), (0, 1), (1, -1)]]
# заполняем нулями наше игровое поле
field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]
t1 = pygame.font.SysFont('serif', 48)
title_game_over = t1.render('GAME OVER!', False, pygame.Color('red'))
t2 = pygame.font.SysFont('serif', 36)
title_game = t2.render('DARK TETRIS', False, pygame.Color('darkorange'))
t3 = pygame.font.SysFont('serif', 24)
title_game_score = t3.render('SCORE:', False, pygame.Color('darkorange'))
title_game_record = t3.render('RECORD:', False, pygame.Color('darkorange'))
title_game_time = t3.render('TIME GAME:', False, pygame.Color('darkorange'))
title_next_cubes = t3.render('NEXT BRICK', False, pygame.Color('red'))
# переменные щетчики (падение фигуры)
animation_count = 0
animation_speed = 60
animation_limit = 2500
# в этом масиве будем  брать елемент двумерного списка а потом каждую координату с этого списка
figures = [[pygame.Rect(x + WIDTH//2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, CELL - 1, CELL - 1)

# выбор фигуры
cubes = deepcopy(choice(figures))
next_cubes = deepcopy(choice(figures))
space = pygame.image.load('img/space.jpg').convert()
astronaut = pygame.image.load('img/astronaut.jpg').convert()
death = pygame.image.load('img/death.jpg').convert()
glass = pygame.image.load('img/glass.png').convert()
# blood = pygame.image.load('img/blood.png').convert()
# граници поля
def check_borders():
    if cubes[i].x < 0 or cubes[i].x > WIDTH - 1:
        return False
    elif cubes[i].y > HEIGHT - 1 or field[cubes[i].y][cubes[i].x]:
        return False
    # print("cubes[i].x = " + str(cubes[i].x) + ", field[cubes[i].y][cubes[i].x = " + str(field[cubes[i].y][cubes[i].x]))
    return True
# запись в файл рекорда
def get_record_game():
    try:
        with open('record_game') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record_game', 'w') as f:
            f.write('0')

# запись нового рекорда если очки больше чем были
def set_record_game(record, score):
    rec = max(int(record), score)
    with open('record_game', 'w') as f:
        f.write(str(rec))

    # print("minute: " + str(current_datetime.minute))
    # print("second: " + str(current_datetime.second))
    # print("microsecond: " + str(current_datetime.microsecond) )

# get_color = lambda : (randrange(90, 256), randrange(90, 256), randrange(90, 256))
WHITE = (255, 255, 255)
PINK = (246, 0, 255)
GREEN = (0, 255, 0)
BLUE_SKY = (0, 255, 251)
BLUE_FIOLE = (88, 80, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 198, 0)
BLOOD_RED = (219, 0, 26)

COLOR = [WHITE, PINK, GREEN, BLUE_SKY, BLUE_FIOLE, YELLOW, ORANGE]
color = choice(COLOR)
next_color = choice(COLOR)

flPause = False
score = 0
lines = 0
time_game_first = 0
time_game_second = 0
datat = 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
time_game_first = datetime.datetime.today()
run = True
while run:
    # window.fill(pygame.Color('black'))
    window_big.blit(space, (0, 0))
    window_big.blit(window,(5,5))
    window.blit(astronaut, (0, 0))
    # pygame.draw.rect(window_big, (255, 10, 10),
    #                  (100, 1, 100, 20), 1)
    distX = 0
    rotate = 0
    # distY = 0
    record = get_record_game()

    for event in pygame.event.get():
        # Проверить если нажато выход то выходим:
        if event.type == pygame.QUIT:
            # exit()
            run = False
        if event.type == pygame.KEYDOWN:
            # get x
            if event.key == pygame.K_RIGHT:
                distX = 1
            elif event.key == pygame.K_LEFT:
                distX = -1
            # position 90 -
            elif event.key == pygame.K_UP:
                rotate = 1
            # get y
            elif event.key == pygame.K_DOWN:
                # distY = 1
                animation_limit = 50

    figure_old = deepcopy(cubes)
        # move x
    for i in range(4):
        cubes[i].x += distX
        # move y (DOWN)
        # cubes[i].y += distY
        # проверка и отдача скопированой фигуры при пересечении границы
        if check_borders()==False:
            cubes = deepcopy(figure_old)
            break
    # move y (ускоренное падение)
    animation_count += animation_speed
    if animation_count > animation_limit:
        animation_count = 0
        figure_old = deepcopy(cubes)
        for i in range(4):
            cubes[i].y += 1
            if check_borders()==False:
                for i in range(4):
                    # закрашиваем упавшую фигуру
                    field[figure_old[i].y][figure_old[i].x] = pygame.Color(BLOOD_RED)
                # color = choice(COLOR)
                # cubes = deepcopy(choice(figures))
                cubes, color = next_cubes, next_color
                next_cubes, next_color = deepcopy(choice(figures)), choice(COLOR)
                animation_limit = 2500
                break

    # check lines
    line = HEIGHT - 1
    lines = 0
    for row in range(line, -1, -1):
        count = 0
        for i in range(WIDTH):
            if field[row][i]:
                # max 15 перезапись строки в которой лини заполнена допустим
                # заполено 23 поле тогда 22 поле запишеться на место 23
                count += 1
            field[line][i] = field[row][i]
        if count < WIDTH:
            line -= 1
        else:
            lines += 1
    # compute score
    score += scores[lines]

    # rotate
    center = cubes[0]
    # print("cubes[0] = "+str(cubes[0]))
    figure_old = deepcopy(cubes)
    if rotate:
        for i in range(4):
            center_x = cubes[i].y - center.y
            # print("cubes[i].y = "+str(cubes[i].y))
            # print("center.y = "+str(center.y))
            center_y = cubes[i].x - center.x
            # перезапись координат для перерисовки
            cubes[i].x = center.x - center_x
            cubes[i].y = center.y + center_y
            if check_borders()==False:
                cubes = deepcopy(figure_old)
                break

    #рисуем клеточки
    [pygame.draw.rect(window, (0,0,0), i_rect, 1) for i_rect in grid]
    # pygame.draw.rect(window,(60,60,10),(0,0,CELL,CELL))

    # draw cubes
    for i in range(4):
        figure_rect.x = cubes[i].x * CELL
        figure_rect.y = cubes[i].y * CELL
        pygame.draw.rect(window, color, figure_rect)

    # рисуем поле с учетом упавших фигур
    for y in range(len(field)):
        raw = field[y]
        for x in range(len(raw)):
            col = raw[x]
            if col:
                figure_rect.x, figure_rect.y = x * CELL, y * CELL
                pygame.draw.rect(window, col, figure_rect)

    # game over
    for i in range(WIDTH):
        if field[0][i]:
            flPause = True
            time_game_second = datetime.datetime.today()
            set_record_game(record, score)
            field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            animation_count, animation_speed, animation_limit = 0, 60, 2500
            score = 0
            if flPause:
                pygame.mixer.music.pause()
                g_b.play()
            window_big.blit(glass, (0, 0))
            pygame.display.flip()
            clock.tick(1)
            m.play()
            for i_rect in grid:
                window_big.blit(death, (0, 0))
                # window_big.blit(blood, (0, 0))

                window_big.blit(title_game_over, ((WIDTH*CELL)//6, (HEIGHT*CELL)//2))
                # print("time_game_first:"+str(time_game_first))
                # print("time_game_second: "+str(time_game_second))
                # print(())
                datat = time_game_second-time_game_first
                window_big.blit(title_game_time, ((WIDTH*CELL)//6, 410))
                window_big.blit(t3.render(str(datat), True, pygame.Color('darkorange')), ((WIDTH*CELL)//6 + 150, 410))
                # pygame.display.update()
                if WIDTH>10:
                    get_position_block = [WIDTH // 2, WIDTH // 3, WIDTH // 4]
                else:
                    get_position_block = [WIDTH//2]

                block = choice(get_position_block)
                figures = [[pygame.Rect(x + block, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
                #
                # # выбор фигуры
                cubes = deepcopy(choice(figures))
                pygame.display.flip()
                clock.tick(200)
                # run = False
            time_game_first = datetime.datetime.today()
            flPause = False
            m.stop()
            pygame.mixer.music.unpause()
            pygame.mixer.music.rewind()
    # draw next cubes
    for i in range(4):
        figure_rect.x = next_cubes[i].x * CELL + 425
        figure_rect.y = next_cubes[i].y * CELL + 150

        pygame.draw.rect(window_big, next_color, figure_rect)

    # draw titless
    window_big.blit(title_game, (525, 10))
    window_big.blit(title_next_cubes, (570, 100))
    window_big.blit(title_game_score, (570, 300))
    window_big.blit(t3.render(str(score), True, pygame.Color('darkorange')), (675, 300))
    window_big.blit(title_game_record, (570, 400))
    window_big.blit(t3.render(record, True, pygame.Color('darkorange')), (690, 400))
    #обновляет ввесь екран
    pygame.display.flip()
    clock.tick(60)
