import pygame
import random
import math

# initializing the pygame for starting the game        
pygame.init()
# screen resolution..
screen = pygame.display.set_mode((800,600))

background = pygame.image.load("space.jpg")
# Title and Icon..

pygame.display.set_caption("War Of Universe")
# icon of the game window..

icon =  pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# player image..

running = True

class Player:
    def __init__(self) -> None:
        self.playerImage = pygame.image.load("UFO.png")
        self.playerx = 379
        self.playery = 520
# initially change in position will be zero...
        self.playerx_change = 0
        self.playery_change = 0
        
    def player(self,x,y):
        screen.blit(self.playerImage, (x, y))



class Enemy:
    def __init__(self) -> None:
        self.enemyImage = [] 
        self.enemyx =[] 
        self.enemyy = [] 
        self.number_of_enemy = 10 
        self.enemyx_change = [] 
        self.enemyy_change = [] 
        self.create_enemy(self.number_of_enemy)
    
    # creating multiple number of enemies in the game window...
    def create_enemy(self,number_of_enemy):
        for i in range(number_of_enemy):
            self.enemyImage.append(pygame.image.load("enemy.png"))
            self.enemyx.append(random.randint(0,600))
            self.enemyy.append(random.randint(10,100))
            self.enemyx_change.append(3)
            self.enemyy_change.append(15)
            
            
    def enemy(self,enemyimage,x,y):
        screen.blit(enemyimage, (x,y))

class Bullet:
    # ready state you cant see the bullet in the screen..
    # fire state in which you are able to see the bullet on the screen..
    def __init__(self):
        self.bulletImage = pygame.image.load("bullet.png")
        self.bulletx = 0
        self.bullety = player.playery
        self.bulletx = 0
        self.bullety_change = 0.7
        self.state = "ready"
        
    def fire_bullet(self,x,y):
        self.state = "fire"
        screen.blit(self.bulletImage, (x+16,y+10))

class Game:
    def __init__(self):
        self.gameImage = pygame.image.load("game-over.png")
        
    def Game_Over(self):
        bullet.state = "ready"
        screen.blit(self.gameImage, (300,200))
        
        
        
           
player = Player()
enemy = Enemy()
bullet = Bullet()
game = Game()

def is_collision(enemyx,enemyy,bulletx,bullety):
    
    distance = math.sqrt(((enemyx-bulletx)**2)+((enemyy-bullety)**2))
    if distance < 27:
        return True
    else:
        return False

    # game looping for running game infinetly
while (running):
    # above evrything just like Z-index..
    screen.fill((0,0,0))
    # background image fill
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
        # if key stroke is pressed weather it is left or right..
        if event.type == pygame.KEYDOWN: #key pressing
            if event.key == pygame.K_LEFT: #left key press check..
                player.playerx_change = -0.5
            elif event.key == pygame.K_RIGHT:
                player.playerx_change = 0.5
            elif event.key == pygame.K_UP:
                player.playery_change = -0.5
            elif event.key ==  pygame.K_DOWN:
                player.playery_change = 0.5
            elif event.key == pygame.K_SPACE:
                if bullet.state=="ready":
                    bullet.bulletx = player.playerx
                    bullet.fire_bullet(bullet.bulletx, player.playery)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT : #left key press check..
                player.playerx_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                player.playery_change = 0
                
    
    # which you want to continue untill game closed...
    # changing position of UFO in x-axis.
    player.playerx += player.playerx_change
    # changing position of UFO in y-axis.
    player.playery += player.playery_change
    
    # setting boundaries of the game window...
    
    # left side...
    if player.playerx <=0 :
        player.playerx = 0
    # right side...
    if player.playerx >= 740:
        player.playerx = 740
    # upward side...
    if player.playery <= 30:
        player.playery = 30
    # downward side...
    if player.playery >= 530:
        player.playery = 530
        
    for i in range(enemy.number_of_enemy):
        enemy.enemyx[i] += enemy.enemyx_change[i]
        if enemy.enemyx[i] <= 0:
            enemy.enemyx_change[i] = 3
            enemy.enemyy[i] += enemy.enemyy_change[i]
        elif enemy.enemyx[i] >= 750 :
            enemy.enemyx_change[i] = -3
            enemy.enemyy[i] += enemy.enemyy_change[i] 
            
    if bullet.bullety <= 0:
        bullet.bullety = player.playery
        bullet.state = "ready"
        
    # bullet movement...
    if bullet.state == "fire":
        bullet.fire_bullet(bullet.bulletx,bullet.bullety)
        bullet.bullety -=  bullet.bullety_change
    
    # collision of bullet with the enemies...
    
    for i in range(enemy.number_of_enemy):
        if is_collision(enemy.enemyx[i],enemy.enemyy[i],bullet.bulletx,bullet.bullety) :
            bullet.state = "ready"
            bullet.bullety = player.playery
            enemy.enemyx[i] = random.randint(0,600)
            enemy.enemyy[i] =  random.randint(10,100)
    
    # for checking collision with the player and the enemy or also if the enemy is going out of bound........ 
    for i in range(enemy.number_of_enemy):
        
        if enemy.enemyy[i]>=580 or is_collision(enemy.enemyx[i], enemy.enemyy[i], player.playerx, player.playery):
            for i in range(enemy.number_of_enemy):
                enemy.enemyx_change[i] = 0
                enemy.enemyy_change[i] = 0
            player.playerx_change = 0
            player.playery_change = 0
            game.Game_Over()
            break
          
    # calling player method for changing the location of UFO in game window..
    player.player(player.playerx,player.playery)
    
    #enemy.enemy()
    # For creating multiple enemies....
    for i in range(enemy.number_of_enemy):
        enemy.enemy(enemy.enemyImage[i],enemy.enemyx[i],enemy.enemyy[i])
        
    pygame.display.update() #for updating screen again and again...
    