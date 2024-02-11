import pygame, sys
from settings import screen_width, screen_height

class Board:
    def __init__(self):
        self.base_font=pygame.font.Font(None, 50)
        self.width = screen_width
        self.height = screen_height
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        self.bg = pygame.image.load("assets/leaderboard/leadboard1.png").convert_alpha()
        self.bg_rect = self.bg.get_rect(center=(self.width//2,self.height//2))
        self.bg_ig = pygame.image.load("assets/leaderboard/bg_ig2.jpg")
        self.bg_ig = pygame.transform.scale(self.bg_ig, (screen_width,screen_height))
        self.bg_ig_rect = self.bg_ig.get_rect(center=(self.width//2,self.height//2))
        self.close = pygame.image.load("assets/leaderboard/closeb.png").convert_alpha()
        self.close = pygame.transform.scale(self.close, (50,50))
        self.close_rect = self.close.get_rect(center=(self.width-130,self.height//6-30))
    def draw_text(self, text, color, x, y):
        textbox = self.base_font.render(text,True, color)
        self.screen.blit(textbox,(x,y))

    def run(self, arr):
        state = True
        while(state):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    state = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.close_rect.collidepoint(pygame.mouse.get_pos()):
                        state = False
            self.screen.fill("grey")
            self.screen.blit(self.bg_ig,self.bg_ig_rect)
            self.screen.blit(self.bg, self.bg_rect)
            self.screen.blit(self.close, self.close_rect)
            for i in range(len(arr)):
                txt = f"{arr[i]['name']}"
                self.draw_text(txt,"Black", (self.width//4)-50,80+(self.height//4)+(i*75))
                self.draw_text(f"{arr[i]['coins']}", "Black", 450+(self.width//4), 80+(self.height//4)+(i*75))
            pygame.display.update()
            self.clock.tick(60)
