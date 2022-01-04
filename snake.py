import pygame
import time
import random
from pygame import mixer


mixer.init()
pygame.init()

#definir as cores para mais facil uso
white = (255,255,255)
blue = (0, 0, 255)
red = (255, 0, 0)
black= (0,0,0)
yellow = (255,255,102)
green = (0,255,0)


#assets load
sound_snake_eat = 'snake_eat.mp3'
sound_snake_death = 'snake_death.mp3'
background = pygame.image.load('relva.jpg')
background = pygame.transform.scale(background, (920,920))
head = pygame.image.load('head.png')
head = pygame.transform.scale(head, (20,20))
body_part = pygame.image.load("body.png")
body_part = pygame.transform.scale(body_part, (20,20))
fruit = pygame.image.load("fruit.png")
fruit = pygame.transform.scale(fruit, (20,20))

#criar a interface
dis_width = 800
dis_height = 600
display = pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption('Snake game by Tito')

#tamanho e velocidade da cobra
snake_block = 20
snake_speed = 10
clock = pygame.time.Clock()

#mensagens de avisos
font_style = pygame.font.SysFont('bahnschrift', 30)
font_style_score = pygame.font.SysFont('comicsanssms', 50)



def play_sound(sound):
    mixer.music.load(sound)
    mixer.music.play()

def message(msg,color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [0, dis_height/2])

def my_score(score):
    value = font_style_score.render(f'Score: {score}', True, green)
    display.blit(value, [0,0])

def the_snake(snake_block, snake_list):
    for x in snake_list[-1:]:
        display.blit(head,[x[0],x[1]])
    for x in snake_list[:-1]:
        display.blit(body_part,[x[0],x[1]])

def gameLoop():
    game_over= False
    game_close = False

    #posição inicial da cobra
    x1 = int(dis_width/2)
    y1 = int(dis_height/2)
    #movimento da cobra
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_lenght = 1

    food_x = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    
    while not game_close:

        while game_over == True:
            display.fill(white)
            message('Morreu! q -> sair j -> jogar', red)
            my_score(snake_lenght - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                        game_over = False
                    if event.key == pygame.K_j:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_close = True
                    game_over = False
        #quando carregar no X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            #movimentação da cobra ao carregar nas setas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0 
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        #definir as barreiras, qunado a cobra bate na borda perde o jogo
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True
            play_sound(sound_snake_death)
        x1 += x1_change
        y1 += y1_change

        display.fill(white)
        display.blit(background, [0,0])

        display.blit(fruit, [food_x,food_y])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_lenght:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True
                play_sound(sound_snake_death)


       
        the_snake(snake_block,snake_list)
        my_score(snake_lenght - 1)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, dis_width -snake_block) / snake_block) * snake_block
            food_y = round(random.randrange(0, dis_height -snake_block) / snake_block) * snake_block
            snake_lenght += 1
            play_sound(sound_snake_eat)
        clock.tick(snake_speed)

    pygame.quit()
    quit()
    
gameLoop()