import sys, pygame
pygame.init()

screen = pygame.display.set_mode((400, 300))
black = 0,0,0
x = 200
y = 150

background_image = pygame.image.load("background.png")
hero = pygame.image.load("player.png")

heroRect = hero.get_rect() #You have to make an object to move
heroRect.x = x
heroRect.y = y
jump = False
grounded = True

clock = pygame.time.Clock() #To get slower movement, you need a clock

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #Exit with top right X
			sys.exit()
		if event.type == pygame.KEYDOWN: #Exit with Escape
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	#Movement
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_SPACE]:
		if grounded == True:
			grounded = False
			jump = True
	if pressed[pygame.K_LEFT]:
		x -= 3
		if x < 0:
			x = 0
	if pressed[pygame.K_RIGHT]:
		x += 3
		if x > 350:
			x = 350
	
	if jump == True:#prevent infinite jumping
		if y < 54:
			jump = False
		y -= 3
	
	if y < 150 and jump == False:#Make the box fall
		y += 3		
	if y == 150:#Check, whether the box is on the ground
		grounded = True

	heroRect.x = x
	heroRect.y = y
	screen.fill(black) #Wipes the screen
	screen.blit(backgroundImage,[0,0])
	screen.blit(hero, heroRect) #Draws the actual image in the certain place
	pygame.display.flip() #"Commits" the change
	clock.tick(60)

