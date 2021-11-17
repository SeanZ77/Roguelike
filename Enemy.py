import pygame
from Bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,image,player,window):
        pygame.sprite.Sprite.__init__(self)

        self.target = player
        self.window = window
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.moveDelay = 0
        self.delay = 10
        self.health = 10
        self.maxHealth = 10
        self.damage = 0.01
        self.reduction = False

    def update(self):
        self.xvel = 0
        self.yvel = 0

        if abs(self.rect.x - self.target.rect.x) < 15 and abs(self.rect.y - self.target.rect.y) < 15:
            self.target.takeDamage(self.damage)

        if self.rect.x < self.target.rect.x:
            self.xvel += 1
        if self.rect.x > self.target.rect.x:
            self.xvel -= 1
        if self.rect.y < self.target.rect.y:
            self.yvel += 1
        if self.rect.y > self.target.rect.y:
            self.yvel -= 1

        if self.moveDelay == 0:
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            self.moveDelay = self.delay

        if self.moveDelay > 0:
            self.moveDelay -= 1

        pygame.draw.rect(self.window, (255, 0, 0), (self.rect.x+self.rect.width/2-15, self.rect.y - 10, 30*(self.health/self.maxHealth), 5))


class RangedEnemy(Enemy):
    def __init__(self,x,y,image,player,window,all_sprites,bullet_img):
        super().__init__(x,y,image,player,window)
        self.bullets = []
        self.all_sprites = all_sprites
        self.bullet_img = bullet_img
        self.shootCd = 0



    def update(self):
        self.xvel = 0
        self.yvel = 0

        if abs(self.rect.x - self.target.rect.x) < 200 and abs(self.rect.y - self.target.rect.y) < 200:
            if self.shootCd == 0:
                self.shoot(self.target.rect.x,self.target.rect.y,self.rect.x+16,self.rect.y+16,self.all_sprites,self.bullet_img,self.bullets)
                self.shootCd = 3000


        if self.rect.x < self.target.rect.x:
            self.xvel += 1
        if self.rect.x > self.target.rect.x:
            self.xvel -= 1
        if self.rect.y < self.target.rect.y:
            self.yvel += 1
        if self.rect.y > self.target.rect.y:
            self.yvel -= 1

        if self.moveDelay == 0:
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            self.moveDelay = self.delay

        if self.moveDelay > 0:
            self.moveDelay -= 1

        pygame.draw.rect(self.window, (255, 0, 0), (self.rect.x+1, self.rect.y - 10, 30*(self.health/10), 5))

        if self.shootCd > 0:
            self.shootCd -= 1


    def shoot(self,x,y,tx,ty,all_sprites,bullet_img,bullets):
        bullet = Bullet(x,y,tx,ty,bullet_img,self,bullets,1)
        all_sprites.add(bullet)




class TankEnemy(Enemy):
    def __init__(self,x,y,image,player,window,enemies):
        super().__init__(x,y,image,player,window)
        self.delay = 30
        self.health = 50
        self.maxHealth = 50
        self.damage = 0.005
        self.enemies = enemies


    def update(self):
        self.xvel = 0
        self.yvel = 0

        if abs(self.rect.x - self.target.rect.x) < 15 and abs(self.rect.y - self.target.rect.y) < 15:
            if self.target.shields > 0:
                if "Dmg Reduction" in self.target.upgrades:
                    self.target.shields -= self.damage/1.2
                else:
                    self.target.shields -= self.damage
            else:
                if "Dmg Reduction" in self.target.upgrades:
                    self.target.health -= self.damage/1.2
                else:
                    self.target.health -= self.damage


        for i in self.enemies:
            if self.rect.x - 100 < i.rect.x < self.rect.right + 100 and self.rect.y - 100 < i.rect.y < self.rect.bottom + 100:
                if i.__class__.__name__ != "TankEnemy":
                    i.reduction = True
            else:
                i.reduction = False

        if self.rect.x < self.target.rect.x:
            self.xvel += 1
        if self.rect.x > self.target.rect.x:
            self.xvel -= 1
        if self.rect.y < self.target.rect.y:
            self.yvel += 1
        if self.rect.y > self.target.rect.y:
            self.yvel -= 1

        if self.moveDelay == 0:
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            self.moveDelay = self.delay

        if self.moveDelay > 0:
            self.moveDelay -= 1

        s = pygame.Surface((240, 240))
        s.set_alpha(50)
        s.fill((0, 0, 0))
        self.window.blit(s, (self.rect.x-100, self.rect.y-100))

        pygame.draw.rect(self.window, (255, 0, 0), (self.rect.x+self.rect.width/2-15, self.rect.y - 10, 30*(self.health/self.maxHealth), 5))
