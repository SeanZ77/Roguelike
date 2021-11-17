import pygame
class Button():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hovered = False


    def draw(self,window):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        if mouseX >= self.x and mouseX <= self.x + 100 and mouseY >= self.y and mouseY <= self.y + 50:
            pygame.draw.rect(window, (200, 200, 200), (self.x, self.y, 100, 50))
        else:
            pygame.draw.rect(window, (150, 150, 150), (self.x, self.y, 100, 50))

