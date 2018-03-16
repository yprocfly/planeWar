import time, pygame, random
from pygame.locals import *
from HeroPlane import *
from EnemyPlane import *
from HeroBullet import *
from Supply import *


class Game(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bullets = []  # 子弹
        self.double_bullets = []    # 双重子弹
        self.is_double_bullet = False
        self.bullet_index = 0  # 子弹索引
        self.enemys = pygame.sprite.Group()  # 敌机精灵组
        self.e_image_index = 0  # 敌机炸毁图片索引
        self.h_image_index = 0  # 我方飞机炸毁图片索引
        self.hero = HeroPlane(screen)  # 生成我方飞机
        self.score = 0  # 分数
        self.level = 1  # 难度级别（随着分数越来越高，难度越来越大，1-5级难度依次递升）
        self.is_pause = False  # 是否暂停
        self.delay = 1800    # 用于延迟
        self.is_game_over = False   # 判断游戏是否结束
        self.is_index = True    # 判断是否在游戏首页
        self.is_supply_super = random.choice([True, False])
        self.supply_super = SupplySuperBullet(screen)   # 超级炸弹补给
        self.supply_double = SupplyDoubleBullet(screen)   # 双重炸弹补给
        self.is_supply = False  # 是否提供补给
        self.super_bullet = pygame.image.load("./images/bullet_14.png").convert_alpha()    # 超级炸弹
        self.super_num = 3      # 超级炸弹剩余数量

        self.createEnemys(20)   # 生成敌机
        self.createBullets(5)   # 生成子弹

        # 加载字体
        self.big_font = pygame.font.Font("./images/simhei.ttf", 26)
        self.small_font = pygame.font.Font("./images/simhei.ttf", 14)
        self.white = (255, 255, 255)    # 白色字体

        # 加载背景音乐
        pygame.mixer.init()
        pygame.mixer.music.load("./images/bg.wav")
        pygame.mixer.music.set_volume(0.1)

        # 加载音效
        self.zidan = pygame.mixer.Sound("./images/bullet.wav")
        self.zidan.set_volume(0.1)
        self.bomb = pygame.mixer.Sound("./images/bomb.wav")
        self.bomb.set_volume(0.1)
        self.bigbomb = pygame.mixer.Sound("./images/bigbomb.wav")
        self.bigbomb.set_volume(0.1)
        self.gameover = pygame.mixer.Sound("./images/gameover.wav")
        self.gameover.set_volume(0.1)

    def showScore(self):
        """显示分数"""
        score_text = self.big_font.render("分数：%d" % self.score, True, self.white)
        self.screen.blit(score_text, (10, 5))

    def createEnemys(self, num = 20):
        """
        添加敌机
        num   需要生成的敌机数量
        """
        for i in range(num):
            self.enemys.add(EnemyPlane(self.screen))

    def createBullets(self, num = 5):
        """
        生成子弹
        num   需要生成的子弹数量
        """
        for i in range(num):
            self.bullets.append(HeroBullet(self.screen, self.hero.rect.midtop))
            self.double_bullets.append(HeroBullet(self.screen, (self.hero.rect.midtop[0] - 40, self.hero.rect.midtop[1] + 5)))
            self.double_bullets.append(HeroBullet(self.screen, (self.hero.rect.midtop[0] + 40, self.hero.rect.midtop[1] + 5)))

    def showHero(self):
        """显示我方飞机"""
        if self.hero.active:
            self.hero.display()
            self.hero.ctrlPlane()

            # 延时控制
            self.delay -= 1
            if not self.delay:
                self.is_supply = True
                self.is_supply_super = random.choice([True, False])
                self.delay = 1800
            if self.delay == 300:
                self.is_double_bullet = False
                self.bullet_index = 0
        else:
            # 我方飞机阵亡
            self.screen.blit(self.hero.distory[self.h_image_index], self.hero.rect)
            self.h_image_index = (self.h_image_index + 1) % len(self.hero.distory)
            if self.h_image_index == 0:
                self.gameover.play()
                self.is_game_over = True


    def showEnemys(self):
        """显示敌机"""
        for enemy in self.enemys:
            if enemy.active:
                enemy.display()
                enemy.move()
            else:
                # 敌机爆炸效果
                self.screen.blit(enemy.distory[self.e_image_index], enemy.rect)
                self.e_image_index = (self.e_image_index + 1) % len(enemy.distory)
                if self.e_image_index == 0:
                    enemy.reset()

    def showBullets(self):
        """显示子弹"""
        for bullet in self.bullets:
            if bullet.active:
                bullet.display()
                bullet.move(self.hero.rect.midtop)
                # 检测碰撞（collide_mask参数可忽略 png 图片的透明背景部分，实现完美碰撞检测）
                enemy_hit = pygame.sprite.spritecollide(bullet, self.enemys, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    bullet.reset(self.hero.rect.midtop)
                    for e in enemy_hit:
                        self.score += (1000 * self.level)
                        # 播放爆炸音效
                        self.bomb.play()
                        e.active = False
        # 每运行10帧，重置一次子弹，可实现无限子弹效果
        if self.delay % 10 == 0:
            self.zidan.play()
            self.bullets[self.bullet_index].reset(self.hero.rect.midtop)
            self.bullet_index = (self.bullet_index + 1) % len(self.bullets)

    def showDoubleBullets(self):
        """显示双重子弹"""
        i = 0
        pos1 = (self.hero.rect.midtop[0] - 40, self.hero.rect.midtop[1] + 5)
        pos2 = (self.hero.rect.midtop[0] + 40, self.hero.rect.midtop[1] + 5)
        for bullet in self.double_bullets:
            pos = pos1 if i % 2 == 0 else pos2
            if bullet.active:
                bullet.display()
                bullet.move(pos)
                # 检测碰撞（collide_mask参数可忽略 png 图片的透明背景部分，实现完美碰撞检测）
                enemy_hit = pygame.sprite.spritecollide(bullet, self.enemys, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    bullet.reset(pos)
                    for e in enemy_hit:
                        self.score += (1000 * self.level)
                        # 播放爆炸音效
                        self.bomb.play()
                        e.active = False
            i = (i + 1) % len(self.double_bullets)

        # 每运行10帧，重置一次子弹，可实现无限子弹效果
        if self.delay % 10 == 0:
            self.zidan.play()
            self.double_bullets[self.bullet_index].reset(pos1)
            self.double_bullets[self.bullet_index + 1].reset(pos2)
            self.bullet_index = (self.bullet_index + 2) % len(self.double_bullets)

    def ctrlGame(self):
        """控制游戏（暂停、退出）"""
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            # 点击键盘按钮
            if event.type == KEYDOWN:
                # 暂停游戏
                if event.key == K_SPACE:
                    self.is_pause = not self.is_pause
                    pygame.mixer.music.pause() if self.is_pause else pygame.mixer.music.unpause()
                # 开始游戏
                if event.key == K_RETURN:
                    if self.is_game_over:
                        self.__init__(self.screen)
                    self.is_index = False
                    pygame.mixer.music.play(-1) 
                # 发射超级炸弹
                if event.key == K_j or event.key == K_KP1:
                    self.shootSuperBullet()
                # 回到首页
                if self.is_game_over and event.key == K_TAB:
                    self.is_index = True
                # 退出游戏
                if self.is_index and event.key == K_ESCAPE:
                    sys.exit()

    def overGame(self):
        """我方飞机触碰到敌机，游戏结束"""
        hero_hit = pygame.sprite.spritecollide(self.hero, self.enemys, False, pygame.sprite.collide_mask)
        if hero_hit:
            pygame.mixer.music.stop()
            self.hero.active = False

    def showGameOver(self):
        """显示游戏结束"""
        over_text = self.big_font.render("GAME OVER", True, self.white)
        pos = (self.screen_rect.width - over_text.get_width()) // 2, (self.screen_rect.height - over_text.get_height()) // 2
        self.screen.blit(over_text, pos)
        tips_text = self.small_font.render("按 Tab 返回主页，按 Enter 重新开始", True, self.white)
        pos = (self.screen_rect.width - tips_text.get_width()) // 2, pos[1] + over_text.get_height() + 10
        self.screen.blit(tips_text, pos)

    def showIndex(self):
        """显示首页"""
        tips_text = self.small_font.render("按 Esc 退出游戏，按 Enter 开始游戏", True, self.white)
        pos = (self.screen_rect.width - tips_text.get_width()) // 2, (self.screen_rect.height + tips_text.get_height()) // 2
        self.screen.blit(tips_text, pos)
        ctrl_text = self.small_font.render("左[A ←]右[D →]上[W ↑]下[S ↓] 全屏炸弹[J 1] 暂停[空格]", True, self.white)
        pos = (self.screen_rect.width - ctrl_text.get_width()) // 2, pos[1] + tips_text.get_height() + 10
        self.screen.blit(ctrl_text, pos)

    def upSpeed(self):
        """提升所有敌机的速度"""
        for enemy in self.enemys:
            enemy.speed += 1

    def upLevel(self):
        """提升级别"""
        if self.level == 1 and self.score >= 50000:
            self.level = 2
            self.createEnemys(3)
            self.upSpeed()
        elif self.level == 2 and self.score >= 300000:
            self.level = 3
            self.createEnemys(5)
            self.upSpeed()
        elif self.level == 3 and self.score >= 1000000:
            self.level = 4
            self.createEnemys(8)
            self.upSpeed()
        elif self.level == 4 and self.score >= 3000000:
            self.level = 5
            self.createEnemys(10)
            self.upSpeed()

    def showSupply(self):
        """补给 超级炸弹和双重子弹"""
        supply = self.supply_super if self.is_supply_super else self.supply_double
        supply.display()
        if self.is_supply:
            supply.move()
            if supply.rect.top > self.screen_rect.height:
                self.is_supply = False
            if pygame.sprite.collide_rect(self.hero, supply):
                supply.reset()
                self.is_supply = False
                if self.is_supply_super:
                    self.super_num += 1
                else:
                    # 双重子弹补给
                    self.is_double_bullet = True
                    self.bullet_index = 0
        

    def shootSuperBullet(self):
        """发射超级炸弹"""
        if self.super_num >= 1:
            for enemy in self.enemys:
                if enemy.rect.top > -300:
                    self.bomb.play()
                    self.score += (1000 * self.level)
                    enemy.active = False
            self.super_num -= 1

    def showSuperNum(self):
        """显示超级炸弹剩余数量"""
        rect = self.super_bullet.get_rect()
        rect.left, rect.top = 10, 40
        self.screen.blit(self.super_bullet, rect)
        super_text = self.small_font.render("×%d" % self.super_num, True, self.white)
        self.screen.blit(super_text, rect.midright)

    