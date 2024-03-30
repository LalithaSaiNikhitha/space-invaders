
import pygame
import random
import math
from pygame import mixer

# Initializing pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Title & icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

# Background image
background = pygame.image.load('bg.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player space shuttle
playerimg = pygame.image.load('ship.png')
playerx = 370
playery = 480
player_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemy_changex = []
enemy_changey = []
no_of_elements = 8

for i in range(no_of_elements):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemy_changex.append(0.3)
    enemy_changey.append(40)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bullet_changex = 0
bullet_changey = 0.7
bullet_state = "ready"  # ready --> you can't see bullet on screen, fire --> bullet moving

# Score
score_value = 0
font = pygame.font.Font('font.ttf', 22)
textx = 16
texty = 16


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 15))


def is_collision(bulletx, bullety, enemyx, enemyy):
    distance = math.sqrt(math.pow((bulletx - enemyx), 2) + (math.pow((bullety - enemyy), 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop

running = True
while running:
    # Changing background screen color
    screen.fill((0, 0, 0))  # RGB value: Red, green, blue

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key pressed & released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_change = 0.3
            elif event.key == pygame.K_LEFT:
                player_change = -0.3
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of spaceship
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_change = 0

    playerx += player_change

    # Setting boundaries for spaceship
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # Enemy movement
    for i in range(no_of_elements):
        if enemyy[i] > 440:
            for j in range(no_of_elements):
                enemyy[j] = 2000
            over_font = pygame.font.Font('font.ttf', 80)
            over_text = over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_text, (150, 250))
            break

        enemyx[i] += enemy_changex[i]
        if enemyx[i] <= 0:
            enemy_changex[i] = 0.3
            enemyy[i] += enemy_changey[i]
        elif enemyx[i] >= 736:
            enemy_changex[i] = -0.3
            enemyy[i] += enemy_changey[i]

        # collision
        collision = is_collision(bulletx, bullety, enemyx[i], enemyy[i])
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullety = 480
            bullet_state = "ready"
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(45, 100)
            score_value += 1
        enemy(enemyx[i], enemyy[i], i)

    # bullet
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullet_changey

    show_score(textx, texty)
    player(playerx, playery)
    pygame.display.update()
