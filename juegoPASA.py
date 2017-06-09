import pygame
import time
import random
import numpy as np
import pasa
import math
name="Carlos"
start=time.time()
clandestine = False
screenW=700
screenH=500
done=False
pos = (0,0)
toggle = 0
bn = 0
score = 0
iteracion = 0
espacio=0
arriba=0
abajo=0
izquierda=0
derecha=0
enemy_images=["data/ufo1.png","data/ufo2.png","data/ufo3.png"]
def setup():
        global channel,randomcreation,lastupdate,star,ex,laser,screen,font, player
        pygame.init()
        font = pygame.font.Font(pygame.font.get_default_font(),10)
        pygame.display.set_caption('TP1 PASA')
        pygame.font.init()
        screen=pygame.display.set_mode((screenW,screenH))
        pygame.mixer.init()
        laser=pygame.mixer.Sound("data/laser.wav")
        ex=pygame.mixer.Sound("data/ex.wav")
        #music=pygame.mixer.Sound("data/music.wav")
        starimg=pygame.image.load ("data/itba-sede.jpg").convert()
        star=pygame.transform.scale (starimg,(screenW,screenH))
        print ("BEGIN\n")
        player = Player()
        sprite_list.append(player)
        #music.play()
        #channel=music.play()
        randomcreation=500
        lastupdate=time.time()

class Sprite:
        def __init__(self,image_path="data/sa.png"):
                self.direction=random.randint(-1,1)
                self.slowness=1
                self.x=0
                self.y=0
                self.image=pygame.image.load(image_path)
                self.image=pygame.transform.scale(self.image,(50,50))
                self.width=50
                self.height=50
        def update(self):
                if random.randint(1,250) == 1:
                        enemybullet = Enemybullet()
                        sprite_list.append(enemybullet)
                        enemybullet.x=self.x+15
                        enemybullet.y=self.y+30
                if toggle%self.slowness==0:
                        if self.x<0:
                                self.direction=1
                        elif self.x>screenW-self.width:
                                self.direction=-1
                        if self.y<screenH+150: #change to 'screenH-150' if want bad guys to stop going L/R before end
                                self.x+=self.direction
                        self.y+=1
                if self.y > screenH+self.width:
                        sprite_list.remove(self)

class Alien(Sprite):
        def __init__(self,x,y,slowness):
                Sprite.__init__(self,enemy_images[random.randrange(0,len(enemy_images))])
                self.x=x
                self.y=y
                self.slowness=slowness
                sprite_list.append(self)
                self.alien=True

class Rectangle:
        def __init__(self,x,y,width,height):
                self.left = x
                self.top = y
                self.bottom = y+height
                self.right = x+width
def rectangular_intersection(rect1,rect2):
        return not (rect1.right < rect2.left or rect1.left > rect2.right or rect1.bottom < rect2.top or rect1.top > rect2.bottom)

class Player(Sprite):
        global cheat
        def __init__(self):
                Sprite.__init__(self,"data/ufo.png")
                self.image=pygame.transform.scale(self.image,(50,50))
                self.x=screenW/2
                self.y=screenH-50
                self.width =50
                self.height=50
                self.filtro=pasa.filtroTP(0.9, math.pi/6,0.09,5000)
                self.speedx=0
                self.speedy=0
        def update(self):
                global start
                # self.K[0]=self.speedx
                # deltax=np.dot(self.deltax,self.Num)+np.dot(self.K, self.Den)
                # self.x=self.x+deltax
                # start=time.time()
                # self.deltax=self.deltax[-1:]+self.deltax[:-1]
                # self.deltax[0]=deltax
                # self.K=self.K[-1:]+self.K[:-1]
                self.y=self.y+self.speedy
                self.x=self.filtro.run(self.speedx)
                # if self.x < 0:
                #         self.x-=self.speedx
                # if self.x > screenW-30:
                #         self.x-=self.speedx
                for sprite in sprite_list:
                        if sprite != self and not hasattr(sprite,"bullet"):
                                self_rectangle = Rectangle(self.x,self.y,self.width,self.height)
                                other_rectangle=Rectangle(sprite.x,sprite.y,sprite.width,sprite.height)
                                if rectangular_intersection(self_rectangle,other_rectangle)and clandestine== False:
                                                global done
                                                done=True

class Bullet(Sprite):
        def __init__(self):
                Sprite.__init__(self,"data/b.png")
                self.image=pygame.transform.scale(self.image,(8,12))
                self.width=8
                self.height=12
                self.bullet = True
                #laser.play()
        def update(self):
                global bn, score
                kill_list = []
                self_rectangle = Rectangle(self.x,self.y,self.width,self.height)
                for sprite in sprite_list:
                        if hasattr(sprite,"alien"):
                                other_rectangle=Rectangle(sprite.x,sprite.y,sprite.width,sprite.height)
                               # kill_list.append(sprite)
                                if rectangular_intersection(self_rectangle,other_rectangle):
                                        kill_list.append(sprite)
                                        ex.play()
                                        if self not in kill_list:
                                                kill_list.append(self)
                                                bn-=1
                        if hasattr(sprite,"enemybullet"):
                                other_rectangle=Rectangle(sprite.x,sprite.y,sprite.width,sprite.height)
                                if rectangular_intersection(self_rectangle,other_rectangle):
                                        kill_list.append(sprite)
                                        if self not in kill_list:
                                                kill_list.append(self)
                                                bn-=1
                if self.y < 0:
                        kill_list.append(self)
                        bn-=1
                for sprite in kill_list:
                        if sprite in sprite_list:
                                sprite_list.remove(sprite)
                                if hasattr(sprite,"alien"):
                                        score+=100
                self.y-=15

class Enemybullet(Sprite):
        def __init__(self):
                Sprite.__init__(self,"data/eb.png")
                self.image=pygame.transform.scale(self.image,(8,12))
                self.width=8
                self.height=12
                self.enemybullet = True
        def update(self):
                kill_list = []
                if self.y > screenH:
                        kill_list.append(self)
                for sprite in kill_list:
                        if sprite in sprite_list:
                                sprite_list.remove(sprite)
                self.y+=0.5

def draw_frame(alist,toggle):
        global score
        global name
        global start
        pygame.draw.rect(screen,(0,0,0),screen.get_rect())
        screen.blit(star,(0,0))
        times = time.time()-start
        timem = font.render(str(times),True,(255,255,255))
        screen.blit(timem,(10,screenH-20))
        timew = font.render("TIME",True,(255,255,255))
        screen.blit(timew,(10,screenH-40))
        scorenumber = font.render(str(score),True,(255,255,255))
        screen.blit(scorenumber,(10,screenH-60))
        scorem = font.render("SCORE",True,(255,255,255))
        screen.blit(scorem,(10,screenH-80))
        namem = font.render(str(name),True,(255,255,255))
        screen.blit(namem,(10,screenH-100))
        for sprite in alist:
                position = (sprite.x,sprite.y)
                screen.blit(sprite.image,position)
        pygame.display.flip()

def update_sprites():
        global toggle,randomcreation,lastupdate
        toggle=(toggle+1)
        if random.randint(1,50) == 1:
                alien = Alien(random.randint(0,screenW-50),random.randint(50,250),1)
        for sprite in sprite_list:
                sprite.update()
sprite_list = []
for x in range(5):
        Alien(random.randint(0,screenW-50),random.randint(50,250),random.randint(1,3))
def readKey():
    global espacio, arriba, abajo, izquierda, derecha
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                espacio=1
            if event.key==pygame.K_LEFT:
                izquierda=1
            if event.key==pygame.K_RIGHT:
                derecha=1
            if event.key==pygame.K_UP:
                arriba=1
            if event.key==pygame.K_DOWN:
                abajo=1
        if event.type==pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                espacio=0
            if event.key==pygame.K_LEFT:
                izquierda=0
            if event.key==pygame.K_RIGHT:
                derecha=0
            if event.key==pygame.K_UP:
                arriba=0
            if event.key==pygame.K_DOWN:
                abajo=0
    return arriba,abajo,izquierda,derecha,espacio

def loop(deltax,deltay,disparo):
        global channel,bn,alien,clandestine,done,player,music,iteracion,espacio
        iteracion += 1
#        if not channel.get_busy():
 #               channel=music.play()
        if random.randint(1,1000) == 1:
                        alien = Alien(random.randint(0,screenW-50),random.randint(50,250),random.randint(1,3))
        if disparo==1:
            if bn<5:
                bullet = Bullet()
                sprite_list.append(bullet)
                bullet.x=player.x+11
                bullet.y=player.y
                bn+=1
            espacio=0
        if bn<0:
            bn=0
        player.speedx=deltax
        player.speedy=deltay
        draw_frame(sprite_list,0)
        update_sprites()
        return player.x

def end():
        pygame.quit()