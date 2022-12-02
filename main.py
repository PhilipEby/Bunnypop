import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))  # Player ship Original
YELLOW_SPACE_SHIP_LEFT = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow_left.png"))  # Player ship moving left
YELLOW_SPACE_SHIP_RIGHT = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow_right.png"))  # Player ship moving right

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
PLAYER_LASER_BLANK = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_blank.png"))
PLAYER_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
PLAYER_LASER_2 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow2.png"))
PLAYER_LASER_3 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow3.png"))
PLAYER_LASER_4_1 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_4_1.png"))
PLAYER_LASER_4_2 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_4_2.png"))
PLAYER_LASER_4_3 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_4_3.png"))
PLAYER_LASER_4_4 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_4_4.png"))
PLAYER_LASER_4_5 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_4_5.png"))
PLAYER_LASER_4_6 = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_4_6.png"))
PLAYER_LASER_RIGHT = pygame.image.load(os.path.join("assets", "pixel_laser_right.png"))
PLAYER_LASER_LEFT = pygame.image.load(os.path.join("assets", "pixel_laser_left.png"))

WEAPONS = pygame.image.load(os.path.join("assets", "pixel_extra_weapons.png"))
EXTRA_LIFE = pygame.image.load(os.path.join("assets", "pixel_extra_life.png"))
EXTRA_HEALTH = pygame.image.load(os.path.join("assets", "pixel_extra_health.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
BG_STAR_1 = pygame.image.load(os.path.join("assets", "background_star_1.png"))
BG_STAR_2 = pygame.image.load(os.path.join("assets", "background_star_2.png"))
BG_STAR_3 = pygame.image.load(os.path.join("assets", "background_star_3.png"))
BG_STAR_4 = pygame.image.load(os.path.join("assets", "background_star_4.png"))


class Star:
    STAR_MAP = {
        "one": BG_STAR_1,
        "two": BG_STAR_2,
        "three": BG_STAR_3,
        "four": BG_STAR_4
    }

    def __init__(self, x, y, star):
        self.x = x
        self.y = y
        self.img = self.STAR_MAP[star]

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class PowerUps:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.bonus_img = img
        self.mask = pygame.mask.from_surface(self.bonus_img)

    def draw(self, window):
        window.blit(self.bonus_img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def get_width(self):
        return self.bonus_img.get_width()

    def get_height(self):
        return self.bonus_img.get_height()


class Ship:
    COOLDOWN = 5  # Length in frames between shots. Edited to 15 from 30.
    COOLDOWN_2 = 5  # Length in frames between shots. Edited to 15 from 30.

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser_img_2 = None
        self.lasers = []
        self.lasers_2 = []
        self.cool_down_counter = 0
        self.cool_down_counter_2 = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        for laser in self.lasers_2:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def cooldown_2(self):
        if self.cool_down_counter_2 >= self.COOLDOWN_2:
            self.cool_down_counter_2 = 0
        elif self.cool_down_counter_2 > 0:
            self.cool_down_counter_2 += 1

    def shoot_2(self):
        if self.cool_down_counter_2 == 0:
            laser = Laser(self.x, self.y, self.laser_img_2)
            self.lasers_2.append(laser)
            self.cool_down_counter_2 = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = None
        self.laser_img_2 = None
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0

    def move_lasers(self, vel, objs, score):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            self.score = 10

    def move_lasers_2(self, vel, objs, score):
        self.cooldown_2()
        for laser in self.lasers_2:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers_2.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers_2:
                            self.lasers_2.remove(laser)
                            self.score = 10

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y + self.ship_img.get_height() + 10,
                                                   self.ship_img.get_width() * (self.health / self.max_health),
                                                   5))  # Changed color


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, last_x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.horz_vel = 0
        self.start = None
        self.last_x = last_x

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)  # This is where the enemy laser is chosen
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # (x, y)


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    score = 0
    main_font = pygame.font.SysFont("comicsans", int(HEIGHT / 30))  # made font size dynamic
    lost_font = pygame.font.SysFont("comicsans", 80)

    stars = []
    stars_start = 0
    star_count = 5
    star_vel = .25

    enemies = []
    wave_length = 0
    enemy_vel = 3  # Speed of enemies
    enemy_vel_horz = 2
    # enemy_start_move = True

    player_vel = 5
    laser_vel_enemy = 4  # Needs to be a changing variable based on level/dificulty
    laser_vel_player = -15  # Needs to be a changing variable based upgrades
    laser_vel_player_2 = -15  # Needs to be a changing variable based upgrades

    player_weapon_select = 1
    player_weapon_power = 0
    player = Player(300, 630)

    shot = 0
    powerup_vel = 3

    xhealth_list = []
    xhealth_control = 1
    xhealth_counter = 0

    xlife_list = []
    xlife_control = 1
    xlife_counter = 0

    weapons = []
    weapons_control = 1
    weapons_counter = 0

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (10, 50))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for star in stars:
            star.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        for xhealth in xhealth_list:
            xhealth.draw(WIN)

        for xlife in xlife_list:
            xlife.draw(WIN)

        for weapon in weapons:
            weapon.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You have Lost!!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2 - lost_label.get_height() / 2))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:  # Resets health bar and reduces live by 1
            player.health = 100
            lives -= 1
            player.x = 300
            player.y = 630

        if lives <= 0:  # changed to fix the 0 health ends game bug
            lost = True
            lost_count += 1

            if lost_count > FPS * 3:  # had to move the if statement below in one offset to make work.  Not sure why??
                run = False
            else:
                continue

        if stars_start < 10:
            stars_start += 1
            for i in range(star_count):
                star = Star(random.randrange(51, WIDTH - 51), random.randrange(-500, HEIGHT),
                            random.choice(['one', 'two', 'three', 'four']))
                stars.append(star)

        if len(enemies) == 0:
            level += 1
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(51, WIDTH - 51), 0, random.randrange(-2000, -100),
                              random.choice(['red', 'blue', 'green']), 100)
                enemy.horz_vel = random.choice([1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 8])
                enemy.start = True
                enemies.append(enemy)

            enemy_vel += enemy_vel * .015

            if xhealth_counter == 3:  # This is for controlling health bonuses
                xhealth_control = 1
                xhealth_counter = 1
            else:
                xhealth_control = 0
                xhealth_counter += 1

            for i in range(xhealth_control):
                xhealth = PowerUps(random.randrange(51, WIDTH - 51), random.randrange(10, 20),
                                   EXTRA_HEALTH)
                xhealth_list.append(xhealth)

            if xlife_counter == 4:  # This is for controlling health bonuses
                xlife_control = 1
                xlife_counter = 1
            else:
                xlife_control = 0
                xlife_counter += 1

            if lives == 10:
                pass
            else:
                for i in range(xlife_control):
                    xlife = PowerUps(random.randrange(51, WIDTH - 51), random.randrange(10, 20),
                                     EXTRA_LIFE)
                    xlife_list.append(xlife)

            if weapons_counter == 1:  # This is for controlling health bonuses
                weapons_control = 1
                weapons_counter = 1
            else:
                weapons_control = 0
                weapons_counter += 1

            for i in range(weapons_control):
                weapon = PowerUps(random.randrange(51, WIDTH - 51), random.randrange(10, 20),
                                  WEAPONS)
                weapons.append(weapon)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.K_ESCAPE:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0 or keys[
            pygame.K_LEFT] and player.x - player_vel > 0:  # left Added arrow keys
            player.x -= player_vel + 2  # changed ship speed
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH or keys[pygame.K_RIGHT] \
                and player.x + player_vel + player.get_width() < WIDTH:  # right Added arrow keys
            player.x += player_vel + 2  # changed ship speed
        if keys[pygame.K_w] and player.y - player_vel > 0 or keys[
            pygame.K_UP] and player.y - player_vel > 0:  # up Added arrow keys
            player.y -= player_vel + 2  # changed ship spped
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 12 < HEIGHT or keys[pygame.K_DOWN] \
                and player.y + player_vel + player.get_height() + 12 < HEIGHT:  # down Added arrow keys
            player.y += player_vel - .5  # changed ship speed

        if keys[pygame.K_1]:  # This allows you to select the desiered weapon. It only works if you change the
            # selections below
            if player_weapon_power >= 0:
                player_weapon_select = 1
        if keys[pygame.K_2]:
            if player_weapon_power >= 1:
                player_weapon_select = 2
        if keys[pygame.K_3]:
            if player_weapon_power >= 2:
                player_weapon_select = 3
        if keys[pygame.K_4]:
            if player_weapon_power >= 3:
                player_weapon_select = 4

        #if player_weapon_select == 1:  # Chnages laser when powerups are collected
        if player_weapon_power == 0:  # Chnages laser when powerups are collected
            player.laser_img = PLAYER_LASER
            player.laser_img_2 = PLAYER_LASER_BLANK
            Ship.COOLDOWN = 20
            Ship.COOLDOWN_2 = 8
            laser_vel_player = -25
            laser_vel_player_2 = -15
        #elif player_weapon_select == 2:
        elif player_weapon_power == 1:
            player.laser_img = PLAYER_LASER
            player.laser_img_2 = PLAYER_LASER_2
            Ship.COOLDOWN = 10
            Ship.COOLDOWN_2 = 8
            laser_vel_player = -25
            laser_vel_player_2 = -15
        #elif player_weapon_select == 3:
        elif player_weapon_power == 2:
            player.laser_img = PLAYER_LASER
            player.laser_img_2 = PLAYER_LASER_3
            Ship.COOLDOWN = 5
            Ship.COOLDOWN_2 = 5
            laser_vel_player = -25
            laser_vel_player_2 = -15
        #elif player_weapon_select == 4:
        elif player_weapon_power == 3:
            player.laser_img = PLAYER_LASER_2
            player.laser_img_2 = PLAYER_LASER_4_6
            Ship.COOLDOWN = 2
            Ship.COOLDOWN_2 = 2
            laser_vel_player = -25
            laser_vel_player_2 = -15
        else:
            player.laser_img = PLAYER_LASER
            player.laser_img_2 = PLAYER_LASER_BLANK
            Ship.COOLDOWN = 20
            Ship.COOLDOWN_2 = 8
            laser_vel_player = -25
            laser_vel_player_2 = -15

        if keys[pygame.K_SPACE]:
            player.shoot()
            player.shoot_2()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # This changes the image on the ship if you move left or right
            player.ship_img = YELLOW_SPACE_SHIP_LEFT
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.ship_img = YELLOW_SPACE_SHIP_RIGHT
        else:
            player.ship_img = YELLOW_SPACE_SHIP

        for star in stars[:]:
            star.move(star_vel)

            if star.y > HEIGHT:
                stars.remove(star)
                star = Star(random.randrange(51, WIDTH - 51), random.randrange(10, 100),
                            random.choice(['one', 'two', 'three', 'four']))
                stars.append(star)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.start == True:
                enemy.start = False
                enemy.last_x = enemy.x
                enemy.x += random.choice([-5, 5])

            if enemy.x + enemy.get_width() < WIDTH and (enemy.last_x < enemy.x or enemy.x < 0):
                enemy.last_x = enemy.x
                enemy.x += enemy.horz_vel
            elif enemy.last_x > enemy.x or enemy.x + enemy.get_width() >= WIDTH:
                enemy.last_x = enemy.x
                enemy.x -= enemy.horz_vel

            enemy_x = enemy.x

            enemy.move_lasers(laser_vel_enemy, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                score += 10
                enemies.remove(enemy)  # I don't like this want to change it
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(laser_vel_player, enemies, score)
        player.move_lasers_2(laser_vel_player, enemies, score)
        score += player.score
        player.score = 0

        for xhealth in xhealth_list[:]:
            xhealth.move(powerup_vel)

            if collide(xhealth, player):
                player.health = 100
                xhealth_list.remove(xhealth)


            elif xhealth.y + xhealth.get_height() > HEIGHT:
                xhealth_list.remove(xhealth)

        for xlife in xlife_list[:]:
            xlife.move(powerup_vel)

            if collide(xlife, player):
                if lives < 10:
                    lives += 1
                xlife_list.remove(xlife)

            elif xlife.y + xlife.get_height() > HEIGHT:
                xlife_list.remove(xlife)

        for weapon in weapons[:]:
            weapon.move(powerup_vel)

            if collide(weapon, player):
                player_weapon_power += 1
                weapons.remove(weapon)

            elif weapon.y + weapon.get_height() > HEIGHT:
                weapons.remove(weapon)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Click anywhere", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


main_menu()
