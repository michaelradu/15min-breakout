# Setup Python ----------------------------------------------- #
import pygame
from random import randrange as rnd
from button import Button

WIDTH, HEIGHT = 1200, 800
fps = 60
# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
# block settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256),rnd(30,256),rnd(30,256)) for i in range(10) for i in range(4)]


# Setup pygame/window ---------------------------------------- #
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Breakout")
sc = pygame.display.set_mode((WIDTH, HEIGHT))
# background image
img = pygame.image.load('breakout_bg.png').convert()
img = pygame.transform.scale(img, (1200, 800))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def message_display(text, color, x=0, y=0, size=0):
    if size == 0:
        largeText = get_font(115)
    else:
        largeText = get_font(size)
    TextSurf = largeText.render(text, True, color)
    TextRect = TextSurf.get_rect()
    if x == 0 and y == 0:
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
    else: TextRect.center = (x,y)
    sc.blit(TextSurf, TextRect)

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 12:
        dx, dy = -dx, dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx

    return dx, dy



def pauseGame(text):
    loop = 1
    message_display(text, (255,255,255))
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                elif event.key == pygame.K_SPACE:
                    sc.fill((0,0,0))
                    loop = 0
                elif event.key == pygame.K_r:
                    restart()

        pygame.display.update()

def pauseScreen():
    pauseGame("PAUSED")

def gameOver():
    pauseGame("GAME OVER")
    message_display("Press R to restart", (255,255,255), (WIDTH/2+10), (HEIGHT/2+10))

def youWon():
    pauseGame("YOU WON!")
    message_display("Press R to restart", (255,255,255), (WIDTH/2+10), (HEIGHT/2+10))

def restart():
    global block_list
    global color_list
    global paddle
    global ball

    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
    color_list = [(rnd(30, 256),rnd(30,256),rnd(30,256)) for i in range(10) for i in range(4)]
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    game_loop()

def main_menu():
    while True:
        # sc.blit(img, (0, 0))
        sc.fill((0,0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("BREAKOUT", True, "#b78f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, HEIGHT//4))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH//2, HEIGHT//2), text_input="-PLAY-", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(WIDTH//2, HEIGHT//2 + 150), text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(WIDTH//2, HEIGHT//2 + 300), text_input="EXIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        sc.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(sc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()


score = 0

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pauseScreen()
                if event.key == pygame.K_r:
                    restart()
        sc.blit(img, (0, 0))
        # drawing world
        [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
        # ball movement
        global dx
        global dy

        global fps
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # collision left right
        if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx
        # collision top
        if ball.centery < ball_radius:
            dy = -dy
        # collision paddle
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        elif ball.centery > HEIGHT:
               gameOver()
        # collision blocks
        hit_index = ball.collidelist(block_list)
        global score
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            # special effects :)
            hit_rect.inflate_ip(ball.width // 4, ball.height // 6)
            pygame.draw.rect(sc, hit_color, hit_rect)
            fps += 2
            score += 1
        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed


        # score
        message_display(("Score: " + str(score)), (255,255,255), (WIDTH - 150), (30), 24)

        # You won!
        if len(block_list) == 0:
            youWon()

        # update screen
        pygame.display.flip()
        clock.tick(fps)



main_menu()
