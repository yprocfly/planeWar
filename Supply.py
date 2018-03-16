import pygame, random

# 超级炸弹
class SupplySuperBullet(pygame.sprite.Sprite):
	
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)

		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.image = pygame.image.load("./images/buji.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.top = random.randint(-60, -50)
		self.rect.left = random.randint(0, self.screen_rect.width - self.rect.width)
		self.speed = 1

	def display(self):
		self.screen.blit(self.image, self.rect)
		if self.rect.top > self.screen_rect.height:
			self.reset()

	def move(self):
		if self.rect.top < self.screen_rect.height // 3:
			self.rect.top += (self.speed * 10)
		else:
			self.rect.top += self.speed

	def reset(self):
		self.rect.top = random.randint(-60, -50)
		self.rect.left = random.randint(0, self.screen_rect.width - self.rect.width)


# 双重子弹
class SupplyDoubleBullet(pygame.sprite.Sprite):
	
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)

		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.image = pygame.image.load("./images/buji2.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.top = random.randint(-60, -50)
		self.rect.left = random.randint(0, self.screen_rect.width - self.rect.width)
		self.speed = 1
		
	def display(self):
		self.screen.blit(self.image, self.rect)
		if self.rect.top > self.screen_rect.height:
			self.reset()

	def move(self):
		if self.rect.top < self.screen_rect.height // 3:
			self.rect.top += (self.speed * 10)
		else:
			self.rect.top += self.speed

	def reset(self):
		self.rect.top = random.randint(-60, -50)
		self.rect.left = random.randint(0, self.screen_rect.width - self.rect.width)
