import pygame as pg
import random
from projectile import Projectile
from collid import collide
from ship import Ship
from pygame import mixer

mixer.init()
pg.font.init()
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)
s = mixer.Sound('sounds/projectile.wav')
s1 = mixer.Sound('sounds/explosion.wav')
width = 600
height = 500
WHITE = 255,255,255
surface = pg.display.set_mode((width, height))
pg.display.set_caption("Космические войны")
pg.display.set_icon(pg.image.load("pictures/logo1.jpg"))

RED_SPACE_SHIP = pg.transform.scale(pg.image.load("pictures/redship.png"), (60, 28))
RED_SPACE_SHIP.set_colorkey((WHITE))
GREEN_SPACE_SHIP = pg.transform.scale(pg.image.load("pictures/th.jpg"), (64, 44))
GREEN_SPACE_SHIP.set_colorkey((WHITE))
BLUE_SPACE_SHIP = pg.transform.scale(pg.image.load("pictures/blueship.png"), (61, 33))
INO = pg.transform.scale(pg.image.load("pictures/ino.png"),(50,40))
sp = pg.image.load("pictures/logo1.jpg")
sp.set_colorkey((WHITE))

SPACE_SHIP = pg.transform.scale(sp, (50, 50))

RED_PROJECTILE = pg.transform.scale(pg.image.load("pictures/projectile_red.png"), (65, 75))
GREEN_PROJECTILE = pg.transform.scale(pg.image.load("pictures/projectile_green.png"), (65, 75))
BLUE_PROJECTILE = pg.transform.scale(pg.image.load("pictures/projectile_blue.png"), (65, 75))
YELLOW_PROJECTILE = pg.transform.scale(pg.image.load("pictures/projectile_yellow.png"), (65, 75))

background = pg.transform.scale(pg.image.load("pictures/backgroundsurface.png"), (width, height))
score = 0

class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SPACE_SHIP
        self.projectile_img = BLUE_PROJECTILE
        self.mask = pg.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_projectiles(self, vel, objs):
        global score
        self.cooldown()
        for projectile in self.projectiles:
            projectile.move(vel)
            if projectile.off_screen(height):
                self.projectiles.remove(projectile)
            else:
                for obj in objs:
                    if projectile.collision(obj):
                        objs.remove(obj)
                        score += 1
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)

    def draw(self, surfacedow):
        super().draw(surfacedow)
        self.healthbar(surfacedow)

    def healthbar(self, surfacedow):
        pg.draw.rect(surfacedow, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pg.draw.rect(surfacedow, (0, 255, 0), (
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_PROJECTILE),
        "green": (GREEN_SPACE_SHIP, GREEN_PROJECTILE),
        "blue": (BLUE_SPACE_SHIP, YELLOW_PROJECTILE),
        "ino": (INO,GREEN_PROJECTILE)

    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.projectile_img = self.COLOR_MAP[color]
        self.mask = pg.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            projectile = Projectile(self.x - 12, self.y, self.projectile_img)
            self.projectiles.append(projectile)
            self.cool_down_counter = 1

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    projectile_vel = 6
    global score
    score = 0

    player = Player(275, 375)

    main_font = pg.font.SysFont("arial", 25)
    lost_font = pg.font.SysFont("arial", 40)
    smallText = pg.font.SysFont("arial", 20)

    clock = pg.time.Clock()

    lost = False
    lost_count = 0

    def redraw_surfacedow():
        surface.blit(background, (0, 0))
        lives_label = main_font.render(f"Прошло врагов {5 - lives }", 1, (255, 255, 255))
        player.draw(surface)

        surface.blit(lives_label, (10, 10))
        level_label = main_font.render(f"СЛОЖНОСТЬ: {level}", 1, (255, 255, 255))
        total = main_font.render(f"ОЧКИ: {score}", 1, (255, 255, 255))
        surface.blit(level_label, (width - level_label.get_width() - 15, 10))
        surface.blit(total, (width - level_label.get_width() - 15, 35))

        for enemy in enemies:
            enemy.draw(surface)

        if lost:
            lost_label = lost_font.render("ВЫ ПРОИГРАЛИ!", 1, (255, 255, 255))
            total = smallText.render(f"ОЧКИ:{score}", 1, (255, 255, 255))
            surface.blit(lost_label, (width / 2 - lost_label.get_width() / 2, 250))
            surface.blit(total, (width / 2 - total.get_width() / 2, 380))

        pg.display.update()

    while run:
        clock.tick(FPS)
        redraw_surfacedow()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        keys = pg.key.get_pressed()
        if (keys[pg.K_a] ^ keys[pg.K_LEFT])  and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if (keys[pg.K_d] ^ keys[pg.K_RIGHT]) and player.x + player_vel + player.get_width() < width:  # right
            player.x += player_vel
        if (keys[pg.K_w] ^ keys[pg.K_UP]) and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if (keys[pg.K_s] ^ keys[pg.K_DOWN]) and player.y + player_vel + player.get_height() + 15 < height:  # down
            player.y += player_vel
        if keys[pg.K_SPACE]:
            player.shoot()
            s.play()

        if keys[pg.K_ESCAPE]:
            paused()
        if keys[pg.K_p]:
            paused()

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_projectiles(projectile_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                s1.play()
                lives -= 1
                enemies.remove(enemy)

        player.move_projectiles(-projectile_vel, enemies)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width - 80), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green","ino"]))
                enemies.append(enemy)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()


def main_menu():
    title_font = pg.font.SysFont("arial", 25)

    run = True
    while run:
        surface.blit(background, (0, 0))
        title_label = title_font.render("Нажмите мышью для начала", 1, (255, 255, 255))
        surface.blit(title_label, (width / 2 - title_label.get_width() / 2, 250))
        back_key = title_font.render("backspace --> главное меню", 1, (255, 255, 255))
        surface.blit(back_key, (width - back_key.get_width() - 10, 10))

        player = Player(275, 375)
        player.draw(surface)

        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                run = False
            if keys[pg.K_BACKSPACE]:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                main()


def option():
    title_font = pg.font.SysFont("arial", 25)
    back_key = title_font.render("backspace --> главное меню", 1, (255, 255, 255))
    run = True
    while run:
        AR = pg.transform.scale(pg.image.load("pictures/controls.png"), (600, 500))
        surface.blit(AR, (0, 0))
        surface.blit(back_key, (width - back_key.get_width() - 10, 10))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            keys = pg.key.get_pressed()
            if keys[pg.K_BACKSPACE]:
                run = False
            if keys[pg.K_ESCAPE]:
                run = False

def rule():
    title_f = pg.font.SysFont("arial", 25)
    back_key = title_f.render("backspace --> главное меню", 1, (255, 255, 255))
    run = True
    while run:
        ARR = pg.transform.scale(pg.image.load("pictures/rules1.png"), (600, 500))
        surface.blit(ARR, (0, 0))
        surface.blit(back_key, (width - back_key.get_width() - 10, 10))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            keys = pg.key.get_pressed()
            if keys[pg.K_BACKSPACE]:
                run = False
            if keys[pg.K_ESCAPE]:
                run = False

def paused():
    largeText = pg.font.SysFont("arial", 75)
    smallText = pg.font.SysFont("arial", 20)
    text = largeText.render("ПАУЗА", 1, (255, 255, 255))
    text2 = smallText.render("НАЖМИ 'c' ДЛЯ ПРОДОЛЖЕНИЯ", 1, (255, 255, 255))
    back_key = smallText.render("backspace --> main menu", 1, (255, 255, 255))
    surface.blit(back_key, (width - back_key.get_width() - 10, 55))
    surface.blit(text, (width / 2 - text.get_width() / 2, 190))
    surface.blit(text2, (width / 2 - text2.get_width() / 2, 290))
    pg.display.update()
    pause = True

    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        keys = pg.key.get_pressed()
        if keys[pg.K_c]:
            pause = False

        if keys[pg.K_BACKSPACE]:
            intro()


def button(msg, x, y, w, h, ic, ac, action=None):  # button display & action func
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()


    smallText = pg.font.SysFont("arial", 20)
    text = smallText.render(msg, 1, (255, 255, 255))

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(surface, ac, (x, y, w, h))

        if click[0] == 1 and action == "start":

            main_menu()
            surface.blit(background, (0, 0))
        if click[0] == 1 and action == "options":
            option()
            intro()
        if click[0] == 1 and action == "rules":
            rule()
            intro()


    else:
        pg.draw.rect(surface, ic, (x, y, w, h))

    surface.blit(text, (width / 2 - text.get_width() / 2, ((y + (h / 2)) - 17)))
    pg.display.update()


def intro():

    surface.blit(background, (0, 0))

    main_font = pg.font.SysFont("arial", 24)
    text = main_font.render("created by MIROSHKIN_ALEXANDR_BBSO-02-21 ", 1, (255, 255, 255))
    surface.blit(text, (90, 10))

    pg.display.update()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_w) ^ (event.key == pg.K_UP):
                    main_menu()
                    run = False
                if (event.key == pg.K_a) ^ (event.key == pg.K_LEFT):
                    run = False

        button("Играть", 215, 150, 170, 50, (0, 0, 0), (90, 90, 90), "start")
        button("Правила игры", 200, 250, 200, 50, (0, 0, 0), (90, 90, 90), "rules")
        button("Управление", 240, 350, 120, 50, (0, 0, 0), (90, 90, 90), "options")


    pg.quit()


intro()
