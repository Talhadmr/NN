import asyncio
from datetime import datetime, timedelta
from game import PongGame, WINNING_SCORE
from visul import Visualize as vsl
from game import Paddle, Ball
import time
import asyncio
import random
import neat 
import os
import pygame

def start_game(room_name):
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

"""For execute the AI"""

def eval_genomes(genomes, config):
	
	game = PongGame()

	for i, (genome_id1, genome1) in enumerate(genomes):
		if i == len(genomes) - 1:
			break
		genome1.fitness = 0
		for genome_id2, genome2 in genomes[i+1:]:
			genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
			game.train_ai(genome1, genome2,config)

def run_neat(config):
	p = neat.Population(config)
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(1))
	
	winner = p.run(eval_genomes, 50)


if __name__ == "__main__":
	#start_game("room")
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config.txt")
	
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	
	run_neat(config)
	#test_ai()
"""For execute the AI"""
 