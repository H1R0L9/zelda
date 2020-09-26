import pygame as pg
import time
from itertools import chain
from os import path
import pytweening as tween
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # avoid bug when adding walls on edges
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.state = 'idle'
        self.direction = 'down'
        self.t_ref = 0
        self.frame_index = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.state = 'walk'
            self.vel = vec(-PLAYER_SPEED, 0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.state = 'walk'
            self.vel = vec(PLAYER_SPEED, 0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.state = 'walk'
            self.vel = vec(0, -PLAYER_SPEED)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.state = 'walk'
            self.vel = vec(0, +PLAYER_SPEED)
        if keys[pg.K_SPACE]:
            self.state = "attack"

    def update(self):
        self.get_keys()
        #self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        #self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        t = pg.time.get_ticks()
        deltaTime = (t - self.t_ref)
        keys = pg.key.get_pressed()

        if(deltaTime > 80): # 250ms means 4 frames per second
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.frame_index += 1
                if self.frame_index >= len(self.game.player_walk_right):
                    self.frame_index = 0
                self.image = self.game.player_walk_right[self.frame_index]
                self.image = pg.transform.flip(self.image, True, False)
                self.direction = 'left'
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.frame_index += 1
                if self.frame_index >= len(self.game.player_walk_right):
                    self.frame_index = 0
                self.image = self.game.player_walk_right[self.frame_index]
                self.direction = 'right'
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.frame_index += 1
                if self.frame_index >= len(self.game.player_walk_up):
                    self.frame_index = 0
                self.image = self.game.player_walk_up[self.frame_index]
                self.direction = 'up'
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.frame_index += 1
                if self.frame_index >= len(self.game.player_walk_down):
                    self.frame_index = 0
                self.image = self.game.player_walk_down[self.frame_index]
                self.direction = 'down'

            # if self.state == 'idle':
            #     self.frame_index += 1
            #     if self.frame_index >= len(self.game.player_img_idle):
            #         self.frame_index = 0
            #     self.image = self.game.player_img_idle[self.frame_index]
            #     if self.direction == 'left':
            #         self.image = pg.transform.flip(self.image, True, False)
            if self.state == 'attack':
                if self.direction == 'left':
                    print('self.frame_index: ', self.frame_index)
                    if self.frame_index == len(self.game.player_attack_right)-1:
                        self.image = pg.transform.flip(self.game.player_idle_right, True, False)
                        self.state = 'idle'
                        self.frame_index = 0
                    else:
                        self.frame_index += 1
                        self.image = pg.transform.flip(self.game.player_attack_right[self.frame_index], True, False)
                elif self.direction == 'right':
                    print('self.frame_index: ', self.frame_index)
                    if self.frame_index == len(self.game.player_attack_right)-1:
                        self.image = self.game.player_idle_right
                        self.state = 'idle'
                        self.frame_index = 0
                    else:
                        self.frame_index += 1
                        self.image = self.game.player_attack_right[self.frame_index]
                elif self.direction == 'up':
                    print('self.frame_index: ', self.frame_index)
                    if self.frame_index == len(self.game.player_attack_up)-1:
                        self.image = self.game.player_idle_up
                        self.state = 'idle'
                        self.frame_index = 0
                    else:
                        self.frame_index += 1
                        self.image = self.game.player_attack_up[self.frame_index]
                elif self.direction == 'down':
                    print('self.frame_index: ', self.frame_index)
                    if self.frame_index == len(self.game.player_attack_down)-1:
                        self.image = self.game.player_idle_down
                        self.state = 'idle'
                        self.frame_index = 0
                    else:
                        self.frame_index += 1
                        self.image = self.game.player_attack_down[self.frame_index]
            # elif self.state != 'attack':
            #     if self.direction == 'left':
            #         # self.frame_index += 1
            #         # if self.frame_index >= len(self.game.player_idle_right):
            #         #     self.frame_index = 0
            #         self.image = pg.transform.flip(self.game.player_idle_right, True, False)
            #     elif self.direction == 'right':
            #         # self.frame_index += 1
            #         # if self.frame_index >= len(self.game.player_idle_right):
            #         #     self.frame_index = 0
            #         self.image = self.game.player_idle_right
            #         self.state = 'idle'
            #     elif self.direction == 'up':
            #         # self.frame_index += 1
            #         # if self.frame_index >= len(self.game.player_idle_up):
            #         #     self.frame_index = 0
            #         self.image = self.game.player_idle_up
            #         self.state = 'idle'
            #     elif self.direction == 'down':
            #         # self.frame_index += 1
            #         # if self.frame_index >= len(self.game.player_idle_down):
            #         #     self.frame_index = 0
            #         self.image = self.game.player_idle_down
            #         self.state = 'idle'
                    
            self.t_ref = pg.time.get_ticks()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Stair(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.stair
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.type = 'dungeon'

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        print('game.boss_idle: ', boss_idle)
        self.image = game.boss_idle[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # avoid bug when adding walls on edges
        self.hit_rect = BOSS_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.state = 'idle'
        self.direction = 'left'
        self.t_ref = 0
        self.frame_index = 0
    
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        t = pg.time.get_ticks()
        deltaTime = (t - self.t_ref)

        if(deltaTime > 80): # 250ms means 4 frames per second
            # if keys[pg.K_LEFT] or keys[pg.K_a]:
            #     self.frame_index += 1
            #     if self.frame_index >= len(self.game.player_walk_right):
            #         self.frame_index = 0
            #     self.image = self.game.player_walk_right[self.frame_index]
            #     self.image = pg.transform.flip(self.image, True, False)
            #     self.direction = 'left'
            # if keys[pg.K_RIGHT] or keys[pg.K_d]:
            #     self.frame_index += 1
            #     if self.frame_index >= len(self.game.player_walk_right):
            #         self.frame_index = 0
            #     self.image = self.game.player_walk_right[self.frame_index]
            #     self.direction = 'right'
            # if keys[pg.K_UP] or keys[pg.K_w]:
            #     self.frame_index += 1
            #     if self.frame_index >= len(self.game.player_walk_up):
            #         self.frame_index = 0
            #     self.image = self.game.player_walk_up[self.frame_index]
            #     self.direction = 'up'
            # if keys[pg.K_DOWN] or keys[pg.K_s]:
            #     self.frame_index += 1
            #     if self.frame_index >= len(self.game.player_walk_down):
            #         self.frame_index = 0
            #     self.image = self.game.player_walk_down[self.frame_index]
            #     self.direction = 'down'
            # for ai

            if self.state == 'idle':
                if self.direction == 'left':
                    print('self.frame_index: ', self.frame_index)
                    if self.frame_index == len(self.game.boss_idle)-1:
                        self.image = pg.transform.flip(self.game.boss_idle, True, False)
                        self.frame_index = 0
                    else:
                        self.frame_index += 1
                        self.image = pg.transform.flip(self.game.boss_idle[self.frame_index], True, False)
                elif self.direction == 'right':
                    print('self.frame_index: ', self.frame_index)
                    if self.frame_index == len(self.game.boss_idle)-1:
                        self.image = self.game.boss_idle
                        self.frame_index = 0
                    else:
                        self.frame_index += 1
                        self.image = self.game.boss_idle[self.frame_index]
                    
            self.t_ref = pg.time.get_ticks()