import pygame
from os import path
import random


width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("змейка")
FPS = 10
clock = pygame.time.Clock()
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
snake_block = 30
snake_list = []
x1 = 400
y1 = 300
x1_change = 0
y1_change = 0
length = 1

music_dir = path.join(path.dirname(__file__), "music")
pygame.mixer.music.load(path.join(music_dir, "fon_music.mp3"))
am = pygame.mixer.Sound(path.join(music_dir, "eat.mp3"))
bad_game = pygame.mixer.Sound(path.join(music_dir, "game_over.mp3"))

img_dir = path.join(path.dirname(__file__), "img")

food_img = [pygame.image.load(path.join(img_dir, "apple.png")).convert(),
            pygame.image.load(path.join(img_dir, "banana.png")).convert(),
            pygame.image.load(path.join(img_dir, "orange1.png")).convert()]

head_image = [pygame.image.load(path.join(img_dir, "head_left.png")).convert(),
              pygame.image.load(path.join(img_dir, "head_down.png")).convert(),
              pygame.image.load(path.join(img_dir, "head_up.png")).convert(),
              pygame.image.load(path.join(img_dir, "head_right.png")).convert()]

snake_img = pygame.image.load(path.join(img_dir, "body3.png")).convert()
snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
snake.set_colorkey(white)

bad_game.set_volume(0.2)
bg = pygame.image.load(path.join(img_dir, "fon.jpg")).convert()
bg = pygame.transform.scale(bg, (width, height))
foodX = random.randrange(width - snake_block)
foodY = random.randrange(height - snake_block)
foodA = random.randrange(height - snake_block)
foodC = random.randrange(width - snake_block)


def eating_check(xcore, ycore, foodx, foody):
    if foodx - snake_block <= xcore <= foodx + snake_block:
        if foody - snake_block <= ycore <= foody + snake_block:
            am.play()
            return True

    else:
        return False


def create_mes(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mes = font_style.render(msg, True, color)
    screen.blit(mes, [x, y])


def game_loop():
    snake_list = []
    x1 = 400
    y1 = 300
    x1_change = 0
    y1_change = 0
    length = 1
    foodX = random.randrange(width - snake_block)
    foodY = random.randrange(height - snake_block)
    game_close = False
    run = True
    food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
    food.set_colorkey(white)
    pygame.mixer.music.play()

    while run:
        clock.tick(FPS)
        while game_close:
            screen.fill(red)
            create_mes("вы проиграли !", black, 200, 200, "chalkduster.tttf", 70)
            create_mes("нажмите Q для выхода и Y для перезапуска игры", black, 25, 300, "times", 35)
            pygame.mixer.music.pause()
            pygame.display.update()
            bad_game.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    elif event.key == pygame.K_y:
                        game_loop()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change -= snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change += snake_block
                    y1_change = 0


                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change -= snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change += snake_block

        if x1 >= width or x1 <= 0 or y1 >= height or y1 <= 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        # screen.fill(green)
        screen.blit(bg, (0, 0))
        # pygame.draw.rect(screen,red,(foodX,foodY,snake_block,snake_block))
        screen.blit(food, (foodX, foodY))
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for x in snake_list:
            # pygame.draw.rect(screen,white,(x[0],x[1],snake_block,snake_block))
            screen.blit(snake, (x[0], x[1]))

        if eating_check(x1, y1, foodX, foodY):
            foodX = random.randrange(width - snake_block)
            foodY = random.randrange(height - snake_block)
            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food.set_colorkey(white)
            length += 1

        create_mes(f"Текущий счет: {length - 1}", white, 455, 0, "comicsans", 35)

        pygame.display.update()
        pygame.display.flip()
    pygame.quit()
    quit()


game_loop()
