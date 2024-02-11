import pygame, sys,time
import json
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from menu import *
from database_conn import update, scores, update_controls
from leaderboard import Board
from aboutScreen import About
from settingScreen import SettingScreen

class Game:
	def __init__(self):

		# game attributes
		self.max_level = max_level
		self.max_health = 100
		self.cur_health = health
		self.coins = coins

		# audio 
		self.level_bg_music = pygame.mixer.Sound('assets/audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('assets/audio/overworld_music.wav')
		self.level_bg_music.set_volume(0.25)
		self.overworld_bg_music.set_volume(0.25)

		# overworld creation
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.status = 'overworld'

		# user interface 
		self.ui = UI(screen)

	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
		self.status = 'level'
		if(music!=0):
			self.overworld_bg_music.stop()
			self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		else:
			end_menu = True
			game_pause = True
			replay_button = Button(screen_width//2,(screen_height//4)+61,replay,0.30,screen)
			home_button = Button(screen_width//2,(screen_height//4)+(122+61), home,0.30, screen)
			while(end_menu):
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						with open("dataset.json", "w") as f:
							data = {
								"start_game": 0,
								"max_level": self.max_level,
								"health": self.cur_health,
								"coins": self.coins
							}
							json.dump(data, f)
						update(name, self.max_level, self.cur_health, self.coins)
						pygame.quit()
						sys.exit()
					
				if(game_pause):
					screen.blit(bg,bg_rect)
					if replay_button.draw():
						end_menu = False
						self.create_level(current_level)
					if home_button.draw():
						game.status = "overworld"
						end_menu = False
						game_pause = False	
						if(music!=0):	
							game.overworld_bg_music.play(loops = -1)
							game.level_bg_music.stop()
						game.run()
				pygame.display.update()
				clock.tick(60)
			return
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		if(music!=0):
			self.overworld_bg_music.play(loops = -1)
			self.level_bg_music.stop()

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount

	def check_game_over(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = max(0, self.coins - 100)
			self.max_level = max(0, self.max_level - 1)
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'
			if(music!=0):
				self.level_bg_music.stop()
				self.overworld_bg_music.play(loops = -1)

	def run(self):
		if self.status == 'overworld':
			with open("dataset.json", "w") as f:
				data = {
					"start_game": 1,
					"max_level": self.max_level,
					"health": self.cur_health,
					"coins": self.coins
				}
				json.dump(data, f)
			update(name, self.max_level, self.cur_health, self.coins)
			global left_key, jump_key, right_key, music
			left_key, jump_key, right_key, music = self.overworld.run(left_key, jump_key, right_key, music)
			
		else:
			self.level.run(left_key, jump_key, right_key)
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()

def startGameScreen(screen):
	screen.fill("grey")
	screen.blit(bg_img, bg_img_rect)
	# screen.blit(msg2, msg2_rect)
	screen.blit(icon_img, icon_img_rect)
	screen.blit(msg3, msg3_rect)
	if(start_button.draw()):
		global start_game, load_scr
		start_game = True
		load_scr = True
	if(setting_button.draw()):
		global left_key, right_key, jump_key, music
		ss = SettingScreen(left_key, jump_key, right_key, music)
		left_key, jump_key, right_key, music = ss.run()
	if(about_button.draw()):
		scr = About()
		scr.run()
		screen = pygame.display.set_mode((screen_width,screen_height))
	if(leaderboard_button.draw()):
		arr = scores()
		scr = Board()
		scr.run(arr)
		screen = pygame.display.set_mode((screen_width,screen_height))

# Pygame setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Georgia', 40, True)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Piratechopper")
clock = pygame.time.Clock()

# Start screen assets
icon_img = pygame.image.load("icon_img.png").convert_alpha()
icon_img = pygame.transform.rotozoom(icon_img, 0, 3)
icon_img_rect = icon_img.get_rect(center = (screen_width//3, (2.5*screen_height)//4+50))

play = pygame.image.load("assets\graphics\label_button1\play.png").convert_alpha()
about = pygame.image.load("assets\graphics\label_button1\About.png").convert_alpha()
leaderboard = pygame.image.load("assets\graphics\label_button1\leaderboard.png").convert_alpha()
setting_img = pygame.image.load("assets/graphics/button/settings-img.png").convert_alpha()

bg_img = pygame.image.load("assets\graphics\label_button1\game_background.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))
bg_img_rect = bg_img.get_rect(center=(screen_width//2,screen_height//2))
msg2 = my_font.render("Welcome to PirateChopper", False, (54,50,50))
msg2_rect = msg2.get_rect(center=((screen_width)//3,(screen_height)//4))
msg3 = pygame.image.load("assets\graphics\label_button1\msg_image.png").convert_alpha()
msg3_rect = msg3.get_rect(center=(390, 220))

start_button = Button((3*screen_width)//4,50+screen_height//4,play,0.5,screen)
about_button = Button(20+(3*screen_width)//4,160+(2*screen_height)//4,about,0.5,screen)
leaderboard_button = Button(100+(3*screen_width)//4,screen_height//4-120,leaderboard,0.3,screen)
setting_button = Button(50,50,setting_img,0.2,screen)

# data of player
with open("dataset.json") as f:
	data = json.load(f)
	start_game = data["start_game"]
	max_level = data["max_level"]
	health = data["health"]
	coins = data["coins"]
	name = data["name"]
	music = data["music"]
	jump_key = data["jump_key"]
	right_key = data["right_key"]
	left_key = data["left_key"]
game_pause = False
load_scr = False
end_menu = False

# menu
resume = pygame.image.load("assets\graphics\label_button1\Resume1.png").convert_alpha()
resume_button = Button(screen_width//2-10,(screen_height//4)+122,resume,0.30,screen)
home = pygame.image.load("assets\graphics\label_button1\home1.png").convert_alpha()
home_button = Button(screen_width//2,(screen_height//4)+(2*122), home,0.30, screen)
replay = pygame.image.load("assets\graphics\label_button1\Replay1.png").convert_alpha()
replay_button = Button(screen_width//2,(screen_height//4),replay,0.30,screen)
bg = pygame.image.load("assets\graphics\label_button1\menu_background.png").convert_alpha()
bg = pygame.transform.scale(bg,(0.8*bg.get_width(),0.8*bg.get_height()))
bg_rect = bg.get_rect(center=(screen_width//2,screen_height//2-55))

game = Game()
# start screen
while (start_game!=True):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			update_controls(name, jump_key, left_key, right_key, music)
			pygame.quit()
			sys.exit()
		
	startGameScreen(screen)
	pygame.display.update()
	clock.tick(60)

curr_time = time.time()
# load screen
while(load_scr):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pgs = time.time()-curr_time
	if(pgs>=2):
		load_scr = False
	screen.fill("black")
	load_msg = my_font.render("Loading........", False, "white")
	msg_rect = load_msg.get_rect(center=((screen_width)//3,(screen_height)//4))
	screen.blit(load_msg, msg_rect)

	# progress bar
	bar_height = 60
	bar_width = 3*(screen_width)//4

	fill = (pgs/2)*bar_width
	x = screen_width//2 - bar_width//2
	y = screen_height//2 - bar_height

	fill_rect = pygame.Rect(x, y, fill, bar_height)
	outline_rect = pygame.Rect(x-10, y-10, bar_width+20, bar_height+20)
	pygame.draw.rect(screen, "white", fill_rect)
	pygame.draw.rect(screen, "white", outline_rect, 2)

	pygame.display.update()
	clock.tick(60)
# time.sleep(1)
# main game
if(music!=0):
	game.overworld_bg_music.play(loops = -1)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# update_data("txt1.txt","start_game","0")
			with open("dataset.json", "w") as f:
				data = {
					"start_game": 0,
					"max_level": game.max_level,
					"health": game.cur_health,
					"coins": game.coins
				}
				json.dump(data, f)
			update(name, game.max_level, game.cur_health, game.coins)
			update_controls(name, jump_key, left_key, right_key, music)
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_p and (game_pause==False) and game.status=="level":
				game_pause = True
	if(game_pause):
		screen.blit(bg,bg_rect)
		if replay_button.draw():
			game_pause = False
			game.create_level(game.level.current_level)
		if resume_button.draw():
			game_pause=False
		if home_button.draw():
			game.status = "overworld"
			game_pause = False
			if(music!=0):
				game.level_bg_music.stop()
				game.overworld_bg_music.play(loops = -1)
			game.run()
	else:
		screen.fill('grey')
		game.run()

	pygame.display.update()
	clock.tick(60)