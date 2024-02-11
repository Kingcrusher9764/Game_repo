import pygame, sys
from settings import screen_width, screen_height

class About:
    def __init__(self):
        # self.swid = swidth
        # self.shei = sheight
        self.base_font=pygame.font.Font(None, 50)
        self.width = screen_width
        self.height = screen_height
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        
        self.bg = pygame.image.load("assets/leaderboard/About.png").convert_alpha()
        # self.bg = pygame.transform.rotozoom(self.bg,0,1.7)
        self.bg_rect = self.bg.get_rect(center=(self.width//2, self.height//2))

        self.bg_ig = pygame.image.load("assets/leaderboard/bg_ig2.jpg")
        self.bg_ig = pygame.transform.scale(self.bg_ig, (screen_width,screen_height))
        # self.bg_ig = pygame.image.load("assets/leaderboard/i3.jpg")
        # self.bg_ig = pygame.transform.rotozoom(self.bg_ig,0,1)
        self.bg_ig_rect = self.bg_ig.get_rect(center=(self.width//2,self.height//2))
        self.close = pygame.image.load("assets/leaderboard/closeb.png").convert_alpha()
        self.close = pygame.transform.scale(self.close, (50,50))
        self.close_rect = self.close.get_rect(center=(self.width-130,self.height//6-30))
    def draw_text(self, text, color, x, y):
        textbox = self.base_font.render(text,True, color)
        self.screen.blit(textbox,(x,y))

    def run(self):
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
            
            pygame.display.update()
            self.clock.tick(60)
