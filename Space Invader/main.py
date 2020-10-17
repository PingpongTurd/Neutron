#Todo: https://trello.com/b/SFzvhiz6/tristan-invaders

import pygame
import socket
import pickle
import os
import time
import random
pygame.font.init()
W,H = 750, 750
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Space Invaders")
# >> Loading Images <<
# >> lasers <<
Plaser = pygame.image.load(os.path.join('assets', 'laser.png'))
Elaser = pygame.image.load(os.path.join('assets', 'enemylaser.png'))

# >> Player << 
PlayerShip = pygame.image.load(os.path.join('assets', 'ship.png'))
SmallShip = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'ship.png')),(25,25))
# >> Enemys <<
Enemy1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy1_1.png')),(50,50))
Enemy1Shoot = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy1_2.png')),(50,50))
Enemy2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy2_1.png')),(50,50))
Enemy2Shoot = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy2_2.png')),(50,50))
Enemy3 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy3_1.png')),(50,50))
Enemy3Shoot = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy3_2.png')),(50,50))


# >> Explosions << 
explosionBlue = pygame.image.load(os.path.join('assets', 'explosionblue.png'))
explosionGreen = pygame.image.load(os.path.join('assets', 'explosiongreen.png'))
explosionPurple = pygame.image.load(os.path.join('assets', 'explosionpurple.png'))
# >> Background <<
Background = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background.jpg')),(W,H))
# >> Powerups <<
Bomb = pygame.transform.scale(pygame.image.load(os.path.join('assets','bomb.png')),(50,50))
MultiGun = pygame.transform.scale(pygame.image.load(os.path.join('assets','MultiGun.png')),(50,50))

# >> Astroid <<
astroid = pygame.transform.scale(pygame.image.load(os.path.join('assets','astroid.png')),(100,100)) 

# >> Server << 
class Server:
    host = 'edi.geinc.xyz'
    port = 80
    def serverfetch():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))
        client.send(pickle.dumps([0,"td"]))
        while True: 
            a= pickle.loads(client.recv(1024))
            return(a)
            break
    def serverdump(nm,sc): #nm is name, sc is score
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))
        client.send(pickle.dumps([nm,sc]))

#MULIPLAYER STUFFS
class multiplayer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        host = '192.168.1.100'
        port = 8888
        client.connect((host,port))
        username = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        uername = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        QUITLOOP = True 
                        break
                    else:
                        print(event.unicode)
                        username += event.unicode
            usert = font.render(f"{username}", 1, (255,255,255))
            WIN.blit(usert,(W/2,10))
            if QUITLOOP == true:
                break

                        
                        
    def sendData(self,data):
        client.send(pickle.dumps(data))
# >> Main Class << 
class main():
    # >> Runtime << 
    def rungame():
        global font, lives, level, player, enemies, lost, lfont, powerups, TWOGUN, TWOGUNTIME, TINYSHIPTIME, astroids, score
        astroids = []
        TINYSHIPTIME = 0
        TWOGUNTIME = 0
        TWOGUN = False
        score = 0
        enemies = []
        wave_length = 0
        enemy_vel = 1
        run = True
        clock = pygame.time.Clock()
        lives = 5
        level = 0
        vel = 5
        font = pygame.font.SysFont("space_invaders", 50)
        lfont = pygame.font.SysFont("space_invaders", 75)
        lost_count = 0
        player = Player(600, 650)
        laser_vel = 4
        lost = False
        powerups = []
        multiplayer()
        while run:
            clock.tick(60) 
            player.rect.size = (50,50)
            player.rect.center = (player.x,player.y)
            if lost:
                if lost_count >= 60 * 5:
                    run = False
                    break
                else:
                    continue 
            if len(enemies) == 0:
                level += 1
                for i in range(1,3):
                    WIN.blit(Background, (0,0))
                    label = lfont.render(f'Wave {level}', 1, (255,255,255))
                    WIN.blit(label, (int(W/2-(label.get_width()/2)),int(H/2)))
                    
                    pygame.display.update()
                    time.sleep(0.5)
                    WIN.blit(Background, (0,0))
                    pygame.display.update()
                    time.sleep(.5)
                    
                wave_length += 5
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50,W-50), random.randrange(-1500, -100), random.choice(['purple','blue','green']))
                    enemies.append(enemy)
                    enemy.laser_img = Elaser
                    
            if lives <= 0 or player.health <= 0:
                lost = True
                lost_count += 1
            main.draw()
            
            
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if player.x - vel - player.get_width() >= 0:
                    player.x -= vel

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if player.x + vel + player.get_width() <= W:
                    player.x += vel
  
                    
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if player.y - vel - player.get_height() >= 0:
                    player.y -= vel

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if player.y + vel + player.get_height() <= H:
                    player.y += vel

            if keys[pygame.K_SPACE]:
                player.shoot()

            if random.randrange(1,2000) == 1 and len(powerups) == 0:
                PU = powerup(random.randrange(50,W-50),random.randrange(-1500,-100), random.choice(['bomb','MultiGun','SmallShip']))
                powerups.append(PU)


            for enemy in enemies[:]:
                
                enemy.move(enemy_vel+(enemy_vel*(level/100)))
                enemy.move_lasers(laser_vel,player)
                enemy.rect.size = (50,50)
                enemy.rect.centerx = enemy.x
                enemy.rect.centery = enemy.y
                
                if enemy.y + enemy.get_height() > H:
                    lives -= 1
                    enemies.remove(enemy)
                if random.randrange(0,4*60) == 1:
                    enemy.shoot()
                if player.collision(enemy):
                    enemies.remove(enemy)
                    player.health -= 10
            player.move_lasers(-laser_vel, enemies)


                    
    # >> Refresh the window << 
    def draw():
        global lives, level, font, player, enemies, lost, powerups, TWOGUN, TWOGUNTIME, TINYSHIP, TINYSHIPTIME, astroids, score
        TINYSHIP = False
        WIN.blit(Background, (0,0))
        livesL = font.render(f"Lives {lives}", 1, (255,255,255))
        levelL = font.render(f"Wave {level}", 1, (255,255,255))
        WIN.blit(livesL, (10,10))
        WIN.blit(levelL, (W-levelL.get_width()-10,10))
        scoreF = font.render(f"Score {score}", 1, (255,255,255))
        WIN.blit(scoreF,(W/2,10))
        for i in enemies:
            i.draw()
        for i in powerups:
            i.move()
            i.draw()
            if not i.is_on_screen():
                powerups.remove(i)

            if i.collision(player):
                if i.name == 'bomb':
                    for en in enemies[:]:
                        score += 100
                        enemies.remove(en)
                elif i.name == 'MultiGun':
                    TWOGUN = True
                    TWOGUNTIME = 600
                elif i.name == 'SmallShip':
                    TINYSHIP = True
                    player.ship_img = SmallShip
                    player.rect = player.ship_img.get_rect()
                    TINYSHIPTIME = 600
                powerups.remove(i)
        if TWOGUN == True and TWOGUNTIME < 1: 
            TWOGUN = False
            player.ship_img = PlayerShip
            player.rect = player.ship_img.get_rect()
        elif TWOGUN == True:
            TWOGUNTIME -= 1
        if TINYSHIP == True and TINYSHIPTIME < 1:
            TINYSHIP = False
        else:
            TINYSHIPTIME -= 1
        if random.randrange(0,20000) == 1:
            asd = Asteroid(random.randrange(150,W-100),random.randrange(-1500,-100))
            astroids.append(asd)
        for i in astroids:
            i.move()
            if player.collision(i):
                player.health = 0
        Player.draw(player)

        if lost == True:
            label = lfont.render("You lost!!", 1, (255,255,255))
            WIN.blit(label, (int(W/2-(label.get_width()/2)),int(H/2)))
        
        pygame.display.update()

# >> collide <<
def collide(obj1, obj2):
    return obj1.rect.colliderect(obj2.rect) == 1
# Laser
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
    def draw(self):
        WIN.blit(self.img, (self.x+24, self.y))

    def move(self, vel):
        self.y += vel
        self.rect.center = (self.x,self.y)

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj,self)
    
# >> POWER UPS <<
class powerup:
    def __init__(self, x, y, name):
        powerupTable = {
            'bomb':Bomb,
            'MultiGun':MultiGun,
            'SmallShip':SmallShip,
        }
        self.x = x
        self.y = y
        self.img = powerupTable[name]
        self.name = name
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        
    def move(self):
        self.y += 5
        self.rect.center = (self.x,self.y)

    def draw(self):
        WIN.blit(self.img,(self.x,self.y))
        
    def is_on_screen(self):
        return (self.y < H)

    def collision(self,obj):
        return collide(self,obj)
# astroid 

class Asteroid():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = astroid
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()

    def move(self):
        self.y += 15 
        WIN.blit(self.img,(self.x,self.y))
    def is_on_screen(self):
        return not(self.y>H)


#Ship
class Ship():
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.lasers = []
        self.cooldown = 0
        
    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = 1
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)

    def move_lasers(self, vel, obj):
        self.cooldownF()
        for i in self.lasers:
            i.move(vel)
            if i.off_screen(H):
                self.lasers.remove(i)
            elif i.collision(obj):
                obj.health -= 10
                self.lasers.remove(i)
                
    def cooldownF(self):
        if self.cooldown >= self.COOLDOWN:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1

    def draw(self):
        WIN.blit(self.ship_img, (self.x, self.y))
        for i in self.lasers:
            i.draw() 
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

# Player
class Player(Ship):
    def __init__(self, x, y, health=100):
        self.ship_img = PlayerShip
        self.laser_img = Plaser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.rect = self.ship_img.get_rect()
        self.max_health = health
        self.small_img = SmallShip
        self.small_mask = pygame.mask.from_surface(self.small_img)
        self.small_rect = self.small_img.get_rect()
        super().__init__(x, y, health)
    
    def move_lasers(self, vel, objs):
        global score
        self.cooldownF()
        for i in self.lasers:
            i.move(vel)
            if i.off_screen(H):
                self.lasers.remove(i)
                break
            else:
                for r in objs:
                    if i.collision(r):
                        score += 100
                        objs.remove(r)
                        self.lasers.remove(i)
                        break
        self.rect.size = (50,50)
        self.rect.center = (self.x+25,self.y)

    def shoot(self):
        global TWOGUN, TINYSHIP
        if self.cooldown == 0:
            self.cooldown = 1
            if not TINYSHIP:
                if TWOGUN == True: 
                    laser = Laser(self.x-(self.ship_img.get_width()/2), self.y, self.laser_img)
                    self.lasers.append(laser)
                    laser = Laser(self.x+(self.ship_img.get_width()/2), self.y, self.laser_img)
                    self.lasers.append(laser)
                else:
                    laser = Laser(self.x, self.y, self.laser_img)
                    self.lasers.append(laser)
            else:
                if TWOGUN == True: 
                    laser = Laser((self.x-(self.ship_img.get_width()/2))/2, self.y, self.laser_img)
                    self.lasers.append(laser)
                    laser = Laser((self.x+(self.ship_img.get_width()/2))/2, self.y, self.laser_img)
                    self.lasers.append(laser)
                else:
                    laser = Laser(self.x-(self.ship_img.get_width()), self.y, self.laser_img)
                    self.lasers.append(laser)
    def draw(self):
        super().draw()
        self.healthbar()
    def healthbar(self):
        pygame.draw.rect(WIN, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(WIN, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
        
    def collision(self,obj):
        return collide(self,obj)
# Enemy
class Enemy(Ship): 
    COLOUR_MAP = {
        'purple': (Enemy1, Enemy1Shoot),
        'green' : (Enemy3, Enemy3Shoot),
        'blue' : (Enemy2, Enemy2Shoot)
    }
    def __init__(self, x, y, colour, health=100):
        self.ship_img, self.shooting_img = self.COLOUR_MAP[colour]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.rect = self.ship_img.get_rect()
        super().__init__(x, y, health)
    def move(self,vel):
        self.y += vel
print("""
© Neutron 2020. All rights reserved.
No part of this publication may be reproduced, distributed, or transmitted in any form or by any means,
including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher,
except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.
For permission requests, write to the publisher, addressed “Attention: Permissions Coordinator innit,” at the addresses below.
sdu23h7dy98y87asd7a@gmail.com 
ElectronDev@protonmail.com
with any questions you may directly ask me or this other random guy on discord:
Just a Thing#4419,
ElectronDev#0001
""")
def main_menu():
    title_font = pygame.font.SysFont("space_invaders", 70)
    run = True
    while run:
        WIN.blit(Background, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (W/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main.rungame()
    pygame.quit()
main_menu()
