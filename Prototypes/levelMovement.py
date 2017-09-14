import pygame
import os, sys


backgroundImage = pygame.image.load("background.png")
floorImage = pygame.image.load("floor.png")
heroImage = os.path.join("D:\skola\Programovani\Python\superFabio", "player.png")
pipeImage = os.path.join("D:\skola\Programovani\Python\superFabio", "pipe.png")
wallImage = os.path.join("D:\skola\Programovani\Python\superFabio", "invisWall.png")
finishOne = os.path.join("D:\skola\Programovani\Python\superFabio", "finish1.png")
finishTwo = os.path.join("D:\skola\Programovani\Python\superFabio", "finish2.png")


black = 0,0,0
global dist #Unified movement for the whole game, more or less arbitrary
dist = 3


class Hero(pygame.sprite.Sprite):
	def __init__(self, x = 100, y = 150):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(heroImage)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.jump = 0 #Variable for completing a jump
		self.rect.x = x
		self.rect.y = y
		self.prevX = x
		self.prevY = y

	#Movement
	def handle_keys(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE]:
			if self.jump == 0:
				self.jump += 1
		if pressed[pygame.K_LEFT]:
			self.prevX = self.x
			self.x -= dist
			self.rect.x -= dist
			if self.x < 0:
				self.x = 0
				self.rect.x = 0
		if pressed[pygame.K_RIGHT]:
			self.prevX = self.x
			self.x += dist
			self.rect.x += dist
			if self.x > 350:
				self.x = 350
				self.rect.x = 350

		if self.jump > 0 and self.jump < 150:
			self.prevY = self.y
			self.y -= 6 #6 is the speed of the jump, arbitrary
			self.rect.y -= 6
			self.jump += 6

		if self.jump > 149 and self.jump < 300:
			self.prevY = self.y
			self.jump += 6

		if self.jump >= 300: #300 "units" is the height of the jump
			self.prevY = self.y
			self.jump = 0

	def draw(self, surface):
		screen.blit(self.image, self.rect)


class Pipe(pygame.sprite.Sprite): 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(pipeImage)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

	def pipeDraw(self, surface):
		screen.blit(self.image, self.rect)


class invisibleWall(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(wallImage)
		self.rect = self.image.get_rect()
		self.rect.x = 200
		self.rect.y = 0
		self.x = x
		self.y = y

class finished(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(finishOne)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x = x
		self.y = y
		self.finVer = True
		self.imageTwo = pygame.image.load(finishTwo)

	def finDraw(self, surface):
		if self.finVer == True:
			screen.blit(self.image, self.rect)
			self.finVer = False
		else:
			screen.blit(self.imageTwo, self.rect)
			self.finVer = True


pygame.init()
screen = pygame.display.set_mode((400, 300))

hero = Hero() 
pipeOne = Pipe(150, 175)
pipeTwo = Pipe(300, 150)
pipeThree = Pipe(500, 150)
wall = invisibleWall(200, 0)
finished = finished(700, 0)

clock = pygame.time.Clock() #To get slower movement, you need a clock

pipes=pygame.sprite.Group(pipeOne, pipeTwo, pipeThree)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #Exit with top right X
			sys.exit()
		if event.type == pygame.KEYDOWN: #Exit with Escape
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	#Collision detection with a specific pipe that is in the group pipes
	collision = pygame.sprite.spritecollide(hero, pipes, False)
	if collision:
		if ((collision[0]).y - hero.y) < 50: #Y-axis barrier
			hero.y -= dist
			hero.rect.y -= dist
		
		#X-axis barriers, positive side needs limits because otherwise, the hero would slide back
		if ((collision[0]).x - hero.x) < 47 and ((collision[0]).x - hero.x) > 40:
			hero.x -= dist
			hero.rect.x -= dist
			
		if ((collision[0]).x - hero.x) < -45:
			hero.x += dist
			hero.rect.x += dist

	#Collision with the invisible wall to create movement of the level
	point = pygame.sprite.collide_mask(hero, wall)
	if point:
		if point[1] > 25:
			hero.y -= dist
			hero.rect.y -= dist
		elif point[0] != 0:
			hero.x -= dist
			hero.rect.x -= dist
		elif point[0] == 0:
			hero.x += dist
			hero.rect.x += dist
		for i in pipes:
			i.x -= dist
			i.rect.x -= dist
		finished.x -= dist
		finished.rect.x -= dist

	#Turns off the game once finish is reached
	end = pygame.sprite.collide_mask(hero, finished)
	if end:
		print ("You have won")
		sys.exit()

	hero.handle_keys()

	#Gravity for the hero
	if hero.y < 150:
		hero.y += dist
		hero.rect.y += dist

	#Bliting
	screen.fill(black)
	screen.blit(backgroundImage,[0,0])
	hero.draw(screen)
	finished.finDraw(screen)
	for i in pipes:
		i.pipeDraw(screen)
	screen.blit(floorImage, [0,200])
	pygame.display.update()
	clock.tick(60)
