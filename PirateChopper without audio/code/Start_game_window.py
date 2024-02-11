import pygame as pg
import sys
from database_conn import login, register
from main import MainGame

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((400, 200))
pg.display.set_caption("Piratechopper")
base_font = pg.font.Font(None, 32)

name_text = ""
pass_text = ""

name_input_rect = pg.Rect(100, 57, 200, 36)
login_rect = pg.Rect(100, 119, 100, 36)

color_active = "white"
color = (60, 58, 58)

name_active = False
pass_active = False
enterstate = False


def draw_text(text, color, x, y):
    msg = base_font.render(text, False, color)
    msg_rect = msg.get_rect(topleft=(x, y))
    screen.blit(msg, msg_rect)


def draw_image(url, x, y):
    bg_img = pg.image.load(url).convert_alpha()
    bg_img_rect = bg_img.get_rect(center=(x, y))
    screen.blit(bg_img, bg_img_rect)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            if name_input_rect.collidepoint(event.pos):
                name_active = True
            else:
                name_active = False
            if login_rect.collidepoint(event.pos):
                if len(name_text) > 0:
                    if login(name_text, pass_text):
                        print("Logined successful")
                        # with open("main.py") as f:
                        #     pg.quit()
                        #     exec(f.read())
                        #     sys.exit()
                        pg.quit()
                        MainGame().main()
                        sys.exit()
                    else:
                        register(name_text, pass_text)
                        login(name_text, pass_text)
                        # with open("main.py") as f:
                        #     pg.quit()
                        #     exec(f.read())
                        #     sys.exit()
                        pg.quit()
                        MainGame().main()
                        sys.exit()
                else:
                    print("Enter name")
        if event.type == pg.KEYDOWN:
            if len(name_text) > 0:
                if event.unicode == "\r":
                    if login(name_text, pass_text):
                        print("Logined successful")
                        # with open("main.py") as f:
                        #     pg.quit()
                        #     exec(f.read())
                        #     sys.exit()
                        pg.quit()
                        MainGame().main()
                        sys.exit()
                    else:
                        register(name_text, pass_text)
                        login(name_text, pass_text)
                        # with open("main.py") as f:
                        #     pg.quit()
                        #     exec(f.read())
                        #     sys.exit()
                        pg.quit()
                        MainGame().main()
                        sys.exit()
            if name_active == True:
                if event.key == pg.K_BACKSPACE:
                    name_text = name_text[0:-1]
                else:
                    name_text += event.unicode
            if pass_active == True:
                if event.key == pg.K_BACKSPACE:
                    pass_text = pass_text[0:-1]
                else:
                    pass_text += event.unicode

    screen.fill("black")
    draw_image("assets\graphics\label_button1\Back_log2.jpg", 200, 150)
    draw_text("Enter name: ", "Black", 100, 25)
    pg.draw.rect(screen, "white", login_rect)
    draw_text("Enter ", "black", 100 + 18, 125)

    if name_active:
        pg.draw.rect(screen, color_active, name_input_rect, 2)
    else:
        pg.draw.rect(screen, color, name_input_rect, 2)

    name_text_surface = base_font.render(name_text, True, "black")

    screen.blit(name_text_surface, (name_input_rect.x + 5, name_input_rect.y + 5))

    pg.display.flip()
    clock.tick(60)
