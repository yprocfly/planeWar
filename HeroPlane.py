import pygame, sys
from pygame.locals import *


# 创建主角飞机类
class HeroPlane(pygame.sprite.Sprite):

    def __init__(self, screen, image = "./images/hero.png"):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.image = pygame.image.load(image).convert_alpha()
        # 飞机初始位置
        self.rect = self.image.get_rect()
        self.rect.top = screen.get_height() - self.rect.height - 50
        self.rect.left = (screen.get_width() - self.rect.width) // 2
        self.speed = 10   # 移动速度
        self.pause = False  # 判断是否暂停游戏
        self.distory = [\
            pygame.image.load("./images/image 1.png").convert_alpha(),\
            pygame.image.load("./images/image 2.png").convert_alpha(),\
            pygame.image.load("./images/image 3.png").convert_alpha(),\
            pygame.image.load("./images/image 4.png").convert_alpha(),\
            pygame.image.load("./images/image 5.png").convert_alpha(),\
            pygame.image.load("./images/image 6.png").convert_alpha(),\
            pygame.image.load("./images/image 7.png").convert_alpha(),\
            pygame.image.load("./images/image 8.png").convert_alpha(),\
            pygame.image.load("./images/image 9.png").convert_alpha(),\
            pygame.image.load("./images/image 10.png").convert_alpha(),\
            pygame.image.load("./images/image 11.png").convert_alpha(),\
            pygame.image.load("./images/image 12.png").convert_alpha(),\
            pygame.image.load("./images/image 13.png").convert_alpha(),\
            pygame.image.load("./images/image 14.png").convert_alpha()\
            ]
        self.active = True

    # 显示主飞机图片
    def display(self):
        self.screen.blit(self.image, self.rect)

    # 左
    def moveLeft(self):
        if self.rect.left >= self.speed:
            self.rect.left -= self.speed

    # 右
    def moveRight(self):
        right = self.screen.get_width() - self.rect.width - 10
        if self.rect.left <= right:
            self.rect.left += self.speed

    # 上
    def moveUp(self):
        if self.rect.top >= self.speed:
            self.rect.top -= self.speed

    # 下
    def moveDown(self):
        down = self.screen.get_height() - self.rect.height - 10
        if self.rect.top <= down:
            self.rect.top += self.speed

    # 控制飞机
    def ctrlPlane(self):
        # 检测键盘状态
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] or pressed[K_a]:
            self.moveLeft()
        elif pressed[K_RIGHT] or pressed[K_d]:
            self.moveRight()
        elif pressed[K_UP] or pressed[K_w]:
            self.moveUp()
        elif pressed[K_DOWN] or pressed[K_s]:
            self.moveDown()
                