import pygame
from Bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self,screen_width,screen_height,surface,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = screen_width/2
        self.y = screen_height/2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = surface
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.moveDelay = 0
        self.maxMoveDelay = 6
        self.damage = 2
        self.speed = 1
        self.maxHealth = 100
        self.shields = 0
        self.shieldcd = 0
        self.magSize = 10
        self.mag = 10
        self.health = self.maxHealth
        self.fullAuto = False
        self.upgrades = {"Damage":10,
                        "Full Auto":10,
                        "Piercing":10,
                        "DoT":10,
                        "Multi Shot":10,
                        "Explosive":10,
                        "Mag Size":10,
                        "Armor":0,
                        "Shields":0,
                        "Regen":0,
                        "Max Health":0,
                        "Speed":0,
                        "Bullet Speed":0,
                        "Slowing":0}

    def update(self):
        self.xvel = 0
        self.yvel = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.xvel -= self.speed
        if keystate[pygame.K_d]:
            self.xvel += self.speed
        if keystate[pygame.K_w]:
            self.yvel -= self.speed
        if keystate[pygame.K_s]:
            self.yvel += self.speed


        self.damage = 2 + (2*self.upgrades["Damage"])
        self.maxHealth = 100 + (50*self.upgrades["Max Health"])
        self.maxMoveDelay = 6 - self.upgrades["Speed"]
        if self.upgrades["Shields"] > 0:
            if self.shieldcd == 0:
                self.shields = self.upgrades["Shields"] * 50
                self.shieldcd = 10000
            if self.shields == 0:
                self.shieldcd -= 1
            if self.shields < 0:
                self.shields = 0
        if self.health < self.maxHealth:
            self.health += 0.002 * (self.upgrades["Regen"])




        if self.rect.x > self.screen_width - 32:
            self.rect.x = self.screen_width - 32
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > self.screen_height - 32:
            self.rect.y = self.screen_height - 32
        if self.rect.y < 0:
            self.rect.y = 0

        if self.moveDelay == 0:
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            self.moveDelay = self.maxMoveDelay

        if self.moveDelay > 0:
            self.moveDelay -= 1

        if self.shields < 0:
            self.shields = 0
        if self.health < 0:
            self.health = 0

        pygame.draw.rect(self.surface, (0, 0, 0), (10, 15, 200, 10))
        pygame.draw.rect(self.surface, (255, 0, 0), (10, 15, (self.health/self.maxHealth) * 200, 10))
        pygame.draw.rect(self.surface, (255,255,255), (10, 13, (self.shields/75) * 200, 2))



    def shoot(self,x,y,tx,ty,all_sprites,bullet_img,bullets):
        bullet = Bullet(x,y,tx,ty,bullet_img,self,bullets,1+(0.25*self.upgrades["Bullet Speed"]))
        all_sprites.add(bullet)

    def takeDamage(self,damage):
        if self.shields > 0:
            self.shields -= damage / (1 + (0.1*self.upgrades["Armor"]))
        else:
            self.health -= damage / (1 + (0.1 * self.upgrades["Armor"]))