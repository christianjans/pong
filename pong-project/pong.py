import pygame

import entities
import cjnn


# window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# constants
MENU_TEXT_SIZE = 32
INSTRUCTIONS_TEXT_SIZE = 24
GAME_FONT_SIZE = 24
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 80
SMALL_BUTTON_WIDTH = 80
SMALL_BUTTON_HEIGHT = 80
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
BALL_WIDTH = 20
BALL_HEIGHT = 20

# colours
MENU_BACKGROUND = (0, 0, 0)
GAME_BACKGROUND = (0, 0, 0)
MENU_FONT_COLOUR = (255, 255, 255)
INSTRUCTIONS_COLOUR = (250, 250, 50)
MULTIPLAYER_COLOUR = (250, 50, 50)
TRAIN_COLOUR = (50, 250, 250)
SINGLEPLAYER_COLOUR = (50, 250, 50)
RESET_COLOUR = (250, 50, 250)
GAME_ENTITIES_COLOUR = (250, 250, 250)

pygame.init()	# start pygame
icon = pygame.image.load("resources/icon.png")	# load icon image
pygame.display.set_icon(icon)
pygame.display.set_caption("Pong")	# set title	
background = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))		# create background object

# initialize the brain (neural net) for the trainable paddle
brain = cjnn.CJNeuralNetwork([1, 4, 2], 0.1)


def menu():
	# font for the menu
	font = pygame.font.SysFont('Comic Sans MS', MENU_TEXT_SIZE)

	# buttons for the menu
	instructions_button = entities.Button(50, 50, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT)
	multiplayer_button = entities.Button(0.3 * WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT)
	singleplayer_button = entities.Button((WINDOW_WIDTH - BUTTON_WIDTH) / 2, WINDOW_HEIGHT / 2,\
		BUTTON_WIDTH, BUTTON_HEIGHT)
	train_button = entities.Button(1.3 * WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT)
	reset_button = entities.Button(50, WINDOW_HEIGHT - BUTTON_HEIGHT - 50, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT)

	# while loop condition variable
	in_menu = True

	while in_menu:
		# refresh background
		background.fill(MENU_BACKGROUND)

		# check if user wants to exit the game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				choice = 'exit'
				in_menu = False

			# check if user clicked a button
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_position = event.pos
				if instructions_button.collidepoint(mouse_position):
					choice = 'instructions'
					in_menu = False
				elif multiplayer_button.collidepoint(mouse_position):
					choice = 'multiplayer'
					in_menu = False 
				elif singleplayer_button.collidepoint(mouse_position):
					choice = 'singleplayer'
					in_menu = False
				elif train_button.collidepoint(mouse_position):
					choice = 'train'
					in_menu = False
				elif reset_button.collidepoint(mouse_position):
					brain.reset_random()

		# display the text
		display_text(font, "Press yellow for instructions, red for multiplayer,",\
			(WINDOW_WIDTH / 2, 0.7 * WINDOW_HEIGHT / 2), MENU_FONT_COLOUR, centered = True)
		display_text(font, "green for multiplayer, blue to test, or purple to reset the AI!",\
			(WINDOW_WIDTH / 2, 0.7 * WINDOW_HEIGHT / 2 + MENU_TEXT_SIZE), MENU_FONT_COLOUR, centered = True)

		# draw the buttons
		pygame.draw.rect(background, INSTRUCTIONS_COLOUR, instructions_button)
		pygame.draw.rect(background, MULTIPLAYER_COLOUR, multiplayer_button)
		pygame.draw.rect(background, SINGLEPLAYER_COLOUR, singleplayer_button)
		pygame.draw.rect(background, TRAIN_COLOUR, train_button)
		pygame.draw.rect(background, RESET_COLOUR, reset_button)

		pygame.display.update()

	return choice

def instructions():
	# refresh background
	background.fill(MENU_BACKGROUND)

	# font for the instructions
	font = pygame.font.SysFont('Comic Sans MS', INSTRUCTIONS_TEXT_SIZE)

	# while loop condition variable
	in_instructions = True

	while in_instructions:
		# refresh the background
		background.fill(GAME_BACKGROUND)

		# check if user wants to exit the game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				in_instructions = False

		# check if ESC was pressed (go to menu)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			in_instructions = False

		# display the instructions
		display_text(font, 'For multiplayer:', (50, 50), MENU_FONT_COLOUR)
		display_text(font, '   - WASD on left vs. ARROW KEYS on right', (50, 50 + INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - Press ESC to go to menu', (50, 50 + 2 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, 'For single player:', (50, 50 + 4 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - Computer on left vs. ARROW KEYS on right',\
			(50, 50 + 5 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - Press ESC to go to menu', (50, 50 + 6 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, 'For testing:', (50, 50 + 8 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - AI on left vs. ARROW KEYS on right', (50, 50 + 9 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - The AI will watch your moves in single/multiplayer',\
			(50, 50 + 10 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - The AI will learn from your moves', (50, 50 + 11 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - May take a few rounds to notice results',\
			(50, 50 + 12 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, '   - Press ESC to go to menu', (50, 50 + 13 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)
		display_text(font, 'Press ESC to go to menu', (50, 50 + 15 * INSTRUCTIONS_TEXT_SIZE), MENU_FONT_COLOUR)

		pygame.display.update()


def play(computer_player):
	# font for the multiplayer mode
	font = pygame.font.SysFont('Comic Sans MS', GAME_FONT_SIZE)

	# make the entities
	paddle_one = entities.Paddle(50, (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
	paddle_two = entities.Paddle(WINDOW_WIDTH - PADDLE_WIDTH - 50,\
		(WINDOW_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
	ball = entities.Ball((WINDOW_WIDTH - BALL_WIDTH) / 2, (WINDOW_HEIGHT - BALL_HEIGHT) / 2, BALL_WIDTH, BALL_HEIGHT)

	# set the initial scores
	player_one_score = 0
	player_two_score = 0

	# while loop condition variables
	in_multiplayer = True
	round_started = False

	while in_multiplayer:
		# refresh the background
		background.fill(GAME_BACKGROUND)

		# check if user wants to exit the game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				in_multiplayer = False

		# move the ball if the game is started, display a message if not
		if round_started:
			ball.move()
		else:
			display_text(font, "Press space to start!", (WINDOW_WIDTH / 2, 0.6 * WINDOW_HEIGHT),\
				GAME_ENTITIES_COLOUR, centered = True)

		# get the vertical difference in distances b/w the ball and paddles for training
		dist_one = [paddle_one.y + PADDLE_HEIGHT / 2 - (ball.y + BALL_HEIGHT / 2)]
		dist_two = [paddle_two.y + PADDLE_HEIGHT / 2 - (ball.y + BALL_HEIGHT / 2)]

		# declare variables to hold the action that result b/c of the distance difference
		action_one = None
		action_two = None

		# handle key inputs from either both, or just one player
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			in_multiplayer = False
		if keys[pygame.K_SPACE] and not round_started:
			round_started = True
		if not computer_player and keys[pygame.K_w] and paddle_one.y > 0:
			paddle_one.move_up()
			action_one = [1, 0]
		if not computer_player and keys[pygame.K_s] and paddle_one.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
			paddle_one.move_down()
			action_one = [0, 1]
		if keys[pygame.K_UP] and paddle_two.y > 0:
			paddle_two.move_up()
			action_two = [1, 0]
		if keys[pygame.K_DOWN] and paddle_two.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
			paddle_two.move_down()
			action_two = [0, 1]

		# handle computer player's moves if there is one
		if computer_player:
			desired_position = ball.y - PADDLE_HEIGHT / 2
			action_one = [1, 0] if desired_position < paddle_one.y else [0, 1]
			paddle_one.y = desired_position

		# train the neural net
		if action_one != None:
			brain.fit(dist_one, action_one)
		if action_two != None:
			brain.fit(dist_two, action_two)

		# handle collision
		if ball.colliderect(paddle_one) or ball.colliderect(paddle_two):
			ball.x_direction *= -1
			ball.increase_speed()
		elif ball.y >= WINDOW_HEIGHT - BALL_HEIGHT or ball.y <= 0:
			ball.y_direction *= -1
		elif ball.x >= WINDOW_WIDTH - BALL_WIDTH:
			player_one_score += 1
			paddle_one.reset()
			paddle_two.reset()
			ball.reset()
			started = False
		elif ball.x <= 0:
			player_two_score += 1
			paddle_one.reset()
			paddle_two.reset()
			ball.reset()
			started = False

		# display the score
		display_text(font, str(player_one_score), (WINDOW_WIDTH / 2 - 50, 50), GAME_ENTITIES_COLOUR, centered = True)
		display_text(font, str(player_two_score), (WINDOW_WIDTH / 2 + 50, 50), GAME_ENTITIES_COLOUR, centered = True)

		# draw entities on the background
		pygame.draw.rect(background, GAME_ENTITIES_COLOUR, paddle_one)
		pygame.draw.rect(background, GAME_ENTITIES_COLOUR, paddle_two)
		pygame.draw.rect(background, GAME_ENTITIES_COLOUR, ball)
		
		pygame.display.update()


def test():
	# font for the multiplayer mode
	font = pygame.font.SysFont('Comic Sans MS', GAME_FONT_SIZE)

	# make the entities
	paddle_one = entities.TrainablePaddle(50, (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT, brain)
	paddle_two = entities.Paddle(WINDOW_WIDTH - PADDLE_WIDTH - 50,\
		(WINDOW_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
	ball = entities.Ball((WINDOW_WIDTH - BALL_WIDTH) / 2, (WINDOW_HEIGHT - BALL_HEIGHT) / 2, BALL_WIDTH, BALL_HEIGHT)

	# set the initial scores
	player_one_score = 0
	player_two_score = 0

	# while loop condition variables
	in_training = True
	round_started = False

	while in_training:
		# refresh the background
		background.fill(GAME_BACKGROUND)

		# check if user wants to exit the game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				in_training = False

		# move the ball if the game is started, display a message if not
		if round_started:
			ball.move()
		else:
			display_text(font, "Press space to start!", (WINDOW_WIDTH / 2, 0.6 * WINDOW_HEIGHT),\
				GAME_ENTITIES_COLOUR, centered = True)

		# get the inputs for the trainable paddle
		inputs = [paddle_one.y + PADDLE_HEIGHT / 2 - (ball.y + BALL_HEIGHT / 2)]

		# handle key inputs from either both, or just one player
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			in_training = False
		if keys[pygame.K_SPACE] and not round_started:
			round_started = True
		if keys[pygame.K_UP] and paddle_two.y > 0:
			paddle_two.move_up()
		if keys[pygame.K_DOWN] and paddle_two.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
			paddle_two.move_down()

		# move the trainable paddle
		paddle_one.move(inputs)

		# handle collision
		if ball.colliderect(paddle_one) or ball.colliderect(paddle_two):
			ball.x_direction *= -1
			ball.increase_speed()
		elif ball.y >= WINDOW_HEIGHT - BALL_HEIGHT or ball.y <= 0:
			ball.y_direction *= -1
		elif ball.x >= WINDOW_WIDTH - BALL_WIDTH:
			player_one_score += 1
			paddle_one.reset()
			paddle_two.reset()
			ball.reset()
			started = False
		elif ball.x <= 0:
			player_two_score += 1
			paddle_one.reset()
			paddle_two.reset()
			ball.reset()
			started = False

		# display the score
		display_text(font, str(player_one_score), (WINDOW_WIDTH / 2 - 50, 50), GAME_ENTITIES_COLOUR, centered = True)
		display_text(font, str(player_two_score), (WINDOW_WIDTH / 2 + 50, 50), GAME_ENTITIES_COLOUR, centered = True)

		# draw entities on the background
		pygame.draw.rect(background, GAME_ENTITIES_COLOUR, paddle_one)
		pygame.draw.rect(background, GAME_ENTITIES_COLOUR, paddle_two)
		pygame.draw.rect(background, GAME_ENTITIES_COLOUR, ball)

		pygame.display.update()


# display text without a hassle
def display_text(font, text, position, colour, centered = False):
	# get the textview to do some positioning if needed
	text_view = font.render(text, True, colour)
	if position == 'center':	# position in center of screen
		background.blit(text_view, ((WINDOW_WIDTH - text_view.get_rect().width) / 2, WINDOW_HEIGHT / 2))
	elif not centered:	# position the top left according to the position argument
		background.blit(text_view, position)
	else:	# position the center at the position argument
		background.blit(text_view, (position[0] - text_view.get_rect().width / 2,\
			position[1] - text_view.get_rect().height / 2))


if __name__ == "__main__":
	while True:
		# get a choice from the menu
		choice = menu()

		# go through the choices
		if choice == 'instructions':
			instructions()
		if choice == 'multiplayer':
			play(False)
		elif choice == 'singleplayer':
			play(True)
		elif choice == 'train':
			test()
		elif choice == 'exit':
			break












