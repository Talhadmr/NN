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
import pickle


def test_ai(config):
	with open("best.pickle", "rb") as f:
		genome = pickle.load(f)
	
	game = PongGame()
	net = neat.nn.FeedForwardNetwork.create(genome, config)
	while True:

		"""from here""" 
		vsl.quit_game()
		vsl.press_key()
		game.screen.fill((0, 0, 0))
		Paddle.draw(game.p1_paddle, game.screen)
		Paddle.draw(game.p2_paddle, game.screen)
		Ball.draw(game.ball, game.screen)
		game.draw_score()
		game.increase_hit_score()
		game.draw_hit_score()
		"""to here for visualizing the game"""

		game.clock.tick()
		keys = pygame.key.get_pressed()
		#game.handle_paddle_movement(keys)
		if keys[pygame.K_w] == 1:
			game.p1_paddle.move(up=1)
		if keys[pygame.K_s] == 1:
			game.p1_paddle.move(up=0)
		
		output = net.activate((game.p2_paddle.y, game.ball.y, abs(game.p2_paddle.x - game.ball.x)))
		decision = output.index(max(output))

		if(decision == 0):
			pass
		elif(decision == 1):
			game.p2_paddle.move(up=1)
		else:
			game.p2_paddle.move(up=0)

		game.ball.move()
		game.handle_collision()
		game.scoreCheck()
		game.wonControl()
		pygame.display.update()
		
		#print("game score: ", game.p1_score, game.p2_score)
		if not game.won:
			pass
		else:
			game.frameCounter += 1


def eval_genomes(genomes, config):
	game = PongGame()	

	for i, (genome_id1, genome1) in enumerate(genomes):
		print(round(i/len(genomes) * 100), end=" ")
		genome1.fitness = 0
		for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
			genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
			force_quit = game.train_ai(genome1, genome2, config)
			if force_quit:
				quit()

def run_neat(config):
	p = neat.Population(config)
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(1))
	
	winner = p.run(eval_genomes, 50)
	with open("best.pickle", "wb") as f:
		pickle.dump(winner, f)


if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config.txt")
	
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
					   neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_path)
	
	#run_neat(config)
	test_ai(config)
"""For execute the AI"""
 