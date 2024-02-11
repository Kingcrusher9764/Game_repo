import pygame

class Button():
    def __init__(self, x, y, image, scale, screen):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect(center = (x,y))
        self.click = False
        self.screen = screen
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.click!=True:
                self.click = True
                action = True
        if pygame.mouse.get_pressed()[0]==0:
            self.click = False
        self.screen.blit(self.image,self.rect)
        return action

