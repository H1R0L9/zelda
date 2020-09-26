import pygame as pg

WIDTH = 300
HEIGHT = 300
FPS = 60
TITLE = "zelda"
PLAYER_IMG = "sprites/idle_down.png"
PLAYER_STATE = "walk"
PLAYER_LAYER = 2
PLAYER_HIT_RECT = pg.Rect(0, 0, 16, 24)
PLAYER_SPEED = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

BOSS_HIT_RECT = pg.Rect(0, 0, 75, 65)

PLAYER_WALK_UP = ["sprites/walk_up1.png", "sprites/walk_up2.png"]
PLAYER_WALK_DOWN = ["sprites/walk_down1.png", "sprites/walk_down2.png"]
PLAYER_WALK_RIGHT = ["sprites/walk_right1.png", "sprites/walk_right2.png"]

PLAYER_ATTACK_UP = ["sprites/sword_up1.png", "sprites/sword_up2.png", "sprites/sword_up2.png", "sprites/sword_up3.png", ]
PLAYER_ATTACK_DOWN = ["sprites/sword_down1.png", "sprites/sword_down2.png", "sprites/sword_down3.png"]
PLAYER_ATTACK_RIGHT = ["sprites/sword_right1.png", "sprites/sword_right2.png", "sprites/sword_right3.png", "sprites/sword_right3.png"]

PLAYER_IDLE_UP = "sprites/idle_up.png"
PLAYER_IDLE_DOWN = "sprites/idle_down.png"
PLAYER_IDLE_RIGHT = "sprites/idle_right.png"

BOSS_IDLE = ["boss/boss_idle1.png", "boss/boss_idle2.png"]
BOSS_WALK = ["boss/boss_walk1.png", "boss/boss_walk2.png", "boss/boss_walk3.png", "boss/boss_walk4.png"]
BOSS_AXE_ATTACK = ["boss/boss_attack_axe1.png", "boss/boss_attack_axe2.png", "boss/boss_attack_axe3.png", "boss/boss_attack_axe4.png", "boss/boss_attack_axe5.png", "boss/boss_attack_axe6.png", "boss/boss_attack_axe7.png"]
BOSS_SPIN_ATTACK = ["boss/boss_spin_attack1.png", "boss/boss_spin_attack2.png", "boss/boss_spin_attack3.png", "boss/boss_spin_attack4.png", "boss/boss_spin_attack5.png", "boss/boss_spin_attack6.png", "boss/boss_spin_attack7.png", "boss/boss_spin_attack8.png"]
BOSS_DEATH = ["boss/boss_death1.png", "boss/boss_death2.png", "boss/boss_death3.png", "boss/boss_death4.png"]

BAT = ["enemies/bat/bat1.png", "enemies/bat/bat1.png", "enemies/bat/bat1.png"]
GHOST = ["enemies/ghost/ghost1.png", "enemies/ghost/ghost2.png", "enemies/ghost/ghost3.png"]
SKELETON = ["enemies/skeleton/skeleton1.png", "enemies/skeleton/skeleton2.png", "enemies/skeleton/skeleton3.png", "enemies/skeleton/skeleton4.png"]
FROG = ["enemies/frog/frog1.png", "enemies/frog/frog2.png", "enemies/frog/frog3.png"]