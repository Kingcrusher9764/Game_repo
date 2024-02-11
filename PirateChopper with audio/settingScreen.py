import pygame, sys
from settings import screen_width, screen_height
from menu import Button

class SettingScreen:
    def __init__(self, left_i, jump_i, right_i, music_i):
        # self.swid = swidth
        # self.shei = sheight
        self.base_font=pygame.font.Font(None, 50)
        self.width = screen_width
        self.height = screen_height
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        
        self.bg = pygame.image.load("assets/leaderboard/setting.png").convert_alpha()
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

        self.vol_l = pygame.Rect(560,229,608-560, 278-229)
        self.vol_r = pygame.Rect(939,229,987-939, 278-229)
        self.jump_l = pygame.Rect(560,372,608-560, 425-374)
        self.jump_r = pygame.Rect(939,372,608-560, 278-229)
        self.moveL_l = pygame.Rect(560,429,608-560, 278-229)
        self.moveL_r = pygame.Rect(939,429,608-560, 278-229)
        self.moveR_l = pygame.Rect(560,483,608-560, 278-229)
        self.moveR_r = pygame.Rect(944,483,608-560, 278-229)

        self.vol_text = ["OFF", "ON"]
        self.jump_text = ["Spacebar-key", "key-W", "UP-arrow-key"]
        self.moveL_text = ["Left-arrow-key", "key-A"]
        self.moveR_text = ["Right-arrow-key", "key-D"]

        self.vol_idx = music_i
        self.jump_idx = jump_i
        self.moveL_idx = left_i
        self.moveR_idx = right_i

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
                    if(self.vol_l.collidepoint(pygame.mouse.get_pos())):
                        self.vol_idx -= 1
                        if self.vol_idx<0:
                            self.vol_idx = len(self.vol_text)-1

                    if(self.vol_r.collidepoint(pygame.mouse.get_pos())):
                        self.vol_idx += 1
                        if(self.vol_idx>=len(self.vol_text)):
                            self.vol_idx = 0
                        
                    if(self.jump_l.collidepoint(pygame.mouse.get_pos())):
                        self.jump_idx -= 1
                        if self.jump_idx<0:
                            self.jump_idx = len(self.jump_text)-1
                        
                    if(self.jump_r.collidepoint(pygame.mouse.get_pos())):
                        self.jump_idx += 1
                        if(self.jump_idx>=len(self.jump_text)):
                            self.jump_idx = 0
                        
                    if(self.moveR_l.collidepoint(pygame.mouse.get_pos())):
                        self.moveR_idx -= 1
                        if self.moveR_idx<0:
                            self.moveR_idx = len(self.moveR_text)-1
                        
                    if(self.moveR_r.collidepoint(pygame.mouse.get_pos())):
                        self.moveR_idx += 1
                        if(self.moveR_idx>=len(self.moveR_text)):
                            self.moveR_idx = 0
                        
                    if(self.moveL_l.collidepoint(pygame.mouse.get_pos())):
                        self.moveL_idx -= 1
                        if self.moveL_idx<0:
                            self.moveL_idx = len(self.moveL_text)-1
                        
                    if(self.moveL_r.collidepoint(pygame.mouse.get_pos())):
                        self.moveL_idx += 1
                        if(self.moveL_idx>=len(self.moveL_text)):
                            self.moveL_idx = 0
                        
                        
            self.screen.fill("grey")
            self.screen.blit(self.bg_ig,self.bg_ig_rect)
            self.screen.blit(self.bg, self.bg_rect)
            self.screen.blit(self.close, self.close_rect)
            self.draw_text(self.vol_text[self.vol_idx], "Black", 740, 240)
            self.draw_text(self.jump_text[self.jump_idx], "Black", 640, 380)
            self.draw_text(self.moveL_text[self.moveL_idx], "Black", 640, 440)
            self.draw_text(self.moveR_text[self.moveR_idx], "Black", 640, 490)
            
            pygame.display.update()
            self.clock.tick(60)
        return [self.moveL_idx, self.jump_idx, self.moveR_idx, self.vol_idx]