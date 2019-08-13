import pygame

import random

import cjnn


# a button class, hopefully can add text to button eventually
class Button(pygame.Rect):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)

# parent paddle class, can move and reset
class Paddle(pygame.Rect):
	STEP = 10

	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)
		self.start_x = x
		self.start_y = y

	def move_up(self):
		self.y -= self.STEP

	def move_down(self):
		self.y += self.STEP

	def reset(self):
		self.x = self.start_x
		self.y = self.start_y

# child of paddle class, moves using neural net
class TrainablePaddle(Paddle):
	def __init__(self, x, y, width, height, brain):
		super().__init__(x, y, width, height)
		self.step = 10
		self.brain = brain

	# get the move from the neural net by feeding it inputs
	def move(self, inputs):
		action = self.brain.binary_guess(inputs)
		if action[0] == 1:
			self.move_up()
		else:
			self.move_down()

# ball class that moves, increases speed and resets
class Ball(pygame.Rect):
	MAX_VELOCITY = 20

	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)
		self.start_x = x
		self.start_y = y
		self.x_direction = 1 if random.random() > 0.5 else -1
		self.y_direction = 1 if random.random() > 0.5 else -1
		self.x_velocity = 6
		self.y_velocity = 0

	def move(self):
		self.x += self.x_direction * self.x_velocity
		self.y += self.y_direction * self.y_velocity

	def increase_speed(self):
		if self.x_velocity < self.MAX_VELOCITY:
			self.x_velocity += 2
		if self.y_velocity < self.MAX_VELOCITY:
			self.y_velocity += 2

	def reset(self):
		self.x = self.start_x
		self.y = self.start_y
		self.x_direction = 1 if random.random() > 0.5 else -1
		self.y_direction = 1 if random.random() > 0.5 else -1
		self.x_velocity = 6
		self.y_velocity = 0










