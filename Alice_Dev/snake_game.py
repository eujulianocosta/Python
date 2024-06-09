import pygame
import time
import random
import json

pygame.init()

# Definir cores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Definir dimensões da tela
dis_width = 1366
dis_height = 768

# Inicializar a tela
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
button_font = pygame.font.SysFont("bahnschrift", 35)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])


def message(msg, color, pos):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, pos)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))
    
    text_surf = button_font.render(msg, True, white)
    dis.blit(text_surf, [x + (w / 2 - text_surf.get_width() / 2), y + (h / 2 - text_surf.get_height() / 2)])


def game_intro():
    intro = True

    player_name = ""
    speed_level = 15

    input_active = False

    def set_speed(speed):
        nonlocal speed_level
        speed_level = speed

    def start_game():
        nonlocal intro
        if player_name != "":
            intro = False

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        dis.fill(blue)
        message("Welcome to Snake Game", white, [dis_width / 6, dis_height / 6])
        pygame.draw.rect(dis, white, [dis_width / 6, dis_height / 3, 400, 50])
        message("Enter your name: " + player_name, black, [dis_width / 6 + 10, dis_height / 3 + 10])
        
        if input_active:
            pygame.draw.rect(dis, red, [dis_width / 6, dis_height / 3, 400, 50], 2)
        
        message("Select Speed: ", white, [dis_width / 6, dis_height / 2])
        button("1 (Slow)", dis_width / 2 - 150, dis_height / 2, 100, 50, green, yellow, lambda: set_speed(10))
        button("2 (Normal)", dis_width / 2, dis_height / 2, 100, 50, green, yellow, lambda: set_speed(15))
        button("3 (Fast)", dis_width / 2 + 150, dis_height / 2, 100, 50, green, yellow, lambda: set_speed(20))
        
        button("Start", dis_width / 2 - 50, dis_height / 1.5, 100, 50, green, yellow, start_game)
        
        pygame.display.update()

        if pygame.mouse.get_pressed()[0]:
            if dis_width / 6 < pygame.mouse.get_pos()[0] < dis_width / 6 + 400 and dis_height / 3 < pygame.mouse.get_pos()[1] < dis_height / 3 + 50:
                input_active = True

    return player_name, speed_level


def save_high_score(score, player_name):
    try:
        with open('high_scores.json', 'r') as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        high_scores = []
    
    high_scores.append({"name": player_name, "score": score})
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:5]

    with open('high_scores.json', 'w') as file:
        json.dump(high_scores, file)


def display_high_scores():
    try:
        with open('high_scores.json', 'r') as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        high_scores = []

    y_offset = 100
    for score_entry in high_scores:
        message(f"{score_entry['name']}: {score_entry['score']}", white, [dis_width / 3, dis_height / 3 + y_offset])
        y_offset += 40


def gameLoop():
    player_name, snake_speed = game_intro()

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red, [dis_width / 6, dis_height / 3])
            your_score(Length_of_snake - 1)
            save_high_score(Length_of_snake - 1, player_name)
            display_high_scores()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Movimento toroidal
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block
        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Corrigir a colisão com a comida
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()