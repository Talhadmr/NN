from pong import Game 
import pygame

width, height = 1000, 800

window = pygame.display.set_mode((width,height))

game = Game(window, width, height)

run = True 
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        game.move_paddle(left= True, up=True)
    elif keys[pygame.K_s]:
        game.move_paddle(left= True, up=False)
    elif keys[pygame.K_ESCAPE]:
        pygame.quit()
    if keys[pygame.K_DOWN]:
        game.move_paddle(left= False, up=False)
    if keys[pygame.K_UP]:
        game.move_paddle(left= False, up=True)

    game_info = game.loop()
    print(F"left hit: {game_info.left_hits} \n left score: {game_info.left_score} \n right hit: {game_info.right_hits} \n right score: {game_info.right_score} \n ")
    game.draw()
    pygame.display.update()

pygame.quit()


print("debug")