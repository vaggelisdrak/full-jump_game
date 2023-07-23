import pygame
import math
import random
import sys,time,os
from itertools import repeat
from pygame import mixer

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
red = (213, 0, 0)
green = (5, 255, 55)
blue = (0, 0, 213)
purple = (75, 0, 130)
orange = (255,153,51)
cyan = (102,0,51)#ειναι σκουρο κοκκινο
originalcyan = (0,255,255)
grey = (160,160,160)
lightgrey =(224,224,224)

dis_width = 900
dis_height = 300

asset_url1 = 'images/abstract.jpg'
asset_url2 = 'images/absbg.jpg'
asset_url3 = 'images/cube.png'
background = pygame.image.load(asset_url1)
blackbg = pygame.image.load(asset_url2)   
icon = pygame.image.load(asset_url3)
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jump Game')
pygame.display.set_icon(icon)
 
clock = pygame.time.Clock()
offset = repeat((0, 0))

x=100
y=240
speed = 5
jumpcount = 8
isjump = False

xobs1 = 900
xobs2 = 1300
xobs3 = 1000
xobs4 = 1500
speedobs = 6

highscore = 0
score = 0
fontsize = 0
life = 50


score_font = pygame.font.Font('freesansbold.ttf', 25)
fpsfont = pygame.font.Font('freesansbold.ttf', 15)

class particle():
    def __init__(self,x1,y1):
        self.x1=x1
        self.y1=y1
        self.x1_vel = random.randrange(-6,-1)*3
        self.y1_vel = random.randrange(1,4)*3
        self.lifetime = 0
        self.radious = 9
        
    
    def draw(self,window):
        self.lifetime +=1 #+`1`kathe frame
        self.radious -=0.4
        if self.lifetime<17:
            self.x1 +=self.x1_vel
            self.y1 +=self.y1_vel
            pygame.draw.rect(dis,orange,[int(self.x1),int(self.y1),abs(int(self.radious)),abs(int(self.radious)+1)])
            
particles=[]

class orparticle():
    def __init__(self,orx1,ory1):
        self.orx1=orx1
        self.ory1=ory1
        self.orx1_vel = random.randrange(-6,-1)*2
        self.ory1_vel = random.randrange(1,4)*2
        self.orlifetime = 0
        self.orradious = 10
        
    
    def draw(self,window):
        global clr
        self.orlifetime +=1 #+`1`kathe frame
        self.orradious -=0.4
        if self.orlifetime<27:
            self.orx1 +=self.orx1_vel
            self.ory1 +=self.ory1_vel
            #pygame.draw.circle(dis,black,(int(self.x1),int(self.y1)),abs(int(self.radious)-1))
            #pygame.draw.circle(dis,yellow,(int(self.x1-3),int(self.y1-3)),abs(int(self.radious)-2))
            #pygame.draw.circle(dis,red,(int(self.x1),int(self.y1)),abs(int(self.radious)))
            pygame.draw.rect(dis,clr,[int(self.orx1),int(self.ory1),abs(int(self.orradious)),abs(int(self.orradious))])
            
orparticles=[]

class dparticle():
    def __init__(self,dx1,dy1):
        self.dx1=dx1
        self.dy1=dy1
        self.dx1_vel = random.randrange(-6,6)*2
        self.dy1_vel = random.randrange(1,6)*2
        self.dlifetime = 0
        self.dradious = 10
        
    
    def draw(self,window):
        self.dlifetime +=1 #+`1`kathe frame
        self.dradious -=0.4
        if self.dlifetime<37:
            self.dx1 +=self.dx1_vel
            self.dy1 +=self.dy1_vel
            pygame.draw.rect(dis,grey,[int(self.dx1),int(self.dy1),abs(int(self.dradious)),abs(int(self.dradious))])
            
dparticles=[]

def shake(L):
    s = -1
    for _ in range(0, 4):
        for x in range(0, L, 5):
            yield (x*s, 0)
        for x in range(L, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)

def score1():
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 10])

def highscore1():
    value = score_font.render("Highscore: " + str(highscore), True, white)
    dis.blit(value, [140, 10])
    
def retry():
    global score1
    global fontsize
    global typewriter
    now = pygame.time.get_ticks()
    colors = 0
    dis.blit(blackbg, (0,0))
    score1()
    highscore1()

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = fpsfont.render(fps, 2, pygame.Color("white"))
	return fps_text

def obstacle1():
    global score
    global xobs1
    xobs1 -= speedobs
    pygame.draw.rect(dis,purple,[int(xobs1),290-h,30,h])
    pygame.draw.rect(dis,white,[int(xobs1),290-h,30,h],2)
    if xobs1<0:
        score += 1
        xobs1 = 900
        pygame.draw.rect(dis,purple,[int(xobs1),290-h,30,h])
        pygame.draw.rect(dis,white,[int(xobs1),290-h,30,h],1)

def obstacle2():
    global score
    global xobs2
    xobs2 -= speedobs
    pygame.draw.rect(dis,yellow,[int(xobs2),260,60,30])
    pygame.draw.rect(dis,white,[int(xobs2),260,60,30],1)
    if xobs2<0:
        score += 1
        xobs2 = 1300
        pygame.draw.rect(dis,yellow,[int(xobs2),260,60,30])
        pygame.draw.rect(dis,white,[int(xobs2),260,60,30],1)

def obstacle3():
    global score
    global xobs3
    xobs3 -= 5
    pygame.draw.polygon(dis, orange, [(xobs3,10),(xobs3+70,10),(xobs3+35,70)])
    pygame.draw.polygon(dis, white, [(xobs3,10),(xobs3+70,10),(xobs3+35,70)],1)
    if xobs3<0:
        score += 1
        xobs3 = 1000
        pygame.draw.polygon(dis, orange, [(xobs3,10),(xobs3+100,10),(xobs3+50,70)])
        pygame.draw.polygon(dis, white, [(xobs3,10),(xobs3+70,10),(xobs3+35,70)],1)

def obstacle4():
    global score
    global xobs4
    xobs4 -= 5
    pygame.draw.polygon(dis, cyan, [(xobs4,10),(xobs4+70,10),(xobs4+35,50)])
    pygame.draw.polygon(dis, white, [(xobs4,10),(xobs4+70,10),(xobs4+35,50)],1)
    if xobs4<0:
        score +=1
        xobs4 = 1600
        pygame.draw.polygon(dis, cyan, [(xobs4,10),(xobs4+70,10),(xobs4+35,50)])
        pygame.draw.polygon(dis, white, [(xobs4,10),(xobs4+70,10),(xobs4+35,50)],1)

loop = True
while loop:
    game_over = False
    running = True
    x=100
    y=240
    speed = 5
    jumpcount = 8
    isjump = False

    xobs1 = 900
    xobs2 = 1300
    speedobs = 6
    colors = 0
    txtsize = 0
    colordur = 0
    colorlife = 0
    h = 60
    r=255
    g=0
    b=0
    clr = (r,g,b)

    score = 0
    pygame.mixer.music.load('bgmusic.mp3')
    pygame.mixer.music.play(0)
    soundstime = 0
    soundstime1 = 0
    
    with open("highscore.txt", "r") as f:
        highscore = f.read()
    while running is True:
        while game_over is True:
            #print('game over')
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            retry()
            colordur += 1

            #allagh text

            gameover = pygame.font.Font('freesansbold.ttf', 45)
            message = 'GAME OVER'
            value1 = gameover.render(message, True, (colors,colors,colors))
            dis.blit(value1, [310, 100])
            value2 = score_font.render('Press ENTER to play again', True, (colors,colors,colors))
            dis.blit(value2, [290, 180])

            if (colors <= 255) and colordur < 4000:
                colors += 0.2
            elif colordur > 3000:
                if (colors >= 0):
                    colors -= 0.22
                else:
                   colors  = 0

            for orparticle_ in orparticles:
                orparticle_.draw(dis)
            life = 50
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.init()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and x>0:
            x -= speed  
        if keys[pygame.K_RIGHT] and x<800:
            x += speed  
        if not(isjump):
            if keys[pygame.K_SPACE]:
                isjump = True
        else:
            if jumpcount >= -8:
                y -= (jumpcount*abs(jumpcount))*0.5
                jumpcount -=0.5
                if y==240:
                    offset = shake(10)
            else:
                isjump = False
                jumpcount = 8

        #background---------------------------------------------------------------------------

        #dis.blit(background, (0,0))
        #pygame.draw.rect(dis,black,(0,0,900,300))
        dis.blit(blackbg,next(offset))
        dis.blit(update_fps(), (830,20))
        k = random.randint(20,850)
        l = random.randint(15,270)
        orparticles.append(orparticle(k,l))
        for orparticle_ in orparticles:
            orparticle_.draw(dis)
        score1()
        highscore1()

        #player-------------------------------------------------------------------------------
        pygame.draw.rect(dis,clr,[0,0,9000,10])
        pygame.draw.rect(dis,clr,[0,290,9000,10])
        pygame.draw.rect(dis,red,[int(x),int(y),50,50])
        pygame.draw.rect(dis,red,[int(x),int(y-40),50,5])
        pygame.draw.rect(dis,green,[int(x),int(y-40),int(life),5])
        pygame.draw.rect(dis,white,[int(x),int(y-40),50,5],1)
        
        if y==240:
            particles.append(particle(x+5,y+30))
            for particle_ in particles:
                particle_.draw(dis)

        #empodia-------------------------------------------------------------------------------

        obstacle1()
        obstacle2()
        obstacle3()
        obstacle4()

        #sygkroysh me empodia------------------------------------------------------------------

        distance = math.sqrt((math.pow(x - xobs1, 2)) + (math.pow(y - (280-h), 2)))
        if distance < 42:
            print('game over1')
            soundstime += 1
            isjump = False
            speed = 0
            speedobs = 0
            #pygame.mixer.music.load('losingsound.wav')
            #pygame.mixer.music.play(0)
            if soundstime>=5:
                print('game over1-2')
                game_over = True

        distance1 = math.sqrt((math.pow(x - xobs2, 2)) + (math.pow(y - 240, 2)))
        if distance1 < 57:
            print('game over2')
            soundstime += 1
            speed = 0
            isjump = False
            speedobs = 0
            #pygame.mixer.music.load('losingsound.wav')
            #pygame.mixer.music.play(0)
            if soundstime>=5:
                print('game over2-2')
                game_over = True

        distance2 = math.sqrt((math.pow(x - xobs3, 2)) + (math.pow(y - 90, 2)))
        if distance2 < 45:
            print('game over3')
            lostsound = mixer.Sound('losingsound.wav')
            lostsound.play()
            life -= 0.2
            offset = shake(20)
            oldobs3 = xobs3
            if soundstime <10:
                dparticles.append(dparticle(oldobs3,50))
                for dparticle_ in dparticles:
                    dparticle_.draw(dis)
            soundstime1 += 1
            if soundstime1>=10:
                xobs3 = 1000
                soundstime1 = 0
        
        #-----------------------------------------------------------------------------------------
        
        if life <= 0:
            print('game over')
            game_over = True

        if score >= 10:
                speedobs += 0.0002
        if score>=int(highscore):
            highscore=score

        #allagh xromaton--------------------------------------------------------------------------
        
        if 5<=score<20:#potokali
            clr = (r,g,b)
            if g<=128:
                g +=1
            if xobs1<=0:
                h = random.randrange(40,80)
        if 20<=score<=50:#kitrino
            clr = (r,g,b)
            if g<255:
                g+=1
            h = 60
        if 50<score<80:#prasino
            clr = (r,g,b)
            if r>0:
                r-=1
            h = 65
        if 80<=score<110:#galazio
            clr = (r,g,b)
            if b<255:
                b+=1
            h = 70
        if 110<=score<140:#mple
            clr = (r,g,b)
            if g>0:
                g-=1
            h = 75
        if 140<=score<170:#mov
            clr = (r,g,b)
            if r<153 or b>153:
                r+=1
                b-=1
            h = 80
        if 170<=score<200:#aspro
            clr =(r,g,b)
            if g<255:
                g+=1
            if r<255:
                r+=1
            if b<255:
                b+=1
            h = 85
        if score>=200:
            clr =(r,g,b)
            if g>0 or r>0 or b>0:
                g-=1
                r-=1
                b-=1
            h = 85
        pygame.display.update()
        clock.tick(60+3*(speedobs))