import pygame
from game import PongGame as pg
pygame.init()

FPS = 60

WIDTH, HEIGHT = 1400, 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
"""
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
paddle_width = 20
paddle_height = 100
paddle_color = WHITE

left_paddle = pygame.Rect(0, HEIGHT/2 - paddle_height/2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - paddle_width, HEIGHT/2 - paddle_height/2, paddle_width, paddle_height)

running = True
while running:
    # Rest of the code...

    # Draw paddles
    pygame.draw.rect(screen, paddle_color, left_paddle)
    pygame.draw.rect(screen, paddle_color, right_paddle)

    # Rest of the code...

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
"""



class Visualize:

    def __init__(self):
        self.game = pg()

    
    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pg.finishGame = True
                break
        
    def press_key():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pg.finishGame = True