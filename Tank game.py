'''
1 游戏引擎pygame 安装
2明白需求：（基于对于面向对象的分析）
        1有哪些类：
           a.主逻辑类:开始游戏 结束游戏
           b.坦克类（1.我方坦克 2.敌方坦克）：移动 射击
           c.子弹类：展示子弹  移动
           d.爆炸效果类：展示爆炸效果
           e.墙壁类：（类属性）是否可以通过
           g.音效类：播放音乐
3游戏框架搭建
涉及到的类用代码简单实现

V1.03
     新增功能
     创建游戏窗口
     用到游戏引擎中的功能模块
     官方开发文档www.pygame.org/docs
V1.04
     新增功能：
     事件处理：点击关闭按钮退出程序的事件
              方向控制，子弹发射
v1.05
     新增功能：
             实现左上角文字提示
              font
V1.06 新增功能：
              加载我方坦克
v1.07
     新增功能：
        1.坦克类新增speed属性，用来控制坦克移动快慢
        2.事件处理：
               2.1 改变坦克方向
              2.2 修改坦克位置（left,top)
                  取决于坦克速度
v1.08
    优化功能：
    1.BUG:坦克可以移除边界
    2优化坦克移动方式 ，按下方向键持续移动，松开方向键 坦克停止
V1.10
    新增敌方坦克：
         1 完善敌方坦克类
         2 创建敌方坦克，将敌方坦克展示到窗口中

'''
import pygame,random,time
_display=pygame.display
version="1.03"
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255,0,0)
class MainGame():
    #游戏主窗口
    window=None
    SCREEN_WIDTH=800
    SCREEN_HEIGHT=800
    #创建我方坦克
    TANK_P1=None
    #储存所有敌方坦克
    EnemyTank_list = []
    #要创建的敌方坦克数量
    EnemyTank_count = 5
    def __init__(self):
        pass
    #开始游戏方法
    def startGame(self):
        #初始化显示模块
        _display.init()
        #创建窗口加载窗口以进行屏幕显示(借鉴官方文档)
        MainGame.window=_display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        #创建我方坦克
        MainGame.TANK_P1=Tank(500,500)
        self.creatEnemyTank()
        #设置游戏标题2
        _display.set_caption("坦克大战"+version)
        #让窗口持续刷新操作
        while True:
            #给窗口完成一个填充颜色Color(r,g,b,a)->Color
            MainGame.window.fill(COLOR_BLACK)
            #在循环中持续完成事件的获取
            self.getEvent()
            #将文字得到的小画布，粘到窗口中  将图像绘制到另一个
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆"%5),(5,5))
            #将我方坦克加入到窗口中
            MainGame.TANK_P1.displayTank()
            #根据坦克的开关状态调用用坦克的方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
            time.sleep(0.02)
            _display.update()
            #循环展示敌方坦克
            self.blitEnemyTank()

    #获取程序期间所有时间（鼠标事件，键盘事件）
    #创建敌方坦克
    def creatEnemyTank(self):
        left = random.randint(1,5)
        top=100
        speed=random.randint(3,6)
        for i in range(MainGame.EnemyTank_count):
            eTank=EnemyTank(left*100,top,speed)
            MainGame.EnemyTank_list.append(eTank)
    #将坦克加入窗口中
    def blitEnemyTank(self):
         for eTank in MainGame.EnemyTank_list:
                    eTank.displayTank()
            #根据坦克的开关状态 调用坦克移动的方法
         if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                #窗口的刷新
                _display.update()
    def getEvent(self):
        #1.获取所有事件
        eventList=pygame.event.get()
        #2.对事件进行判断处理（1、点击关闭按钮 2、按下键盘上的某个按键
        for event in eventList:
            #判断event.type是否QUIT，如果是退出直接调用程序结束方法
            if event.type==pygame.QUIT:
                self.endGame()
            #判断事件类型是否为按键下，如果是,继续判断案件是哪一个按键，进行相应的处理
            if event.type==pygame.KEYDOWN:
                #具体是哪个按键的处理：
                if event.key==pygame.K_LEFT:
                    print("坦克向左掉头，移动")
                    #修改坦克方向
                    MainGame.TANK_P1.direction='L'
                    MainGame.TANK_P1.stop=False
                    #完成移动操作
                    #MainGame.TANK_P1.move()
                elif event.key == pygame.K_RIGHT:
                    print("坦克向右掉头，移动")
                    MainGame.TANK_P1.direction = 'R'
                    MainGame.TANK_P1.stop = False
                # MainGame.TANK_P1.move()
                elif event.key == pygame.K_UP:
                    print("坦克向上掉头，移动")
                    MainGame.TANK_P1.direction = 'U'
                    MainGame.TANK_P1.stop = False
                   # MainGame.TANK_P1.move()
                elif event.key == pygame.K_DOWN:
                    print("坦克向下掉头，移动")
                    MainGame.TANK_P1.direction = 'D'
                    MainGame.TANK_P1.stop = False
                   # MainGame.TANK_P1.move()
                elif event.key==pygame.K_SPACE:
                    print("发射子弹")
            elif event.type==pygame.KEYUP:
                #松开的如果是方向键，才更改移动状态
                MainGame.TANK_P1.stop=True
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    #修改坦克移动状态
                    MainGame.TANK_P1.Stop=True
    #左上角文字绘制的功能
    def getTextSurface(self,text):
        #初始化字体模块
         pygame.font.init()
        #选中一个合适的字体  查看系统可用的字体 ：fontList=pygame.font.get.fonts()
         font=pygame.font.SysFont("kaiti",18)
        #使用字符完成相应内容的绘制   在新Surface 上绘制文本 pygame.font.render(文本,抗锯齿,颜色,背景=无)
         textSurface=font.render(text,True,COLOR_RED)
         return textSurface
    #结束游戏方法
    def endGame(self):
        print("游戏结束了")
        #结束python解释器
        exit()
class Tank():
    def __init__(self,left,top):
        self.images={
        'D':pygame.image.load('img/p1tankD.gif'),
        'U': pygame.image.load('img/p1tankU.gif'),
        'R': pygame.image.load('img/p1tankR.gif'),
        'L': pygame.image.load('img/p1tankL.gif')
        }
        self.direction='U'
        self.image=self.images[self.direction]
        #坦克所在的区域 Rect->
        self.rect=self.image.get_rect()
        #制定坦克初始化位置 分别距X ,Y的位置。
        self.rect.left=left
        self.rect.top=top
        #新增速度属性
        self.speed = 1
        #新增属性：坦克的移动开始暂停
        self.stop=True
    #坦克的移动方法
    def move(self):
        if self.direction=='L':
            if self.rect.left > 0:
              self.rect.left-=self.speed
        elif self.direction == 'R':
            if self.rect.left+self.rect.height<MainGame.SCREEN_WIDTH:
             self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top>0:
             self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top+self.rect.height<MainGame.SCREEN_HEIGHT:
             self.rect.top += self.speed
    #射击方法
    def shoot(self):
        pass
    #展示坦克（将坦克这个surface绘制到窗口中 blit())
    def displayTank(self):
        #1 重新设置坦克图片
        self.image=self.images[self.direction]
        #2 将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)
class MyTank():
    def __init__(self):
        pass
class EnemyTank():
    def __init__(self,left,top,speed):
        #图片  方向   位置区域  速度  rect  live 是否活着
        self.images = {
            'D': pygame.image.load('img/enemy1D.gif'),
            'U': pygame.image.load('img/enemy1U.gif'),
            'R': pygame.image.load('img/enemy1R.gif'),
            'L': pygame.image.load('img/enemy1L.gif')
        }
        self.direction =self.randDirection()
        self.image = self.images[self.direction]
        # 坦克所在的区域 Rect->
        self.rect = self.image.get_rect()
        # 制定坦克初始化位置 分别距X ,Y的位置。
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        # 新增属性：坦克的移动开始暂停
        self.stop = True
    def randDirection(self):
        num=random.randint(1,4)
        if num==1:
            self.direction='D'
        if num==2:
            self.direction='U'
        if num==3:
            self.direction='L'
        if num==4:
            self.direction='R'
    # def displayEnemTank(self):
    #    super().displayTank()
class Bullet():
    def __init__(self):
        pass
    #子弹的移动方法
    def move(self):
        pass
    #展示子弹的方法
    def displayBullet(self):
        pass
class Explode():
    def __init__(self):
        pass
    #展示爆炸效果
    def playExplode(self):
        pass
class Wall():
    def __init__(self):
        pass
    #展示墙壁的方法
    def displayWall(self):
        pass
class Music():
    def __init__(self):
        pass
    #开始播放音乐
    def displayMusic(self):
        pass
MainGame().startGame()