import pygame, random


# 创建敌机类
class EnemyPlane(pygame.sprite.Sprite):

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.image = pygame.image.load("./images/img-plane_%d.png" % random.randint(1, 7)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.screen.get_width() - self.image.get_width())
        self.rect.top = random.randint(-3 * self.screen.get_height(), 0)
        self.speed = 3
        self.active = True
        self.distory = [\
            pygame.image.load("./images/bomb-1.png").convert_alpha(),\
            pygame.image.load("./images/bomb-2.png").convert_alpha(),\
            pygame.image.load("./images/bomb-3.png").convert_alpha(),\
            pygame.image.load("./images/bomb-4.png").convert_alpha(),\
            pygame.image.load("./images/bomb-5.png").convert_alpha(),\
            pygame.image.load("./images/bomb-6.png").convert_alpha()\
            ]

    def display(self):
        self.screen.blit(self.image, (self.rect.left, self.rect.top))

    def move(self):
        if self.rect.top <= self.screen.get_height():
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left = random.randint(0, self.screen.get_width() - self.image.get_width())
        self.rect.top = random.randint(-5 * self.screen.get_height(), 0)
