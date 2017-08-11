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
			self.y -= 6 #2*gravity is the speed of the jump, arbitrary
			self.rect.y -= 6
			self.jump += 6

		if self.jump > yAxis - 1 and self.jump < yAxis:
			self.prevY = self.y
			self.jump += 6

		if self.jump >= yAxis: #300 "units" is the height of the jump
			self.prevY = self.y
			#self.jump = 0

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
pipeOne = Pipe(150, (yFloor - 50) - 25)
pipeTwo = Pipe(350, (yFloor - 50) - 50)
pipeThree = Pipe(900, (yFloor - 50) + 25)
wall = InvisibleWall(xAxis/2, (yFloor - 50))
finished = Finished(1400, yFloor - 300)
lavaOne = Lava(600)
coinOne = Coin(pipeOne.x + 11, (yFloor - 50) - 75) #X coordinate is 150 + 12 because 12 looks nice
coinTwo = Coin(pipeTwo.x + 11, (yFloor - 50) - 100)
coinThree = Coin(pipeTwo.x + 75, (yFloor - 50) + 5)
coinFour = Coin(coinThree.x + 55, (yFloor - 50) + 5)
coinFive = Coin(coinFour.x + 55, (yFloor - 50) + 5)
coinSix = Coin(lavaOne.x + 75, (yFloor - 50) + 5)
coinSeven = Coin(coinSix.x + 55, (yFloor - 50) + 5)
coinEight = Coin(coinSeven.x + 55, (yFloor - 50) + 5)
coinNine = Coin(coinEight.x + 55, (yFloor - 50) + 5)
dalekOne = Dalek(200)
dalekTwo = Dalek(500)


pipes = pygame.sprite.Group(pipeOne, pipeTwo, pipeThree)
coins = pygame.sprite.Group(coinOne, coinTwo, coinThree, coinFour, coinFive, coinSix, coinSeven, coinEight, coinNine)
daleks = pygame.sprite.Group(dalekOne, dalekTwo)
lavas = pygame.sprite.Group(lavaOne)

clock = pygame.time.Clock() #To get slower movement, you need a clock

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
		if ((collision[0]).y - hero.y) < 55 and ((collision[0]).y - hero.y) > 45: #Y-axis barrier
			hero.y -= dist
			hero.rect.y -= dist
			hero.jump = 0
		
		#X-axis barriers, positive side needs limits because otherwise, the hero would slide back
		elif ((collision[0]).x - hero.x) < 47 and ((collision[0]).x - hero.x) > 40:
			hero.x -= dist
			hero.rect.x -= dist
			
		elif ((collision[0]).x - hero.x) < -45:
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
		for k in coins:
			k.x -= dist
			k.rect.x -= dist
		for k in daleks:
			k.x -= dist
			k.rect.x -= dist
		for k in lavas:
			k.x -= dist
			k.rect.x -= dist
		finished.x -= dist
		finished.rect.x -= dist

	#Counts the number of coins
	collection = pygame.sprite.spritecollide(hero, coins, False)
	if collection:
		if collection[0].full == True:
			coinage += 1
			collection[0].full = False

	#Turns off the game once finish is reached
	end = pygame.sprite.collide_mask(hero, finished)
	if end:
		print ("You have won")
		print ("Number of coins:", coinage)
		print ('Your time:', time)
		sys.exit()

	#Ends the game once the hero steps on lava
	deathLava = pygame.sprite.spritecollide(hero, lavas, False)
	if deathLava:
		print ('You died')
		print ("Number of coins:", coinage)
		print ('Your time:', time)
		sys.exit()

	#Collision detection with a specific dalek that is in the group daleks
	collision = pygame.sprite.spritecollide(hero, daleks, False)
	if collision:
		if ((collision[0]).y - hero.y) <= 48 and ((collision[0]).y - hero.y) > 45:
			(collision[0]).y = 5000 #Just get it off the screen
			(collision[0]).rect.y = 5000
		
		#X-axis barriers, positive side needs limits because otherwise, the hero would slide back
		elif((collision[0]).x - hero.x) < 47 and ((collision[0]).x - hero.x) > 40:
			print ('You died')
			print ("Number of coins:", coinage)
			print ('Your time:', time)
			sys.exit()
			
		elif ((collision[0]).x - hero.x) < -45:
			print ('You died')
			print ("Number of coins:", coinage)
			print ('Your time:', time)
			sys.exit()

	#Collision between Pipes and Daleks
	#The thing is a DICTIONARY, THIS IS IMPORTANT! READ THIS AND DON'T GET STUCK LIKE AN IDIOT
	collisionPipesDaleks = pygame.sprite.groupcollide(daleks, pipes, False, False)
	if collisionPipesDaleks:
		for i in collisionPipesDaleks: #i is the dalek
			for k in collisionPipesDaleks[i]: #k is the pipe
				if (i.x - k.x) < 47 and (i.x - k.x) > 40:
					i.x += dist
					i.rect.x += dist
					i.direction = True
				if (i.x - k.x) < -47:
					i.x -= dist
					i.rect.x -= dist
					i.direction = False

	for i in daleks:
		i.dalekMove()
	hero.handle_keys()

	#Gravity for the hero
	if hero.y < (yFloor - 50):
		hero.y += dist
		hero.rect.y += dist
	if hero.y == (yFloor - 50):
		hero.jump = 0

	#Bliting
	screen.fill(black)
	screen.blit(backgroundImage,[0,0])
	hero.draw(screen)
	finished.finDraw(screen)
	for k in pipes:
		k.pipeDraw(screen)
	for k in coins:
		k.coinDraw(screen)
	for k in daleks:
		k.dalekDraw(screen)
	screen.blit(floorImage, [0,yFloor])
	screen.blit(floorImage, [400,yFloor])
	for k in lavas:
		k.lavaDraw(screen)
	pygame.display.update()
	clock.tick(60)
	time += 1
