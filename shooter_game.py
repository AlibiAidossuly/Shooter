from random import *
from pygame import *
from time import sleep

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('SHOOTER')
back = image.load('galaxy.jpg')
back = transform.scale(back,(win_width,win_height))
clock = time.Clock()
FPS = 60
music_play = True
font.init()
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()

font = font.SysFont('Comic Sans MS', 40)
points = 0
points_title = font.render('Счёт:'+str(points), True, (255,255,255))
miss = 0
miss_title = font.render('Пропущено:'+str(miss), True, (255,255,255))
win = font.render('Победа', True, (30,255,0))
lose = font.render('Пройгрыш', True, (255,30,0))
fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
	def __init__(self,picture,width,height,x,y,speed):
		super().__init__()
		self.width = width
		self.height = height
		self.image = transform.scale(image.load(picture), (self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed = speed
	def reset(self):
		window.blit(self.image, (self.rect.x,self.rect.y))
class Hero(GameSprite):
	def __init__(self,picture,width,height,x,y,speed):
		super().__init__(picture,width,height,x,y,speed)
	def update(self):
		keys = key.get_pressed()
		if keys[K_RIGHT] and self.rect.x + self.width <= win_width:
			self.rect.x += self.speed
		elif keys[K_LEFT] and self.rect.x >= 0:
			self.rect.x -= self.speed
	def fire(self):
		global bullets
		bullet = Bullet("bullet.png", 20, 20, rocket.rect.x+28, rocket.rect.y, 3)
		bullets.add(bullet)
class UFO(GameSprite):
	def __init__(self,picture,width,height,x,y,speed):
		super().__init__(picture,width,height,x,y,speed)
	def update(self):
		global miss
		self.rect.y += self.speed
		if self.rect.y >= win_height:
			miss += 1
			self.rect.y = 0
			self.rect.x = randint(0,win_width-self.width)
class Bullet(GameSprite):
	def __init__(self,picture,width,height,x,y,speed):
		super().__init__(picture,width,height,x,y,speed)		
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y <= 0:
			self.kill()



rocket = Hero("rocket.png", 75, 75, 300, 400, 5)
enemies = sprite.Group()
bullets = sprite.Group()
for i in range(5):
	ufo = UFO("ufo.png", 100, 60, randint(0, win_width-100), 0, randint(1,4))
	enemies.add(ufo)

game = 'in_process'
while True:	
	window.blit(back, (0,0))
	points_title = font.render('Счёт:'+str(points), True, (255,255,255))
	miss_title = font.render('Пропущено:'+str(miss), True, (255,255,255))
	window.blit(points_title, (10,10))
	window.blit(miss_title, (10,50))
	keys = key.get_pressed()
	rocket.reset()
	rocket.update()
	bullets.draw(window)
	bullets.update()
	enemies.draw(window)
	enemies.update()
	hits = sprite.groupcollide(bullets,enemies,True,True)
	for i in hits:
		ufo = UFO("ufo.png", 100, 60, randint(0, win_width-100), 0, randint(1,4))
		enemies.add(ufo)
		points += 1
	display.update()
	if sprite.spritecollideany(rocket,enemies):
		window.blit(lose, (300,200))
		display.update()
		game = 'lose'
		sleep(1)
	if points >= 10:
		game = 'win'
	if miss >= 10:
		game = 'fail' 
	elif game == 'win':
		window.blit(win, (300,200))
		display.update()
		sleep(1)
	elif game == 'fail':
		window.blit(lose, (300,200))
		display.update()
		sleep(1)
	
	for i in event.get():
		if i.type == QUIT:
			quit()
		if i.type == KEYDOWN:
			if i.key == K_DOWN and game == 'in_process':
				rocket.fire()
				fire.play()
			if i.key == K_SPACE and game != 'in_process':	
				points = 0
				miss = 0
				points_title = font.render('Счёт:'+str(points), True, (255,255,255)) 
				miss_title = font.render('Пропущено:'+str(miss), True, (255,255,255))
				enemies.empty()
				bullets.empty()
				rocket.rect.x = 300
				for i in range(5):
					ufo = UFO("ufo.png", 100, 60, randint(0, win_width-100), 0, randint(1,4))
					enemies.add(ufo)
				game = 'in_process'
	clock.tick(FPS)
#