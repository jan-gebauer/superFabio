import pygame
import os, sys


backgroundImage = pygame.image.load("background.png")
floorImage = pygame.image.load("floor.png")
heroImage = os.path.join("D:\skola\Programovani\Python\superFabio", "player.png")
pipeImage = os.path.join("D:\skola\Programovani\Python\superFabio", "pipe.png")

black = 0,0,0


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
			self.x -= 3
			self.rect.x -= 3
			if self.x < 0:
				self.x = 0
				self.rect.x = 0
		if pressed[pygame.K_RIGHT]:
			self.prevX = self.x
			self.x += 3
			self.rect.x += 3
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
	def __init__(self, x, y, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(pipeImage)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		self.name = name

	def pipeDraw(self, surface):
		screen.blit(self.image, self.rect)

pygame.init()
screen = pygame.display.set_mode((400, 300))

hero = Hero() 
pipeOne = Pipe(150, 175, "pipeOne")
pipeTwo = Pipe(300, 150, "pipeTwo")

clock = pygame.time.Clock() #To get slower movement, you need a clock

pipes=pygame.sprite.Group(pipeOne, pipeTwo)

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
			hero.y -= 3
			hero.rect.y -= 3
		
		#X-axis barriers, positive side needs limits because otherwise, the hero would slide back
		if ((collision[0]).x - hero.x) < 47 and ((collision[0]).x - hero.x) > 40:
			hero.x -= 3
			hero.rect.x -= 3
			
		if ((collision[0]).x - hero.x) < -45:
			hero.x += 3
			hero.rect.x += 3

	hero.handle_keys()

	#Gravity for the hero
	if hero.y < 150:
		hero.y += 3
		hero.rect.y += 3

	#Bliting
	screen.fill(black)
	screen.blit(backgroundImage,[0,0])
	screen.blit(floorImage, [0,200])
	hero.draw(screen)
	pipeOne.pipeDraw(screen)
	pipeTwo.pipeDraw(screen)
	pygame.display.update()
	clock.tick(60)
