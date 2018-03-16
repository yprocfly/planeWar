# encoding=utf-8
import pygame, game, random

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 600))
    # 加载背景图片
    bg = pygame.image.load("./images/img_bg_level_%d.jpg" % random.randint(1, 5)).convert()

    # 设置窗口图标和标题
    icon = pygame.image.load("./images/game.ico").convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption("飞机大战")

    clock = pygame.time.Clock()

    my_game = game.Game(screen)

    while True:
        # 显示背景
        screen.blit(bg, (0, 0))
        
        my_game.ctrlGame()
        if my_game.is_index:
            my_game.showIndex()
        else:
            my_game.showScore()
            if my_game.is_game_over:
                my_game.showGameOver()
            else:
                # 暂停游戏
                if not my_game.is_pause:
                    my_game.showHero()
                    my_game.showSupply()
                    my_game.showSuperNum()
                    my_game.upLevel()
                    my_game.showEnemys()
                    # 子弹
                    my_game.showDoubleBullets() if my_game.is_double_bullet else my_game.showBullets()
                    my_game.overGame()

        # 更新画面
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()



