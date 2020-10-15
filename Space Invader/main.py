import pygame
import os
import time
import random
pygame.font.init()
W,H = 750, 750
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Space Invaders")
# >> Loading Images innit <<
# >> lasers innit <<
Plaser = pygame.image.load(os.path.join('assets', 'laser.png'))
Elaser = pygame.image.load(os.path.join('assets', 'enemylaser.png'))

# >> Player innit << 
PlayerShip = pygame.image.load(os.path.join('assets', 'ship.png'))
# >> Enemys innit <<
Enemy1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy1_1.png')),(50,50))
Enemy1Shoot = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy1_2.png')),(50,50))
Enemy2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy2_1.png')),(50,50))
Enemy2Shoot = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy2_2.png')),(50,50))
Enemy3 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy3_1.png')),(50,50))
Enemy3Shoot = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemy3_2.png')),(50,50))
# >> Explosions innit << 
explosionBlue = pygame.image.load(os.path.join('assets', 'explosionblue.png'))
explosionGreen = pygame.image.load(os.path.join('assets', 'explosiongreen.png'))
explosionPurple = pygame.image.load(os.path.join('assets', 'explosionpurple.png'))
# >> Background innit <<
Background = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background.jpg')),(W,H))
# >> Powerups innit innit <<
Bomb = pygame.transform.scale(pygame.image.load(os.path.join('assets','bomb.png')),(25,25))

# >> Main Class innit << 
class main():
    # >> Runtime innit << 
    def rungame():
        global font, lives, level, player, enemies, lost, lfont
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
        while run:
            clock.tick(60)
            player.rect.size = (50,50)
            player.rect.center = (player.x,player.y)
            if lost:
                if lost_count >= 60 * 5:
                    run = False
                    pygame.quit()
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

            if random.randrange(1,2) == 1 and len(powerups) == 0:
                PU = powerup(random.randrange(50,W-50), random.randrange(-1500, -100), random.choice(['bomb']))
                powerups.append(PU)
            for i in powerups:
                i.move()
            for enemy in enemies[:]:
                
                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel,player)
                enemy.rect.size = (50,50)
                enemy.rect.centerx = enemy.x
                enemy.rect.centery = enemy.y
                
                if enemy.y + enemy.get_height() > H:
                    lives -= 1
                    enemies.remove(enemy)
                if random.randrange(0,4*60) == 1:
                    enemy.shoot()
            player.move_lasers(-laser_vel, enemies)
            
                    
    # >> Refresh the window innit << 
    def draw():
        global lives, level, font, player, enemies, lost
        WIN.blit(Background, (0,0))
        livesL = font.render(f"Lives {lives}", 1, (255,255,255))
        levelL = font.render(f"Wave {level}", 1, (255,255,255))
        WIN.blit(livesL, (10,10))
        WIN.blit(levelL, (W-levelL.get_width()-10,10))
        for i in enemies:
            i.draw()
        Player.draw(player)

        if lost == True:
            label = lfont.render("You lost!!", 1, (255,255,255))
            WIN.blit(label, (int(W/2-(label.get_width()/2)),int(H/2)))
        
        pygame.display.update()


# >> collide innit <<
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
    
# >> POWER UPS innit <<
class powerup:

    
    
    def __init__(self, x, y, name):
        powerupTable = {
            'bomb':Bomb,
        }
        self.x = x
        self.y = y
        self.img = powerupTable[name]
        self.name = name
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        
    def move(self):
        self.y += 10
        self.rect.center = (self.x,self.y)
    def draw(self):
        WIN.blit(self.img,(self.x,self.y))
        
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
        super().__init__(x, y, health)
    
    def move_lasers(self, vel, objs):
        self.cooldownF()
        for i in self.lasers:
            i.move(vel)
            if i.off_screen(H):
                self.lasers.remove(i)
                break
            else:
                for r in objs:
                    if i.collision(r):
                        objs.remove(r)
                        self.lasers.remove(i)
                        break
        self.rect.size = (50,50)
        self.rect.center = (self.x+25,self.y)
    def draw(self):
        super().draw()
        self.healthbar()
    def healthbar(self):
        pygame.draw.rect(WIN, (255,0,0), (self.x, self.y + PlayerShip.get_height() + 10, PlayerShip.get_width(), 10))
        pygame.draw.rect(WIN, (0,255,0), (self.x, self.y + PlayerShip.get_height() + 10, PlayerShip.get_width() * (self.health/self.max_health), 10))
        
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
© 2020 Leighton Bridger 
All rights reserved. No part of this publication may be reproduced, distributed,
or transmitted in any form or by any means, including photocopying, recording,
or other electronic or mechanical methods, without the prior written permission
of the publisher, except in the case of brief quotations embodied in critical
reviews and certain other noncommercial uses permitted by copyright law.
For permission requests, write to the publisher, addressed
“Attention: Permissions Coordinator,” at the address below.
3173540@students.ripleyacademy.org
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

