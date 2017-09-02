import pygame
import os, sys


backgroundImage = pygame.image.load("background.png")
floorImage = pygame.image.load("floor.png")
heroImage = os.path.join("D:\skola\Programovani\Python\superFabio", "player.png")
pipeImage = os.path.join("D:\skola\Programovani\Python\superFabio", "pipe.png")
wallImage = os.path.join("D:\skola\Programovani\Python\superFabio", "invisWall.png")
finishOne = os.path.join("D:\skola\Programovani\Python\superFabio", "finish1.png")
finishTwo = os.path.join("D:\skola\Programovani\Python\superFabio", "finish2.png")
lavaImage = os.path.join("D:\skola\Programovani\Python\superFabio", "lava.png")
coinFull = os.path.join("D:\skola\Programovani\Python\superFabio", "coinFull.png")
coinEmpty = os.path.join("D:\skola\Programovani\Python\superFabio", "coinEmpty.png")
dalekOneImage = os.path.join("D:\skola\Programovani\Python\superFabio", "dalekOne.png")
dalekTwoImage = os.path.join("D:\skola\Programovani\Python\superFabio", "dalekTwo.png")
dalekThreeImage = os.path.join("D:\skola\Programovani\Python\superFabio", "dalekThree.png")


black = 0,0,0
global dist #Unified movement for the whole game, more or less arbitrary
dist = 3
coinage = 0
time = 0
xAxis = 800
yAxis = 400
heroHeight = 50
yFloor = yAxis - 3*heroHeight
gravity = 3

class Hero(pygame.sprite.Sprite):
	def __init__(self, x = xAxis/10, y = yFloor - 50):
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
			if self.x > (xAxis - 50):
				self.x = (xAxis - 50)
				self.rect.x = (xAxis - 50)

		if self.jump > 0 and self.jump < yAxis/2:
			self.prevY = self.y
			self.y -= 2*gravity #2*gravity is the speed of the jump, arbitrary
			self.rect.y -= 2*gravity
			self.jump += 2*gravity

		if self.jump > yAxis - 1 and self.jump < yAxis:
			self.prevY = self.y
			self.jump += 2*gravity

		if self.jump >= yAxis: #300 "units" is the height of the jump
			self.prevY = self.y

	def draw(self, surface):
		screen.blit(self.image, self.rect)

class Dalek(pygame.sprite.Sprite):
	def __init__(self, x, y = yFloor - 50):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(dalekOneImage)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		self.phase = 1
		self.pTwo = pygame.image.load(dalekTwoImage)
		self.pThree = pygame.image.load(dalekThreeImage)
		self.direction = False #False - Left, True - Right

	def dalekMove(self):
		if self.direction == False:
			self.x -= dist/3
			self.rect.x -= dist/3
		else:
			self.x += dist/3
			self.rect.x += dist/3

	def dalekDraw(self, surface):
		if self.phase == 1:
			screen.blit(self.image, self.rect)
			self.phase += 1
		elif self.phase == 2:
			screen.blit(self.pTwo, self.rect)
			self.phase += 1
		else:
			screen.blit(self.pThree, self.rect)
			self.phase = 1



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

class Lava(pygame.sprite.Sprite): 
	def __init__(self, x, y = yFloor - 1):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(lavaImage)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

	def lavaDraw(self, surface):
		screen.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite): 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(coinFull)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		self.full = True
		self.imageEmpty = pygame.image.load(coinEmpty)

	def coinDraw(self, surface):
		if self.full == True:
			screen.blit(self.image, self.rect)
		else:
			screen.blit(self.imageEmpty, self.rect)


class InvisibleWall(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(wallImage)
		self.rect = self.image.get_rect()
		self.rect.x = xAxis/2
		self.rect.y = 0
		self.x = x
		self.y = y

class Finished(pygame.sprite.Sprite):
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
screen = pygame.display.set_mode((xAxis, yAxis))

hero = Hero()
wall = InvisibleWall(xAxis/2, (yFloor - 50))
finished = Finished(1400, yFloor - 300)

numberOfdaleks = 2
initialDalekx = [200, 500]
daleksArray = []
for c in range(numberOfdaleks):
	daleksArray.append(Dalek(initialDalekx[c]))

numberOflavas = 1
initialLavax = [600]
lavasArray = []
for c in range(numberOflavas):
	lavasArray.append(Lava(initialLavax[c]))

numberOfpipes = 3
initialPipex = [150, 300, 900]
initialPipey = [(yFloor - 50) - 25, (yFloor - 50) - 50, (yFloor - 50) + 25]
pipesArray = []
for c in range(numberOfpipes):
	pipesArray.append(Pipe(initialPipex[c], initialPipey[c]))

numberOfcoins = 9
initial_coin_x = [initialPipex[0] + 11, initialPipex[1] + 11, initialPipex[1] + 75, initialPipex[1] + 75 + 55,
					initialPipex[1] + 75 + 55 + 55, initialLavax[0] + 75, initialLavax[0] + 75 + 55,
					initialLavax[0] + 75 + 55 + 55, initialLavax[0] + 75 + 55 + 55 + 55]
initial_coin_y = [(yFloor - 50) - 75, (yFloor - 50) - 100, (yFloor - 50) + 5, (yFloor - 50) + 5,
					(yFloor - 50) + 5, (yFloor - 50) + 5, (yFloor - 50) + 5, (yFloor - 50) + 5,
					(yFloor - 50) + 5]
coinsArray = []
for c in range(numberOfcoins):
    coinsArray.append(Coin(initial_coin_x[c], initial_coin_y[c]))

clock = pygame.time.Clock() #To get slower movement, you need a clock

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #Exit with top right X
			sys.exit()
		if event.type == pygame.KEYDOWN: #Exit with Escape
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	#Collision detection with a specific pipe that is in the group pipes
	for (i, c) in enumerate(pipesArray):
		collisionHP = pygame.sprite.collide_rect(hero, c)
		if collisionHP:
			#print (c.y - hero.y)
			print (c.x - hero.x)
			if (c.y - hero.y) < 50 and (c.y - hero.y) > 46 and (c.x - hero.x) < 49: #Y-axis barrier
				hero.y -= dist
				hero.rect.y -= dist
				hero.jump = 0
		
			#X-axis barriers, positive side needs limits because otherwise, the hero would slide back
			elif (c.x - hero.x) <= 50 and (c.x - hero.x) > 45:
				hero.x -= dist
				hero.rect.x -= dist
			
			elif (c.x - hero.x) <= -47:
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
		for i in pipesArray:
			i.x -= dist
			i.rect.x -= dist
		for k in coinsArray:
			k.x -= dist
			k.rect.x -= dist
		for k in daleksArray:
			k.x -= dist
			k.rect.x -= dist
		for k in lavasArray:
			k.x -= dist
			k.rect.x -= dist
		finished.x -= dist
		finished.rect.x -= dist

	#Collision for the Hero and the coins
	for (i, c) in enumerate(coinsArray):
		collection = pygame.sprite.collide_rect(hero, c)
		if collection:
			if c.full == True:
				coinage += 1
				c.full = False

	#Turns off the game once finish is reached
	end = pygame.sprite.collide_mask(hero, finished)
	if end:
		print ("You have won")
		print ("Number of coins:", coinage)
		print ('Your time:', time)
		sys.exit()

	#Ends the game once the hero steps on lava
	for (i, c) in enumerate(lavasArray):
		collisionHL = pygame.sprite.collide_rect(hero, c)
		if collisionHL:
			print ('You died')
			print ("Number of coins:", coinage)
			print ('Your time:', time)
			sys.exit()


	#Collision detection with a specific dalek that is in the group daleks
	for (i, c) in enumerate(daleksArray):
		collisionHD = pygame.sprite.collide_rect(hero, c)
		if collisionHD:
			if (c.y - hero.y) <= 48 and (c.y - hero.y) > 45:
				c.y = 5000 #Just get it off the screen
				c.rect.y = 5000
			#X-axis barriers, positive side needs limits because otherwise, the hero would slide back
			elif(c.x - hero.x) < 47 and (c.x - hero.x) > 40:
				print ('You died')
				print ("Number of coins:", coinage)
				print ('Your time:', time)
				sys.exit()
			elif (c.x - hero.x) < -45:
				print ('You died')
				print ("Number of coins:", coinage)
				print ('Your time:', time)
				sys.exit()

	#Collision between Pipes and Daleks
	for (i, c) in enumerate(daleksArray):
		for (k, d) in enumerate(pipesArray):
			collisionPD = pygame.sprite.collide_rect(c,d)
			if collisionPD:
				if (c.x - d.x) < 47 and (c.x - d.x) > 40:
					c.x += dist
					c.rect.x += dist
					c.direction = True
				if (c.x - d.x) < -47:
					c.x -= dist
					c.rect.x -= dist
					c.direction = False

	for i in daleksArray:
		i.dalekMove()
	hero.handle_keys()

	#Gravity for the hero
	if hero.y < (yFloor - 50):
		hero.y += gravity
		hero.rect.y += gravity
	if hero.y == (yFloor - 50):
		hero.jump = 0

	#Bliting
	screen.fill(black)
	screen.blit(backgroundImage,[0,0])
	hero.draw(screen)
	finished.finDraw(screen)
	for k in pipesArray:
		k.pipeDraw(screen)
	for k in coinsArray:
		k.coinDraw(screen)
	for k in daleksArray:
		k.dalekDraw(screen)
	screen.blit(floorImage, [0,yFloor])
	screen.blit(floorImage, [400,yFloor])
	for k in lavasArray:
		k.lavaDraw(screen)
	pygame.display.update()
	clock.tick(60)
	time += 1
