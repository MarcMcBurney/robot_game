#Game title is "100 TO WIN!"
#You control a robot who can move left and right across the bottom of the screen
# Use left and right arrow keys to control robot
#Coins randomly rain down from the sky along with monsters
#Collect the coins and avoid the monsters. Coins are worth 1 point each
#The game speeds up the more coins you collect
# You start with 6 lives. If you hit a monster you lose a life. 
# You win the game by getting 100 points before losing all your lives


import pygame
import random

class Doordash:
    def __init__(self):
        pygame.init()
        self.load_images()
        self.game_setup()
        self.coins()
        self.monsters()
        self.main_loop()
        
    
    def game_setup(self):
        #Initialise game setup
        self.window = pygame.display.set_mode((640, 480))
        self.display = pygame.display.set_caption("100 TO WIN!")
        self.clock = pygame.time.Clock()
        #Initialise game fonts
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.points_text = self.game_font.render("Points: ", True, (255, 0, 0))
        self.lives_text = self.game_font.render("Lives: ", True, (255, 255, 255))
        # Initial robot Co-ordinates and boolean variables monotoring left and right keypress
        self.xr,self.yr = 0,0
        self.key_right = False
        self.key_left = False
        #set game speed, points, lives and boolean state indicating game is underway
        self.speed = 130
        self.points = 0
        self.final_points = 0
        self.lives = 6
        self.gameover = False
        self.coins_list = []
        self.monsters_list = []
        self.doorc = 10
        self.fifty = False
        self.game_won = False

    def game_over(self):
        #initialise game over state and blit game over text
        self.game_font2 = pygame.font.SysFont("Arial", 72)
        self.game_over_text = self.game_font2.render("GAME OVER!", True, (255, 255, 255))
        self.window.blit(self.game_over_text,self.game_over_text.get_rect(center = self.window.get_rect().center))
        self.lives = 0
        self.gameover = True
    
    def you_win(self):
        #Blit winning text
            self.game_font2 = pygame.font.SysFont("Arial", 72)
            self.you_win_text = self.game_font2.render("YOU WIN!", True, (255, 255, 255))
            self.window.blit(self.you_win_text,self.you_win_text.get_rect(center = self.window.get_rect().center))
            self.game_won = True
    def load_images(self):
        #load game images into list and assign variables
        self.images = []
        for name in ["coin", "door", "monster","robot"]:
            self.images.append(pygame.image.load(name + ".png"))
        self.robot = self.images[3]
        self.monster = self.images[2]
        self.door = self.images[1]
        self.coin = self.images[0]
        #create a Rect object for robot and co-ordinates to track
        self.robotrect = self.robot.get_rect()
        self.robotrect.x = 0
        self.robotrect.y = 480-self.robot.get_height()
    
    
            

    def coins(self):
        #create randomly spawning coin list
        
        while len(self.coins_list) < 10:
            self.new_coin()
            
          #replace coins as they dissappear ensuring no collisions         
    def new_coin(self):
            self.x = random.randint(0,640-self.coin.get_width())
            self.y = random.randint(-1500,-100)
            self.new_item_rect = pygame.Rect((self.x, self.y), (self.coin.get_width(), self.coin.get_height()))
            collides =  self.new_item_rect.collidelist(self.coins_list)
            if collides == -1: 
                self.coins_list.append(self.new_item_rect)
            else:
                self.new_coin()
    def monsters(self):
        #create randomly spawning monster list 
        while len(self.monsters_list) < 10:
            self.new_monster()
                       
   #replace monsters as they dissappear ensuring no collisions
    def new_monster(self):
            self.x = random.randint(0,640-self.monster.get_width())
            self.y = random.randint(-1500,-100)
            
            self.monsterRect = pygame.Rect((self.x, self.y), (self.monster.get_width(), self.monster.get_height()))
            collides =  self.monsterRect.collidelist(self.monsters_list)
            if collides == -1: 
                self.monsters_list.append(self.monsterRect)    
            else:
                self.new_monster()
    def main_loop(self):
        print (self.speed)
        while True:
            # when no lives left initiate game over method
            if self.lives <= 0:
                self.lives = 0
                self.game_over()
            # Game speeds up as points gained
            if  0 <= self.points  <= 20:
                self.speed = 150
                
            elif 20 <= self.points <= 40:
                self.speed = 170
                
            elif 40 <= self.points <= 60:
                self.speed = 190
                
            elif 60 <= self.points <= 80:
                self.speed = 220
                
            else:
                self.speed = 250
        
            # 100 points wins game
            if self.points == 100:
                self.you_win()

            for item in self.coins_list:
                # coins rain down
                self.window.blit(self.coin, (item[0], item[1]))
                item[1]+=1
                self.item_rect = pygame.Rect((item[0], item[1]), (self.coin.get_width(), self.coin.get_height()))
                #collect 1 point per coin
                if self.robotrect.colliderect(self.item_rect) and self.game_won == False:
                    if self.gameover == False:
                        self.points += 1
                    self.coins_list.remove(item)
                    self.new_coin()
                    # remove coin and create new randomly positioned coin
                if item[1] >= 480:
                    self.coins_list.remove(item)
                    self.new_coin()    
                    
            for item in self.monsters_list:
                self.window.blit(self.monster, (item[0], item[1]))
                self.monsterRect = pygame.Rect((item[0], item[1]), (self.monster.get_width(), self.monster.get_height()))
                collides =  self.monsterRect.collidelist(self.coins_list)
                #stop monsters spawning over coins
                if collides != -1:
                    self.monsters_list.remove(item)
                    self.new_monster()
                item[1]+=1
                #respawn monsters after they hit the bottom
                if item[1] >= 480:
                    self.monsters_list.remove(item)
                    self.new_monster()
                if self.robotrect.colliderect(self.monsterRect) and self.game_won == False:
                    self.lives -= 1
                    #lose a life if collide with monster and spawn new one
                    #screen flashes red as life lost
                    self.window.fill((255, 0, 0))
                    self.monsters_list.remove(item)
                    self.new_monster()
            self.check_events()
            self.draw_window()
            self.clock.tick(self.speed)
            #self.coins()
            
             
    def check_events(self):
        #move robot
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.key_left = True
                if event.key == pygame.K_RIGHT:
                    self.key_right = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.key_left = False
                if event.key == pygame.K_RIGHT:
                    self.key_right = False

        if self.key_left:
            self.xr -= 3
            self.robotrect.x = self.xr
            if self.xr <= 0:
                self.xr = 0
        if self.key_right:
            self.xr += 3
            self.robotrect.x = self.xr
            if self.xr >= 640 - (self.robot.get_width()):
                self.xr = 640 - (self.robot.get_width())

                
    def draw_window(self):
        #draw display
        pygame.display.flip()
        self.score_tally = self.game_font.render(str(self.points), True, (255,0,0))
        self.lives_tally = self.game_font.render(str(self.lives), True, (255,255,255))
        self.final_points = self.game_font.render(str(self.final_points), True, (255,255,255))
        self.window.fill((0, 0, 255))
        self.window.blit(self.points_text, (510, 0))
        self.window.blit(self.score_tally, (590, 0))
        self.window.blit(self.lives_text, (10, 0))
        self.window.blit(self.lives_tally, (80, 0))
        self.window.blit(self.robot, (self.xr, (480-self.yr-self.robot.get_height())))
        
if __name__ == "__main__":
    Doordash()