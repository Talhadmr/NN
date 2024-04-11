import asyncio
from datetime import datetime, timedelta
from game import PongGame, WINNING_SCORE
print("Game started")

def start_game(room_name):
	print("in")
	game = PongGame()
	while not game.won and not game.finishGame:
		game.clock.tick()
		game.handle_paddle_movement()
		game.ball.move()
		game.handle_collision()
		game.scoreCheck()
		game.wonControl()
		print("game score: ", game.p1_score, game.p2_score)
		if not game.won:
			pass
		else:
			game.frameCounter += 1

start_game("room1")