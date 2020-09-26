import pygame as pg
from os import path
from settings import *
from sprites import *
from tilemap import *
import sys

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert()
        self.player_idle_up = pg.image.load(path.join(img_folder, PLAYER_IDLE_UP)).convert()
        self.player_idle_down = pg.image.load(path.join(img_folder, PLAYER_IDLE_DOWN)).convert()
        self.player_idle_right = pg.image.load(path.join(img_folder, PLAYER_IDLE_RIGHT)).convert()
        self.player_img.set_colorkey((0,64,64))
        self.player_idle_up.set_colorkey((0,64,64))
        self.player_idle_down.set_colorkey((0,64,64))
        self.player_idle_right.set_colorkey((0,64,64))
        self.player_walk_up = []
        self.player_walk_down = []
        self.player_walk_right = []
        self.player_attack_up = []
        self.player_attack_right = []
        self.player_attack_down = []

        self.boss_idle = []
        self.boss_walk = []
        self.boss_axe_attack = []
        self.boss_spin_attack = []
        self.boss_death = []
        self.bat = []
        self.ghost = []
        self.frog = []
        self.skeleton = []

        for i in range(len(PLAYER_WALK_UP)):
            player_walk_up = pg.image.load(path.join(img_folder, PLAYER_WALK_UP[i])).convert()
            player_walk_up.set_colorkey((0,64,64))
            self.player_walk_up.append(player_walk_up)
        for i in range(len(PLAYER_WALK_DOWN)):
            player_walk_down = pg.image.load(path.join(img_folder, PLAYER_WALK_DOWN[i])).convert()
            player_walk_down.set_colorkey((0,64,64))
            self.player_walk_down.append(player_walk_down)
        for i in range(len(PLAYER_WALK_RIGHT)):
            player_walk_right = pg.image.load(path.join(img_folder, PLAYER_WALK_RIGHT[i])).convert()
            player_walk_right.set_colorkey((0,64,64))
            self.player_walk_right.append(player_walk_right)
        for i in range(len(PLAYER_ATTACK_UP)):
            player_attack_up = pg.image.load(path.join(img_folder, PLAYER_ATTACK_UP[i])).convert()
            player_attack_up.set_colorkey((0,64,64))
            self.player_attack_up.append(player_attack_up)
        for i in range(len(PLAYER_ATTACK_DOWN)):
            player_attack_down = pg.image.load(path.join(img_folder, PLAYER_ATTACK_DOWN[i])).convert()
            player_attack_down.set_colorkey((0,64,64))
            self.player_attack_down.append(player_attack_down)
        for i in range(len(PLAYER_ATTACK_RIGHT)):
            player_attack_right = pg.image.load(path.join(img_folder, PLAYER_ATTACK_RIGHT[i])).convert()
            player_attack_right.set_colorkey((0,64,64))
            self.player_attack_right.append(player_attack_right)
        self.enemyloading('BOSS_IDLE')
        self.enemyloading('BOSS_WALK')
        self.enemyloading('BOSS_AXE_ATTACK')
        self.enemyloading('BOSS_SPIN_ATTACK')
        self.enemyloading('BOSS_DEATH')
        self.enemyloading('BAT')
        self.enemyloading('GHOST')
        self.enemyloading('FROG')
        self.enemyloading('SKELETON')
        self.maploading("untitled.tmx")

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.stair, False)
        for hit in hits:
            if hit.type == 'dungeon':
                self.maploading('dungeon1.tmx')

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        pg.display.flip()

    # def draw_text(self, text, font_name, size, color, x, y, align="nw"):
    #     font = pg.font.Font(font_name, size)
    #     text_surface = font.render(text, True, color)
    #     text_rect = text_surface.get_rect()
    #     if align == "nw":
    #         text_rect.topleft = (x, y)
    #     if align == "ne":
    #         text_rect.topright = (x, y)
    #     if align == "sw":
    #         text_rect.bottomleft = (x, y)
    #     if align == "se":
    #         text_rect.bottomright = (x, y)
    #     if align == "n":
    #         text_rect.midtop = (x, y)
    #     if align == "s":
    #         text_rect.midbottom = (x, y)
    #     if align == "e":
    #         text_rect.midright = (x, y)
    #     if align == "w":
    #         text_rect.midleft = (x, y)
    #     if align == "center":
    #         text_rect.center = (x, y)
    #     self.screen.blit(text_surface, text_rect)


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        # self.screen.fill(BLACK)
        # self.draw_text("ZOMBIE SHOOTERS", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        # self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        # pg.display.flip()
        # self.wait_for_key()
        pass

    def show_go_screen(self):
        # self.screen.fill(BLACK)
        # self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        # self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        # pg.display.flip()
        # self.wait_for_key()
        pass

    def maploading(self, mapname):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(self.map_folder, mapname))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stair = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'dungeon':
                Stair(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'boss':
                Boss(self, tile_object.x, tile_object.y)

    def enemyloading(self, type):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')

        if type == 'BOSS_IDLE':
            for i in range(len(BOSS_IDLE)):
                enemies = pg.image.load(path.join(img_folder, BOSS_IDLE[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.boss_idle.append(enemies)
            print('enemyloading - BOSS_IDLE: ', self.boss_idle)
        elif type == 'BOSS_WALK':
            for i in range(len(BOSS_WALK)):
                enemies = pg.image.load(path.join(img_folder, BOSS_WALK[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.boss_walk.append(enemies)
        elif type == 'BOSS_AXE_ATTACK':
            for i in range(len(BOSS_AXE_ATTACK)):
                enemies = pg.image.load(path.join(img_folder, BOSS_AXE_ATTACK[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.boss_axe_attack.append(enemies)
        elif type == 'BOSS_SPIN_ATTACK':
            for i in range(len(BOSS_SPIN_ATTACK)):
                enemies = pg.image.load(path.join(img_folder, BOSS_SPIN_ATTACK[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.boss_spin_attack.append(enemies)
        elif type == 'BOSS_DEATH':
            for i in range(len(BOSS_DEATH)):
                enemies = pg.image.load(path.join(img_folder, BOSS_DEATH[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.boss_death.append(enemies)
        elif type == 'BAT':
            for i in range(len(BAT)):
                enemies = pg.image.load(path.join(img_folder, BAT[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.bat.append(enemies)
        elif type == 'GHOST':
            for i in range(len(GHOST)):
                enemies = pg.image.load(path.join(img_folder, GHOST[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.ghost.append(enemies)
        elif type == 'FROG':
            for i in range(len(FROG)):
                enemies = pg.image.load(path.join(img_folder, FROG[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.frog.append(enemies)
        elif type == 'SKELETON':
            for i in range(len(SKELETON)):
                enemies = pg.image.load(path.join(img_folder, SKELETON[i])).convert()
                enemies.set_colorkey((0,0,0))
                self.skeleton.append(enemies)

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
