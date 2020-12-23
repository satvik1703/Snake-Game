# Importing the Pygame Module
import pygame
#initialising all modules of pygame
pygame.init()
#for exiting the system
import sys
#for generating randomness
import random
import os

#creating windows
game_window_width=800
game_window_height=500
game_window=pygame.display.set_mode((game_window_width,game_window_height))
#adding title
pygame.display.set_caption("Game by-S@tvik")

FPS=30 #frames per second
clock=pygame.time.Clock() # time k according frames ko change krna padta haii

#for music
pygame.mixer.init()

#defining colors
WHITE=(255,255,255)
RED=(255,0,0)
BLACK=(0,0,0)
BLUE=(0,0,255)
YELLOW=(0,255,10)

background=pygame.image.load("D:\\snake_game\\Game_Sprites\\Back.jpg")
background=pygame.transform.scale(background,(game_window_width,game_window_height)).convert_alpha()


#font
font=pygame.font.SysFont("Helvetica",40)

#for dispalying any message on window
def message_to_screen(text,color,x,y):
    message_screen=font.render(text,True,color)
    game_window.blit(message_screen,[x,y])

def snake_plot(game_window,color,snake_list,snake_size):
    for x,y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])

#CREATING THE HOME SCREEN
def welcome_screen():
    exit_game=False
    pygame.mixer.music.load("D:\\snake_game\\Game_Sprites\\begin_game.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        game_window.fill(WHITE)
        HOME_PIC=pygame.image.load("D:\\snake_game\\Game_Sprites\\home_pic.jpg")
        HOME_PIC=pygame.transform.scale(HOME_PIC,(800,500)).convert_alpha()
        game_window.blit(HOME_PIC,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
                pygame.quit()
                sys.exit()
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.load("D:\\snake_game\\Game_Sprites\\start.mp3")
                    pygame.mixer.music.play()
                    GAME_LOOP()
        pygame.display.update()
        clock.tick(30)

def GAME_LOOP():
    global bgimg
    #game specific variables
    exit_game=False
    game_over=False
    snake_in_x=20
    snake_in_y=40
    snake_size=20
    velocity_x=0
    velocity_y=0
    score=0
    snake_list=[]
    snake_lenght=1 # Initialising the snake lenght to 1.

    #we have to generate the food randomly.
    food_x=random.randint(40,game_window_width//1.5)
    food_y=random.randint(40,game_window_height//1.5)

    #check if hiscore file exists or not:
    if(not os.path.exists("HISCORE.txt")):
        with open("HISCORE.txt","w") as f:
            f.write("0")
    #OPEN FILE
    with open("HISCORE.txt","r") as f:
        High_score=f.read() # but it will return in string format.
    #creating a game loop
    while not exit_game:
        if game_over:
            game_end=pygame.image.load("D:\\snake_game\\Game_Sprites\\GAME_OVER.PNG")
            game_end=pygame.transform.scale(game_end,(800,500)).convert_alpha()
            with open("HISCORE.txt","w") as f:
                f.write(str(High_score))
                
            game_window.fill(WHITE)
            game_window.blit((game_end),(0,0))

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                
                if event.type==pygame.KEYDOWN: # ye check krega key dabi ya nhi.
                    if event.key==pygame.K_RETURN:# agar dabi h toh konsi dabi
                        bgimg=pygame.image.load("D:\\snake_game\\Game_Sprites\\Back.jpg")
                        bgimg=pygame.transform.scale(bgimg,(800,500)).convert_alpha()
                        
                        game_window.blit(bgimg,(0,0))
                        welcome_screen()
        

        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x +=7
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x +=-7
                        velocity_y=0
                    if event.key==pygame.K_UP:
                        velocity_y +=-7
                        velocity_x=0
                    if event.key==pygame.K_DOWN:
                        velocity_y +=7
                        velocity_x=0
                    if event.key==pygame.K_d:
                        score +=7

            snake_in_x += velocity_x
            snake_in_y += velocity_y

            # adding score when the food gets eated by the snake
            if abs(food_x - snake_in_x)<9 and abs(food_y - snake_in_y)<9:
                score +=10
                snake_lenght +=5
                food_x=random.randint(0,game_window_width)
                food_y=random.randint(0,game_window_height)

            if score>int(High_score):
                High_score=score
            
            game_window.fill(WHITE)
            game_window.blit(background,(0,0))

            # if the snake collide get collide then game get over.
            if snake_in_x<0 or snake_in_x>game_window_width or snake_in_y<0 or snake_in_y>game_window_height:
                game_over=True
                pygame.mixer.music.load("hit_sound.mp3")
                pygame.mixer.music.play()

            #calling the message_to_screen so that our score will get displayed
            message_to_screen("SCORE : "+str(score)+" HighScore: "+str(High_score),YELLOW,5,5)
            # displaying food on the window
            pygame.draw.circle(game_window,BLUE,(food_x,food_y),10)

            #creating the head of snake
            snake_head=[]
            snake_head.append(snake_in_x)
            snake_head.append(snake_in_y)
            snake_list.append(snake_head)

            if len(snake_list)>snake_lenght:
                del snake_list[0]
            
            #when the snake collide in itself
            if snake_head in snake_list[:-1]:
                game_over=True
                pygame.mixer.music.load("D:\\snake_game\\Game_Sprites\\hit_sound.mp3")
                pygame.mixer.music.play()

            snake_plot(game_window,RED,snake_list,snake_size)
        #updating the window
        pygame.display.update()
        clock.tick(FPS)

    #for stop pyagme  
    pygame.quit()
    #for exit from the program
    sys.exit()

#calling the welcome screen
welcome_screen()
#calling the gameloop
GAME_LOOP()

