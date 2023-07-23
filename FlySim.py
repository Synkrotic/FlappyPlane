import pygame as pg, sys, os, random

# Setup
pg.init()
clock = pg.time.Clock()

# Variables
width = 1366
height = 768
fps = 60
upSpeed = 5
enemySpeed = 50
points = 0
enemySpawnSpeed = 1200 # Milliseconds

text_surface = "0"

dead = False
kbinput = None
paused = False

screenRes = (width, height)
start = -enemySpawnSpeed

# Plane animation
planes = ["Sprites/PlaneUp.png", "Sprites/PlaneDown.png"]

# Screen
screen = pg.display.set_mode(screenRes)
background = pg.image.load("Sprites/PlatformerBackground.png")
pg.display.set_caption("FlySim")
pg.mouse.set_visible(False)

# Colours
blur = pg.image.load("Sprites/Blur.png")
white = (255, 255, 255)
black = (0, 0, 0)

# Classes
class Player(pg.sprite.Sprite):
    def __init__(self, playerimg, posX, posY):
        super().__init__()
        self.image = pg.image.load(playerimg)
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.direction = "right"
    def Update(self):
        self.rect.center = (self.posX, self.posY)
        kbinput = pg.key.get_pressed()
        if kbinput[pg.K_SPACE]:
            self.image = pg.image.load(planes[0])
            self.posY -= upSpeed
        else:
            self.image = pg.image.load(planes[1])
            self.posY += upSpeed/2
        if self.posY <= 0 or self.posY >= height:
            Pausing(True, False)
            global dead
            dead = True


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemyimg, posX, posY):
        super().__init__()
        self.image = pg.image.load(enemyimg)
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.pointgiven = False
    def Update(self):
        if self.rect.collidepoint(player.posX, player.posY):
            Pausing(True, False)
            global dead
            dead = True
        self.rect.center = (self.posX, self.posY)
        self.posX -= enemySpeed
        if self.posX <= 0:
            self.kill()
    def Points(self):
        global points
        if self.posX <= player.posX and self.pointgiven == False:
            self.pointgiven = True
            points += 1
            print(points)

# Sprites
player = Player(planes[1], width*.30, height/2)
player_group = pg.sprite.Group()
player_group.add(player)

enemy_group = pg.sprite.Group()

# Methodes
def Quit():
    pg.quit()
    sys.exit()

def Update():
    RenderSprites()
    SpawnEnemy()
    DisplayPoints()
    Pausing(True, True)

def RenderSprites():
    player_group.draw(screen)
    enemy_group.draw(screen)

def DisplayPoints():
    global points
    global text_surface
    font = pg.font.SysFont('Ariel', 75)
    text_surface = font.render(str(points), True, black)

def SpawnEnemy():
    global start
    global enemySpawnSpeed
    now = pg.time.get_ticks()
    if now - start > enemySpawnSpeed:
        start = now
        if enemySpawnSpeed != 300:
            enemySpawnSpeed -= 30
        enemy = Enemy("Sprites/Enemy.png", width, random.randrange(0, height))
        enemy_group.add(enemy)

def Pausing(switch, press):
    global paused
    kbinput = pg.key.get_pressed()
    if press == False:
        paused = switch
        pg.mouse.set_visible(switch)
    elif kbinput[pg.K_ESCAPE]:
        paused = switch
        pg.mouse.set_visible(switch)

# Game loop
while True:
    if paused == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Quit()
        screen.blit(background, (0,0))
        for enemy in enemy_group:
            enemy.Update()
            enemy.Points()
        player.Update()
        Update()
        screen.blit(text_surface, (width/2-30, height/10))
    elif paused == True:
        screen.blit(blur, (0,0))
        if dead == False:
            Pausing(False, False)
    pg.display.flip()
    clock.tick(fps)