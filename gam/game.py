import time
import asyncio
import random
import neat 
import os
import pygame



""" for visualizing the game"""
import pygame
""" for visualizing the game"""
lis = []
class MyClock:
	def __init__(self, ticks_per_second):
		self.ticks_per_second = ticks_per_second
		self.tick_duration = 1 / ticks_per_second
		self.last_tick_time = time.time()

	def tick(self):
		current_time = time.time()
		elapsed_time = current_time - self.last_tick_time
		sleep_time = self.tick_duration - elapsed_time

		if sleep_time > 0:
			time.sleep(sleep_time)
		else:
			self.last_tick_time = current_time

		self.last_tick_time += self.tick_duration

WIDTH, HEIGHT = 1400, 1000

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 6, 200
BALL_RADIUS = 20

#this is the score that the game will be played until
WINNING_SCORE = 3


class Paddle:
	COLOR = WHITE
	VEL = 20

	def __init__(self, x, y, width, height):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.width = width
		self.height = height

	def move(self, up=1):
		if up == 1:
			if self.y - self.VEL >= 0:
				self.y -= self.VEL
			elif self.y - self.VEL < 0:
				self.y = 0
		else:
			if self.y + self.VEL + self.height <= HEIGHT:
				self.y += self.VEL
			elif self.y + self.VEL + self.height > HEIGHT:
				self.y = HEIGHT - self.height

	""" for visualizing the game"""
	def draw(self, screen):
		pygame.draw.rect(screen , (255, 255, 255), (self.x, self.y, self.width, self.height))
		#pygame.draw.rect(screen, self.COLOR, (self.x, self.y, 30, self.height))
	def vis_move_left(self):
		if pygame.key.get_pressed()[pygame.K_UP]:
			self.y -= 1
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			self.y += 1
	def vis_move_right(self):
		if pygame.key.get_pressed()[pygame.K_w]:
			self.y -= 1
		if pygame.key.get_pressed()[pygame.K_s]:
			self.y += 1
	""" for visualizing the game"""

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y


class Ball:
	MAX_VEL = 15.0
	COLOR = WHITE

	def __init__(self, x, y, radius):
		self.x = self.original_x = x
		self.y = self.original_y = y
		self.radius = radius
		self.x_vel = list([-1, 1])[random.randint(0,1)] * self.MAX_VEL
		self.y_vel = list([-1, 1])[random.randint(0,1)] * self.MAX_VEL
		
			

	def move(self):
		self.x = round(self.x + self.x_vel, 3)
		self.y = round(self.y + self.y_vel, 3)

	""" for visualizing the game"""
	def draw(self, screen):
		pygame.draw.circle(screen, self.COLOR, (int(self.x), int(self.y)), self.radius)
	""" for visualizing the game"""

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y
		self.x_vel = list([-1, 1])[random.randint(0,1)] * self.MAX_VEL
		self.y_vel = list([-1, 1])[random.randint(0,1)] * self.MAX_VEL

class PongGame:
	def __init__(self):
		""" for visualizing the game"""
		self.hit_score = 0
		self.debug()

		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		""" for visualizing the game"""
		
		self.p1_paddle =  Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
							2, PADDLE_WIDTH, PADDLE_HEIGHT)
		self.p2_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
							2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
		self.ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
		self.p1_score = 0
		self.p2_score = 0
		self.clock = MyClock(FPS)
		self.frameCounter = 0
		self.run = True
		self.won = False
		self.finishGame = False
		self.keys = {"player1Up":0,
				"player1Down":0,
				"player2Up":0,
				"player2Down":0}

	""" for visualizing the game"""

	def debug(self):
		print("debug")
	
	def draw_score(self):
		font = pygame.font.Font(None, 74)
		text = font.render(f"{self.p2_score} : {self.p1_score}", True, WHITE)
		text_rect = text.get_rect(center=(WIDTH/2, 30))
		self.screen.blit(text, text_rect)

	def increase_hit_score(self):
		if(self.ball.x == 1375 or self.ball.x == 25):
			self.hit_score += 1

	def draw_hit_score(self):
		font = pygame.font.Font(None, 74)
		text = font.render(f"Hit Score: {self.hit_score}", True, WHITE)
		text_rect = text.get_rect(center=(WIDTH/2, 70))
		self.screen.blit(text, text_rect)

	""" for visualizing the game"""

	"""for ai"""

	def train_ai(self, genome1, genome2, config):
		net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
		net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

		output1 = net1.activate((self.p1_paddle.y, self.ball.y, abs(self.p1_paddle.x - self.ball.x)))
		output2 = net2.activate((self.p2_paddle.y, self.ball.y, abs(self.p2_paddle.x - self.ball.x)))

		while True:
			"""from here""" 
			self.screen.fill((0, 0, 0))
			Paddle.draw(self.p1_paddle, self.screen)
			Paddle.draw(self.p2_paddle, self.screen)
			Ball.draw(self.ball, self.screen)
			Paddle.vis_move_left(self.p2_paddle)
			Paddle.vis_move_right(self.p1_paddle)
			self.draw_score()
			self.increase_hit_score()
			self.draw_hit_score()
			pygame.display.update()
			"""to here for visualizing the game"""

			#self.clock.tick()
			keys = pygame.key.get_pressed()
			#game.handle_paddle_movement(keys)
			self.ball.move()
			self.handle_collision()
			self.scoreCheck()
			self.wonControl()
			
			#print("game score: ", game.p1_score, game.p2_score)
			if not self.won:
				pass
			else:
				self.frameCounter += 1
			if self.p1_score >= 5 or self.p2_score >= 5:
				break


	"""for ai"""
	
	def handle_collision(self):
		if self.ball.y + self.ball.radius >= HEIGHT:
			self.ball.y_vel = -1 * abs(self.ball.y_vel)
		elif self.ball.y - self.ball.radius <= 0:
			self.ball.y_vel = abs(self.ball.y_vel)

		if self.ball.x_vel < 0:
			if self.ball.y + self.ball.radius >= self.p1_paddle.y and self.ball.y - self.ball.radius <= self.p1_paddle.y + self.p1_paddle.height:
				if self.ball.x - self.ball.radius <= self.p1_paddle.x + self.p1_paddle.width:
					self.ball.x_vel = abs(self.ball.x_vel)
					middle_y = self.p1_paddle.y + self.p1_paddle.height / 2
					difference_in_y = middle_y - self.ball.y
					reduction_factor = (self.p1_paddle.height / 2) / self.ball.MAX_VEL
					y_vel = difference_in_y / reduction_factor
					self.ball.y_vel = round(-1 * y_vel, 3)
		else:
			if self.ball.y + self.ball.radius >= self.p2_paddle.y and self.ball.y - self.ball.radius <= self.p2_paddle.y + self.p2_paddle.height:
				if self.ball.x + self.ball.radius >= self.p2_paddle.x:
					self.ball.x_vel = -1 * abs(self.ball.x_vel)
					middle_y = self.p2_paddle.y + self.p2_paddle.height / 2
					difference_in_y = middle_y - self.ball.y
					reduction_factor = (self.p2_paddle.height / 2) / self.ball.MAX_VEL
					y_vel = difference_in_y / reduction_factor
					self.ball.y_vel = round(-1 * y_vel, 3)

	def handle_paddle_movement(self, keys):
		if keys[pygame.K_w] == 1:
			self.p1_paddle.move(up=1)
		if keys[pygame.K_s] == 1:
			self.p1_paddle.move(up=0)
		if keys[pygame.K_UP] == 1:
			self.p2_paddle.move(up=1)
		if keys[pygame.K_DOWN] == 1:
			self.p2_paddle.move(up=0)
 
	def scoreCheck(self):
		if self.ball.x < 0:
			""" for visualizing the game"""	
			self.hit_score -= 1
			#self.hit_score = 0
			""" for visualizing the game"""
			self.p1_score += 1
			self.ball.reset()
			self.p1_paddle.reset()
			self.p2_paddle.reset()
		elif self.ball.x > WIDTH:
			""" for visualizing the game"""	
			self.hit_score -= 1
			#self.hit_score = 0
			""" for visualizing the game"""
			self.p2_score += 1
			self.ball.reset()
			self.p1_paddle.reset()
			self.p2_paddle.reset()

	def wonControl(self):
		if self.p1_score >= WINNING_SCORE:
			#print("KESIN BURASI1")
			self.won = True
		elif self.p2_score >= WINNING_SCORE:
			#print("KESIN BURASI2")
			self.won = True

		""" for visualizing the game"""	
		#changed for a test
		"""
		if 	self.won == True:
			self.ball.reset()
			self.p1_paddle.reset()
			self.p2_paddle.reset()
			#print("KESIN BURASI2")
		"""
		""" for visualizing the game"""