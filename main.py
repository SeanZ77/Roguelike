import pygame
from random import randint
from os import path
from Player import Player
from Enemy import Enemy
from Enemy import RangedEnemy
from Enemy import TankEnemy
from Menu import Menu


pygame.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

display = pygame.display

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roguelike")

img_dir = path.dirname(__file__)
bullet_img = pygame.image.load(path.join(img_dir, "Bullet.png")).convert_alpha()
bullet_img = pygame.transform.smoothscale(bullet_img, (10, 10))
player_img = pygame.image.load(path.join(img_dir, "Player.png")).convert_alpha()
enemy_img = pygame.image.load(path.join(img_dir, "Enemy.png")).convert_alpha()
rangedEnemy_img = pygame.image.load(path.join(img_dir, "RangedEnemy.png")).convert_alpha()
tankEnemy_img = pygame.image.load(path.join(img_dir, "TankEnemy.png")).convert_alpha()
tankEnemy_img = pygame.transform.smoothscale(tankEnemy_img, (40, 40))
enemyBullet_img = pygame.image.load(path.join(img_dir, "EnemyBullet.png")).convert_alpha()
enemyBullet_img = pygame.transform.smoothscale(enemyBullet_img, (10, 10))


bullets = []
enemies = []
menuActive = False
level = 1


def newLevel():
    global level
    global enemies
    player.health = player.maxHealth
    level += 1
    x = round(0.5*(level ** 2))
    enemy = TankEnemy(randint(0, SCREEN_WIDTH - 32), randint(0, SCREEN_HEIGHT - 32), tankEnemy_img, player, window, enemies)
    enemies.append(enemy)
    all_sprites.add(enemy)
    for i in range(x):
        enemy = Enemy(randint(0,SCREEN_WIDTH-32),randint(0,SCREEN_HEIGHT-32),enemy_img,player,window)
        enemies.append(enemy)
        all_sprites.add(enemy)




all_sprites = pygame.sprite.Group()

menu = Menu()
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT,window,player_img)
enemy = Enemy(100,100,enemy_img,player,window)

all_sprites.add(player)
all_sprites.add(enemy)
enemies.append(enemy)

pygame.event.get()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            if len(enemies) > 0:
                if "Multi Shot" in player.upgrades:
                    player.shoot(mouseX, mouseY, player.rect.x, player.rect.y+16, all_sprites, bullet_img, bullets)
                    player.shoot(mouseX, mouseY, player.rect.x + 32, player.rect.y + 16, all_sprites, bullet_img, bullets)
                else:
                    player.shoot(mouseX, mouseY, player.rect.x + 16, player.rect.y + 16, all_sprites, bullet_img, bullets)

            if menuActive:
                if len(menu.powerUpgrades) > 0:
                    if menu.button1XY[0] <= mouseX <= menu.button1XY[0] + 100 and menu.button1XY[1] <= mouseY <= menu.button1XY[1] + 50:
                        player.upgrades[menu.powerUpgrade] += 1
                        menu.powerUpgrade = None
                        newLevel()
                if len(menu.healthUpgrades) > 0:
                    if menu.button2XY[0] <= mouseX <= menu.button2XY[0] + 100 and menu.button2XY[1] <= mouseY <= menu.button2XY[1] + 50:
                        player.upgrades[menu.healthUpgrade] += 1
                        menu.healthUpgrade = None
                        newLevel()

                if len(menu.miscUpgrades) > 0:
                    if menu.button3XY[0] <= mouseX <= menu.button3XY[0] + 100 and menu.button3XY[1] <= mouseY <= menu.button3XY[1] + 50:
                        player.upgrades[menu.miscUpgrade] += 1
                        menu.miscUpgrade = None
                        newLevel()


    for i in bullets:
        if i.duration >= 2000:
            bullets.remove(i)
            i.kill()
            all_sprites.remove(i)

        if len(enemies) > 0:
            for j in enemies:
                if i.rect.colliderect(j.rect):
                    if j not in i.hit:
                        if j.reduction:
                            j.health -= player.damage/2
                        else:
                            j.health -= player.damage
                        i.hit.append(j)
                        if j.health <= 0:
                            enemies.remove(j)
                            all_sprites.remove(j)
                            j.kill()


                    if "Piercing" not in player.upgrades:
                        if i in bullets:
                            bullets.remove(i)
                            all_sprites.remove(i)
                            i.kill()
                        break

    for i in range(len(enemies)):
        if enemies[i].__class__.__name__ == "RangedEnemy":
            for j in enemies[i].bullets:
                if j.rect.colliderect(player):
                    j.kill()
                    all_sprites.remove(j)
                    enemies[i].bullets.remove(j)
                    player.health -= 10
                if j.duration > 2000:
                    j.kill()
                    all_sprites.remove(j)
                    enemies[i].bullets.remove(j)

        for j in range(i,len(enemies)):
            if enemies[i].rect.colliderect(enemies[j].rect):
                r = randint(0,1)
                if r == 0:
                    enemies[i].rect.x -= 1
                    enemies[j].rect.x += 1
                if r == 1:
                    enemies[i].rect.y -= 1
                    enemies[j].rect.y += 1



    window.fill((0, 150, 205))
    all_sprites.draw(window)
    all_sprites.update()


    if len(enemies) == 0:
        menuActive = True
    else:
        menuActive = False

    if menuActive:
        if menu.powerUpgrade is None:
            menu.generateUpgrade("Power")
        if menu.healthUpgrade is None:
            menu.generateUpgrade("Health")
        if menu.miscUpgrade is None:
            menu.generateUpgrade("Misc")
        menu.update(window,player)



    pygame.display.flip()
