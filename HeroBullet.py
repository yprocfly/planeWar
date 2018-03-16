import pygame


# 子弹对象
class HeroBullet(pygame.sprite.Sprite):
    def __init__(self, screen, position, image = "./images/bullet_9.png"):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.image = pygame.image.load(image).convert_alpha()
        # 初始位置
        self.rect = self.image.get_rect()
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.active = True
        self.speed = 12

    # 显示子弹
    def display(self):
        self.screen.blit(self.image, (self.rect.left, self.rect.top))

    # 移动子弹
    def move(self, position):
        if self.rect.top > 5:
           self.rect.top -= self.speed
        else:
            self.reset(position)

    # 重置子弹
    def reset(self, position):
        self.rect.left = position[0] - self.rect.width // 2
        self.rect.top = position[1] - self.rect.height
        self.active = True
