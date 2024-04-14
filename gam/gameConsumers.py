import asyncio
from datetime import datetime, timedelta
from game import PongGame, WINNING_SCORE
from visul import Visualize as vsl
from game import Paddle, Ball
import pygame

print("Game started")
def start_game(room_name):
	print("in")
	game = PongGame()
	while True:

		"""from here""" 
		vsl.quit_game()
		vsl.press_key()
		game.screen.fill((0, 0, 0))
		Paddle.draw(game.p1_paddle, game.screen)
		Paddle.draw(game.p2_paddle, game.screen)
		Ball.draw(game.ball, game.screen)
		Paddle.vis_move_left(game.p2_paddle)
		Paddle.vis_move_right(game.p1_paddle)
		game.draw_score()
		game.increase_hit_score()
		game.draw_hit_score()
		pygame.display.update()
		"""to here for visualizing the game"""

		game.clock.tick()
		keys = pygame.key.get_pressed()
		game.handle_paddle_movement(keys)
		game.ball.move()
		game.handle_collision()
		game.scoreCheck()
		game.wonControl()
		
		#print("game score: ", game.p1_score, game.p2_score)
		if not game.won:
			pass
		else:
			game.frameCounter += 1

def test_ai():
	print("test ai")

start_game("room")