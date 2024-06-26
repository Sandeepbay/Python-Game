import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

SPEED = 10
score = 0

RED = (255 , 0, 0)
BACKGROUND_COLOR = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255 , 0)

player_size = 50
player_pos = [WIDTH / 2 , HEIGHT - 2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0 , WIDTH - enemy_size) , 0]
enemy_list = [enemy_pos]

screen = pygame.display.set_mode((WIDTH , HEIGHT))

clock = pygame.time.Clock()

game_over = False

myFont =  pygame.font.SysFont('monospace', 35)

def setLevel(score , SPEED):
    if score < 20:
        SPEED = 10
    elif score <= 40:
        SPEED = 15
    elif score <= 50:
        SPEED = 20
    else:
        SPEED = 25
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 25 and delay < 0.1:
        x_pos = (random.randint(0 , WIDTH - enemy_size))
        y_pos = 0
        enemy_list.append([x_pos , y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
           pygame.draw.rect(screen , BLUE , (enemy_pos[0] , enemy_pos[1] , enemy_size , enemy_size))

def update_enemy_positions(enemy_list , score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            score += 1
            enemy_list.pop(idx)
    return score

def collisionChecker(enemy_list , player_pos):
    for enemy_pos in enemy_list:
        if detect_collisions(player_pos , enemy_pos):
            return True
    return False


def detect_collisions(player_pos , enemy_pos):
    player_x = player_pos[0]
    player_y = player_pos[1]

    enemy_x = enemy_pos[0]
    enemy_y = enemy_pos[1]

    if enemy_x >= player_x and (enemy_x < (player_x + player_size)) or player_x >= enemy_x and (player_x < (enemy_x+enemy_size)):
        if enemy_y >= player_y and (enemy_y < (player_y + player_size)) or player_y >= enemy_y and (player_y < (enemy_y+enemy_size)):
            return True
    return False
                            

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x = x - player_size
            elif event.key == pygame.K_RIGHT:
                x = x + player_size

            player_pos = [x,y]

    screen.fill(BACKGROUND_COLOR)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list , score)
    SPEED = setLevel(score , SPEED)
    
    text = "Score:" + str(score)
    label = myFont.render(text , 1 , YELLOW)
    screen.blit(label , (WIDTH-200 , HEIGHT-40))

    if collisionChecker(enemy_list , player_pos):
        game_over = True
        print("Your Final Score is:" , score)
        break

    draw_enemies(enemy_list)
    

    pygame.draw.rect(screen , RED , (player_pos[0], player_pos[1] , player_size , player_size))
 
    clock.tick(30)

    pygame.display.update()