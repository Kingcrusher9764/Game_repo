import pygame, sys, time
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
    def __init__(
        self,
        max_level,
        health,
        coins,
        screen,
        name,
        left_key,
        jump_key,
        right_key,
        game_pause,
        load_scr,
        end_menu,
        resume,
        home,
        replay,
        bg,
        bg_rect,
        clock,
    ):
        self.clock = clock
        self.bg = bg
        self.bg_rect = bg_rect
        self.replay = replay
        self.home = home
        self.resume = resume
        self.load_scr = load_scr
        self.end_menu = end_menu
        self.game_pause = game_pause
        self.left_key = left_key
        self.jump_key = jump_key
        self.right_key = right_key
        # game attributes
        self.name = name
        self.max_level = max_level
        self.max_health = 100
        self.cur_health = health
        self.coins = coins
        self.screen = screen

        # overworld creation
        self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
        self.status = "overworld"

        # user interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(
            current_level,
            self.screen,
            self.create_overworld,
            self.change_coins,
            self.change_health,
        )
        self.status = "level"

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        else:
            end_menu = True
            game_pause = True
            replay_button = Button(
                screen_width // 2,
                (screen_height // 4) + 61,
                self.replay,
                0.30,
                self.screen,
            )
            home_button = Button(
                screen_width // 2,
                (screen_height // 4) + (122 + 61),
                self.home,
                0.30,
                self.screen,
            )
            while end_menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        with open("dataset.json", "w") as f:
                            data = {
                                "start_game": 0,
                                "max_level": self.max_level,
                                "health": self.cur_health,
                                "coins": self.coins,
                            }
                            json.dump(data, f)
                        update(self.name, self.max_level, self.cur_health, self.coins)
                        pygame.quit()
                        sys.exit()

                if game_pause:
                    self.screen.blit(self.bg, self.bg_rect)
                    if replay_button.draw():
                        end_menu = False
                        self.create_level(current_level)
                    if home_button.draw():
                        self.status = "overworld"
                        end_menu = False
                        game_pause = False
                        self.run()
                pygame.display.update()
                self.clock.tick(60)
            return
        self.overworld = Overworld(
            current_level, self.max_level, self.screen, self.create_level
        )
        self.status = "overworld"

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = max(0, self.coins - 100)
            self.max_level = max(0, self.max_level - 1)
            self.overworld = Overworld(
                0, self.max_level, self.screen, self.create_level
            )
            self.status = "overworld"

    def run(self):
        if self.status == "overworld":
            with open("dataset.json", "w") as f:
                data = {
                    "start_game": 1,
                    "max_level": self.max_level,
                    "health": self.cur_health,
                    "coins": self.coins,
                }
                json.dump(data, f)
            update(self.name, self.max_level, self.cur_health, self.coins)
            # global left_key, jump_key, right_key
            self.left_key, self.jump_key, self.right_key = self.overworld.run(
                self.left_key, self.jump_key, self.right_key
            )
        else:
            self.level.run(self.left_key, self.jump_key, self.right_key)
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


class MainGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont("Georgia", 40, True)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Piratechopper")
        self.clock = pygame.time.Clock()

        # Start screen assets
        self.icon_img = pygame.image.load("icon_img.png").convert_alpha()
        self.icon_img = pygame.transform.rotozoom(self.icon_img, 0, 3)
        self.icon_img_rect = self.icon_img.get_rect(
            center=(screen_width // 3, (2.5 * screen_height) // 4 + 50)
        )
        self.play = pygame.image.load(
            "assets\graphics\label_button1\play.png"
        ).convert_alpha()
        self.about = pygame.image.load(
            "assets\graphics\label_button1\About.png"
        ).convert_alpha()
        self.leaderboard = pygame.image.load(
            "assets\graphics\label_button1\leaderboard.png"
        ).convert_alpha()
        self.setting_img = pygame.image.load(
            "assets/graphics/button/settings-img.png"
        ).convert_alpha()
        self.bg_img = pygame.image.load(
            "assets\graphics\label_button1\game_background.png"
        ).convert_alpha()
        self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))
        self.bg_img_rect = self.bg_img.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        self.msg2 = self.my_font.render("Welcome to PirateChopper", False, (54, 50, 50))
        self.msg2_rect = self.msg2.get_rect(
            center=((screen_width) // 3, (screen_height) // 4)
        )
        self.msg3 = pygame.image.load(
            "assets\graphics\label_button1\msg_image.png"
        ).convert_alpha()
        self.msg3_rect = self.msg3.get_rect(center=(390, 220))
        self.start_button = Button(
            (3 * screen_width) // 4,
            50 + screen_height // 4,
            self.play,
            0.5,
            self.screen,
        )
        self.about_button = Button(
            20 + (3 * screen_width) // 4,
            160 + (2 * screen_height) // 4,
            self.about,
            0.5,
            self.screen,
        )
        self.leaderboard_button = Button(
            100 + (3 * screen_width) // 4,
            screen_height // 4 - 120,
            self.leaderboard,
            0.3,
            self.screen,
        )
        self.setting_button = Button(50, 50, self.setting_img, 0.2, self.screen)

        # data of player
        with open("dataset.json") as f:
            self.data = json.load(f)
            self.name = self.data["name"]
            self.start_game = self.data["start_game"]
            self.max_level = self.data["max_level"]
            self.health = self.data["health"]
            self.coins = self.data["coins"]
            self.name = self.data["name"]
            self.music = self.data["music"]
            self.jump_key = self.data["jump_key"]
            self.right_key = self.data["right_key"]
            self.left_key = self.data["left_key"]
        self.game_pause = False
        self.load_scr = False
        self.end_menu = False

        # menu
        self.resume = pygame.image.load(
            "assets\graphics\label_button1\Resume1.png"
        ).convert_alpha()
        self.resume_button = Button(
            screen_width // 2 - 10,
            (screen_height // 4) + 122,
            self.resume,
            0.30,
            self.screen,
        )
        self.home = pygame.image.load(
            "assets\graphics\label_button1\home1.png"
        ).convert_alpha()
        self.home_button = Button(
            screen_width // 2,
            (screen_height // 4) + (2 * 122),
            self.home,
            0.30,
            self.screen,
        )
        self.replay = pygame.image.load(
            "assets\graphics\label_button1\Replay1.png"
        ).convert_alpha()
        self.replay_button = Button(
            screen_width // 2, (screen_height // 4), self.replay, 0.30, self.screen
        )
        self.bg = pygame.image.load(
            "assets\graphics\label_button1\menu_background.png"
        ).convert_alpha()
        self.bg = pygame.transform.scale(
            self.bg, (0.8 * self.bg.get_width(), 0.8 * self.bg.get_height())
        )
        self.bg_rect = self.bg.get_rect(
            center=(screen_width // 2, screen_height // 2 - 55)
        )

    def startGameScreen(self):
        self.screen.fill("grey")
        self.screen.blit(self.bg_img, self.bg_img_rect)
        # screen.blit(msg2, msg2_rect)
        self.screen.blit(self.icon_img, self.icon_img_rect)
        self.screen.blit(self.msg3, self.msg3_rect)
        if self.start_button.draw():
            # global start_game, load_scr
            self.start_game = True
            self.load_scr = True
        if self.setting_button.draw():
            # global left_key, right_key, jump_key
            self.ss = SettingScreen(self.left_key, self.jump_key, self.right_key)
            self.left_key, self.jump_key, self.right_key = self.ss.run()
        if self.about_button.draw():
            self.scr = About()
            self.scr.run()
            self.screen = pygame.display.set_mode((screen_width, screen_height))
        if self.leaderboard_button.draw():
            self.arr = scores()
            self.scr = Board()
            self.scr.run(self.arr)
            self.screen = pygame.display.set_mode((screen_width, screen_height))

    def main(self):
        # start screen
        while self.start_game != True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    update_controls(
                        self.name, self.jump_key, self.left_key, self.right_key
                    )
                    pygame.quit()
                    sys.exit()
            self.startGameScreen()
            pygame.display.update()
            self.clock.tick(60)
        self.game = Game(
            self.max_level,
            self.health,
            self.coins,
            self.screen,
            self.name,
            self.left_key,
            self.jump_key,
            self.right_key,
            self.game_pause,
            self.load_scr,
            self.end_menu,
            self.resume,
            self.home,
            self.replay,
            self.bg,
            self.bg_rect,
            self.clock,
        )
        self.curr_time = time.time()
        # load screen
        while self.load_scr:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pgs = time.time() - self.curr_time
            if pgs >= 2:
                self.load_scr = False
            self.screen.fill("black")
            self.load_msg = self.my_font.render("Loading........", False, "white")
            self.msg_rect = self.load_msg.get_rect(
                center=((screen_width) // 3, (screen_height) // 4)
            )
            self.screen.blit(self.load_msg, self.msg_rect)

            # progress bar
            self.bar_height = 60
            self.bar_width = 3 * (screen_width) // 4
            self.fill = (pgs / 2) * self.bar_width
            self.x = screen_width // 2 - self.bar_width // 2
            self.y = screen_height // 2 - self.bar_height
            self.fill_rect = pygame.Rect(self.x, self.y, self.fill, self.bar_height)
            self.outline_rect = pygame.Rect(
                self.x - 10, self.y - 10, self.bar_width + 20, self.bar_height + 20
            )
            pygame.draw.rect(self.screen, "white", self.fill_rect)
            pygame.draw.rect(self.screen, "white", self.outline_rect, 2)
            pygame.display.update()
            self.clock.tick(60)
        # time.sleep(1)
        # main game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # update_data("txt1.txt","start_game","0")
                    with open("dataset.json", "w") as f:
                        data = {
                            "start_game": 0,
                            "max_level": self.game.max_level,
                            "health": self.game.cur_health,
                            "coins": self.game.coins,
                        }
                        json.dump(data, f)
                        update(
                            self.name,
                            self.game.max_level,
                            self.game.cur_health,
                            self.game.coins,
                        )
                        update_controls(
                            self.name, self.jump_key, self.left_key, self.right_key
                        )
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_p
                        and (self.game_pause == False)
                        and self.game.status == "level"
                    ):
                        self.game_pause = True
            if self.game_pause:
                self.screen.blit(self.bg, self.bg_rect)
                if self.replay_button.draw():
                    self.game_pause = False
                    self.game.create_level(self.game.level.current_level)
                if self.resume_button.draw():
                    self.game_pause = False
                if self.home_button.draw():
                    self.game.status = "overworld"
                    self.game_pause = False
                    self.game.run()
            else:
                self.screen.fill("grey")
                self.game.run()
            pygame.display.update()
            self.clock.tick(60)
