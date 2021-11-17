import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,tx,ty,bullet_img, player, bullets, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.vel = vel
        self.x = tx
        self.y = ty
        self.player = player
        bullets.append(self)
        self.mx = x
        self.my = y
        self.dx = self.mx - self.x
        self.dy = self.my - self.y
        self.len = math.hypot(self.dx, self.dy)
        self.dx = self.dx / self.len
        self.dy = self.dy / self.len
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.duration = 0
        self.hit = []


    def update(self):
        self.rect.x += round(self.dx) * self.vel
        self.rect.y += round(self.dy) * self.vel

