import time
import asyncio
import random

class MyClock:
	def __init__(self, ticks_per_second):
		self.ticks_per_second = ticks_per_second
		self.tick_duration = 1 / ticks_per_second
		self.last_tick_time = time.time()

	async def tick(self):
		current_time = time.time()
		elapsed_time = current_time - self.last_tick_time
		sleep_time = self.tick_duration - elapsed_time

		if sleep_time > 0:
			await asyncio.sleep(sleep_time)
		else:
			self.last_tick_time = current_time

		self.last_tick_time += self.tick_duration


WIDTH, HEIGHT = 1400, 1000

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 6, 200
BALL_RADIUS = 20

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
		self.y_vel = 0.0

	def move(self):
		self.x = round(self.x + self.x_vel, 3)
		self.y = round(self.y + self.y_vel, 3)

	def reset(self):
		self.x = self.original_x
		self.y = self.original_y
		self.x_vel = list([-1, 1])[random.randint(0,1)] * self.MAX_VEL
		self.y_vel = 0

class PongGame:
	def __init__(self):
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

	def handle_paddle_movement(self):
		if self.keys["player1Up"] == 1:
			self.p1_paddle.move(up=1)
		if self.keys["player1Down"] == 1:
			self.p1_paddle.move(up=0)
		if self.keys["player2Up"] == 1:
			self.p2_paddle.move(up=1)
		if self.keys["player2Down"] == 1:
			self.p2_paddle.move(up=0)

	def scoreCheck(self):
		if self.ball.x < 0:
			self.p1_score += 1
			self.ball.reset()
			self.p1_paddle.reset()
			self.p2_paddle.reset()
		elif self.ball.x > WIDTH:
			self.p2_score += 1
			self.ball.reset()
			self.p1_paddle.reset()
			self.p2_paddle.reset()

	def wonControl(self):
		if self.p1_score >= WINNING_SCORE:
			print("KESIN BURASI1")
			self.won = True
		elif self.p2_score >= WINNING_SCORE:
			print("KESIN BURASI2")
			self.won = True
		if 	self.won == True:
			self.ball.reset()
			self.p1_paddle.reset()
			self.p2_paddle.reset()
