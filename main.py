import pygame 
import os
import math 
import random 
pygame.init() 

clock = pygame.time.Clock()
winx, winy = 1200 , 700
canvas = pygame.display.set_mode((winx,winy))
pygame.display.set_caption("WW2 Simulated : London Bombing ")



#Image list 

nazi1 = pygame.image.load(os.path.join('assets','nazi1.png'))
nazi2 = pygame.image.load(os.path.join('assets','nazi2.png'))
nazi3 = pygame.image.load(os.path.join('assets','nazi3.png'))
bullety = pygame.transform.scale(pygame.image.load(os.path.join('assets','bullet1.png')), (40,10))
bulleto = pygame.transform.scale(pygame.image.load(os.path.join('assets','bullet2.png')), (40,10))
playership = pygame.transform.scale(pygame.image.load(os.path.join('assets','Shooter.png')),(200,100))

#convert moving background





#Tick Coutner for Refresh/update rate
fps = 60
#backgroud image import
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets','background.jpg')),(winx,winy)).convert()
#These Classes Help create blueprints of game elements : Shoot is blueprints for bullets and how they act , Ship is the 
# blueprint of both player ship and enemies ship movement and shooting action and the player 
# and enemie classes are for masking the images and specific actions of each.
class Shoot: 
    def __init__(self,x , y ,img): 
        self.x = x + 175
        self.y = y + 50
        self.img = img 
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,window): 
        window.blit(self.img, (self.x ,self.y))
    def move(self, vel): 
        self.x += vel
    def off_screen(self, width): 
        return self.x >= width or self.x <= 0
    def impaction(self,obj):
        return impact(self,obj)
   
class Ship: 
    COOLDOWN = 10
    def __init__(self,x,y,hp = 100): 
        self.x = x 
        self.y = y
        self.hp = hp 
        self.ship_img = None  
        self.bull_img = None 
        self.bullets = []
        self.cool_down = 0 
    def draw(self, window): 
        window.blit(self.ship_img, (self.x , self.y))
        for bullet in self.bullets: 
            bullet.draw(window)
    def bullmove(self,vel,obj): 
        self.cooldown() 
        for bullet in self.bullets: 
            bullet.move(vel)
            if bullet.off_screen(winx): 
                self.bullets.remove(bullet)
            elif bullet.impaction(obj): 
                obj.hp -= 10 
                self.bullets.remove(bullet)
    def cooldown(self): 
        if self.cool_down >= self.COOLDOWN: 
            self.cool_down = 0 
        elif self.cool_down > 0:
            self.cool_down +=1
    def fire(self): 
        if self.cool_down == 0 :
            bullet = Shoot(self.x,self.y,self.bull_img)
            self.bullets.append(bullet)
            self.cool_down = 1 
    def get_width(self): 
        return self.ship_img.get_width() 
    def get_height(self): 
        return self.ship_img.get_height() 
        
class Player(Ship): 
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.ship_img = playership 
        self.bull_img = bullety
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_hp = hp 
    def bullmove(self,vel,objs): 
        self.cooldown() 
        for bullet in self.bullets: 
            bullet.move(vel)
            if bullet.off_screen(winx): 
                self.bullets.remove(bullet)
            else:  
                for obj in objs : 
                    if bullet.impaction(obj): 
                        objs.remove(obj)
                        if bullet in self.bullets: 
                            self.bullets.remove(bullet)
    def draw(self, window): 
        super().draw(window)
        self.hpbar(window)
    def hpbar(self, window): 
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.hp/self.max_hp), 10))
class Enemy(Ship):
    nazi_ship_list = { 
        "enem1" : (nazi1,bulleto),
        "enem2" : (nazi2,bulleto),
        "enem3" : (nazi3,bulleto)
    }
    def __init__(self, x, y, nazis , hp=100):
        super().__init__(x, y, hp)
        self.ship_img , self.bull_img = self.nazi_ship_list[nazis]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,enemyvel): 
        self.x += enemyvel
    def fire(self): 
        if self.cool_down == 0 : 
            bullet = Shoot(self.x-20, self.y,self.bull_img)
            self.bullets.append(bullet)
            self.cool_down = 1 
    def collide(obj1,obj2): 
        offset_x = obj2.x - obj1 
        offset_y = obj2.y - obj1.y 
        return obj1.mask.overlap(obj2.mask , (offset_x , offset_y)) != None
#This defines the collision of ships between player and enemies , main function detects impacting pixels
def impact(obj1 , obj2): 
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y 
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))
#This is the main function which contain details , variables , text , and more.
def main(): 
    
    scroll = 0
    tiles = math.ceil(winx/bg.get_width())+ 1
    run = True
    lives = 5 
    waves = 0
    main_font = pygame.font.SysFont("times_new_roman" , 50)
    gameover_font = pygame.font.SysFont("impact" , 100)
    gameover_font2 = pygame.font.SysFont("impact" , 50)
    player = Player(150,100)
    gameover = False
    gameovernum = 0 
    enemies = []
    wavetime = 5
    enemyvel = -2
    bullete_vel = -5
    bullete2_vel = -5
    #This function here is for representing what each time the screen needs to update. Also contains numerous text  + 
    # functions which is contained to be able to be updated aswell 
    def update_win():
        livestxt= main_font.render(f"Lives: {lives}" , 1 , ( 0 , 0 , 0))
        wavestxt = main_font.render(f"Wave: {waves}" , 1 , ( 0 , 0 , 0))
        canvas.blit(livestxt, (10,10))
        canvas.blit(wavestxt , (winx - 180 , 10) )
        for enemy in enemies: 
                enemy.draw(canvas)
        if gameover: 
                gameovertxt = gameover_font.render("GAMEOVER" , 1 , (255,0,0))
                gameovertxt2 = gameover_font2.render("Game Will Close Shortly" , 1 , (255,0,0))
                canvas.blit(gameovertxt, (winx/2 - gameovertxt.get_width()/2,winy / 2 - gameovertxt.get_height()/2  ))
                canvas.blit(gameovertxt2, (winx/2 - gameovertxt2.get_width()/2,(winy / 2 - gameovertxt2.get_height()/2) + 70  ))
        player.draw(canvas)
        pygame.display.update() 
    #This while function is ment ro run the screen objects and the whole game functions in a loop unless its closed. 
    while run == True:
        clock.tick(fps)
        update_win()
        #This if fuction is ment for if the player looses its life or lives to the enemies and is summoning
        #  the gameover text created in the updated function
        if lives  <= 0 or player.hp <= 0: 
            gameover = True 
            gameovernum += 1
        if gameover:  
            if gameovernum > fps * 5 : 
                run = False
            else: 
                continue
        #This if function represents when each wave is completed the enemies get faster and grow in numbers which makes the game challenging
        if len(enemies) == 0 : 
            waves +=1
            wavetime += 2
            enemyvel += -0.3
            bullete2_vel += -0.5
            for i in range(wavetime): 
                enemy = Enemy(random.randrange(1600,4000),random.randrange(95, 540),random.choice(["enem1","enem2","enem3"]))
                enemies.append(enemy)
        #This function is ment for the moving background in the screen/canvas to make it look like the player is flying through a city
        i = 0
        while(i < tiles):
            canvas.blit(bg, (bg.get_width()*i
                            + scroll, 0))
            i += 1
        scroll -= 8
        if abs(scroll) > bg.get_width():
            scroll = 0

        #These if statements represents keylisteners that allow the player to move in specific areas  and shoot with specific buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys_pressed = pygame.key.get_pressed() 
        55


        if keys_pressed[pygame.K_UP] : 
            if player.y >=95 :  
                player.y -= 5.8                    
        if keys_pressed[pygame.K_DOWN] : 
            if player.y <= 550 :  
                player.y += 6.4
        if keys_pressed[pygame.K_SPACE] : 
            player.fire()
        #This function represents the enemie's main functions like colission velocity , bullet velocity and more , and how to to reduce the players life when impact. 
        for enemy in enemies[:]: 
            enemy.move(enemyvel)
            enemy.bullmove(bullete2_vel,player)
            if random.randrange(0,2*60) == 1 : 
                enemy.fire() 
            if impact(enemy, player): 
                player.hp -=10 
                enemies.remove(enemy)
            elif enemy.x + enemy.get_width() < 100 : 
                lives -= 1 
                enemies.remove(enemy)
        player.bullmove(-bullete_vel,enemies)

        update_win()
    pygame.quit()

main() 




