from Button import Button
import pygame
import random

class Menu():
    def __init__(self):
        self.button1XY = [280, 335]
        self.button2XY = [430, 335]
        self.button3XY = [580, 335]
        self.button1 = Button(self.button1XY[0], self.button1XY[1])
        self.button2 = Button(self.button2XY[0], self.button2XY[1])
        self.button3 = Button(self.button3XY[0], self.button3XY[1])
        self.powerUpgrades = ["Damage", "Full Auto", "Piercing", "DoT","Multi Shot","Explosive","Mag Size"]
        self.healthUpgrades = ["Armor", "Shields", "Regen", "Max Health"]
        self.miscUpgrades = ["Speed", "Bullet Speed", "Slowing"]
        self.powerUpgrade = None
        self.healthUpgrade = None
        self.miscUpgrade = None


    def draw_text(self, surf, text, size, color, x, y):
        font_name = pygame.font.match_font('bahnschrift')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def generateUpgrade(self, upgrade):
        if upgrade == "Power":
            self.powerUpgrade = random.choice(self.powerUpgrades)
        elif upgrade == "Health":
            self.healthUpgrade = random.choice(self.healthUpgrades)
        elif upgrade == "Misc":
            self.miscUpgrade = random.choice(self.miscUpgrades)

    def update(self,window):

        self.button1.draw(window)
        self.button2.draw(window)
        self.button3.draw(window)

        self.draw_text(window, "Power", 17, (0, 0, 0), 330, 338)

        if len(self.powerUpgrades) > 0:
            self.draw_text(window, self.powerUpgrade, 15, (0, 0, 0), 330, 358)
        else:
            self.draw_text(window, "Maxed", 16, (0, 0, 0), 330, 358)

        self.draw_text(window, "Health", 17, (0, 0, 0), 480, 338)

        if len(self.healthUpgrades) > 0:
            self.draw_text(window, self.healthUpgrade, 15, (0, 0, 0), 480, 358)
        else:
            self.draw_text(window, "Maxed", 16, (0, 0, 0), 480, 358)
        self.draw_text(window, "Misc.", 17, (0, 0, 0), 630, 338)

        if len(self.miscUpgrades) > 0:
            self.draw_text(window, self.miscUpgrade, 15, (0, 0, 0), 630, 358)
        else:
            self.draw_text(window, "Maxed", 16, (0, 0, 0), 630, 358)

