import pygame as pg
import time, random, math, os
from pygame import mixer

# Initalize the pygame
pg.init()

# Create the screen
screen_height = 600
screen_width = 800

screen = pg.display.set_mode((screen_width, screen_height))

# Title and icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load("Icon32x32.png")
pg.display.set_icon(icon)

# Player Image
playerImg = pg.image.load("Fighter64x64.png")

# Enemy Image
#enemyImg = pg.image.load("final.png")
enemyImg = []

# Background Image
backgroundImg = pg.image.load("Background.jpg")

# Backgroud Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Bullet Image
bulletImg = pg.image.load("Bullet32x32.png")

# Player initial position
player_pos_x = 370
player_pos_y = 500
playerX_change = 0

# Enemies initial position
enemy_pos_x = []
enemy_pos_y = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for e in range(num_of_enemies):
    enemyImg.append(pg.image.load("final.png"))
    enemy_pos_x.append(random.randint(70, screen_width - 70))
    enemy_pos_y.append(random.randint(10, screen_height - 250))
    enemyX_change.append(1)
    enemyY_change.append(5)

# Bullet position
bullet_pos_x = 0
bullet_pos_y = 500
bulletX_change = 0
bulletY_change = 10
# "ready" - Not visible on the screen
# "fire" - The bullet is currently moving
bullet_state = "ready"




# Score
score = 0
font = pg.font.Font("freesansbold.ttf", 32)
text_pos_x = 10
text_pos_y = 10

# Bullet distance from enemy
bullet_distance = "---"

# Game Over
overFont = pg.font.Font("freesansbold.ttf", 64)
def game_over_text():
    over_text = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250)) 

def show_score(x, y):
    sc = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(sc, (x, y))

def player(playerX, playerY):
    screen.blit(playerImg, (playerX, playerY))

def enemy(enemyI, enemyX, enemyY):
    screen.blit(enemyI, (enemyX, enemyY))

def fire_bullet(bulletX, bulletY):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (bulletX + 16, bulletY + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt( math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    global bullet_distance
    bullet_distance = distance
    if distance <= 27:
        return True
    return False

def Logs(player, enemy, bullet, distance_t):
    print("Player x:{} y:{}".format(player[0], player[1]))
    print("Enemy x:{} y:{}".format(enemy[0], enemy[1]))
    print("Bullet: x:{} y:{}".format(bullet[0], bullet[1]))
    print("Distance: {}".format(distance_t))
    os.system("cls")

# Game Loop
running = True
while running:
    # Set background Color (RGB)
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # if keystroke is pressed check whether its right or left
        if event.type == pg.KEYDOWN:
            
            if event.key == pg.K_LEFT:
                # Move Left
                playerX_change = -5
            
            if event.key == pg.K_RIGHT:
                # Move right
                playerX_change = 5
            
            if event.key == pg.K_SPACE:
                # Fire bullet
                if bullet_state == "ready":
                    # Get the current x-axis of the spaceship
                    bullet_pos_x = player_pos_x
                    # Bullet Sound
                    b_sound = mixer.Sound("laser.wav")
                    b_sound.play()
                    fire_bullet(bullet_pos_x, bullet_pos_y)
               
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0
           
    player_pos_x += playerX_change

    # If outside the window no change
    if screen_width <= player_pos_x + 64 or 0 > player_pos_x:
        player_pos_x -= playerX_change

    # Bullet Movement
    if bullet_pos_y <= 0:
        bullet_pos_y = 500
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_pos_x, bullet_pos_y)
        bullet_pos_y -= bulletY_change

    
    # Change enemy position
    for e in range(num_of_enemies):

        if enemy_pos_y[e] > player_pos_y - 50:
            for j in range(num_of_enemies):
                enemy_pos_y[j] = 2000
            game_over_text()
            break

        enemy_pos_x[e] += enemyX_change[e]
        if screen_width - 64 <= enemy_pos_x[e] :
            enemyX_change[e] = -1
            enemy_pos_y[e] += 30
            

        elif 0 > enemy_pos_x[e]:
            enemyX_change[e] = 1
            enemy_pos_y[e] += 30
            
        enemy(enemyImg[e], enemy_pos_x[e], enemy_pos_y[e])

        # Collision

        collision = isCollision(enemy_pos_x[e], enemy_pos_y[e], bullet_pos_x, bullet_pos_y)

        if collision:
            explosion = mixer.Sound("explosion.wav")
            explosion.play()
            bullet_pos_y = 500
            bullet_state = "ready"
            score += 1
            print("Score:",score, end = "\r")
            enemy_pos_x[e] = random.randint(70, screen_width - 70)
            enemy_pos_y[e] = random.randint(10, screen_height - 250)
    
    #Logs((player_pos_x, player_pos_y), (enemy_pos_x, enemy_pos_y), (bullet_pos_x, bullet_pos_y), bullet_distance)

    player(player_pos_x, player_pos_y)
    show_score(text_pos_x, text_pos_y)

    pg.display.update()
    pg.time.Clock().tick()
    print("FPS:",pg.time.Clock().get_fps())
    