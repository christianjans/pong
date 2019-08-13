# pong
Pong AI that learns from how you play.

## how to use
1. Install pygame and numpy
   '''
   pip install pygame
   '''
   '''
   pip install numpy
   '''
2. Run main.py
3. Play the game!

## project history
Originally, I just wanted to try and build a simple game with pygame, eventually deciding on Pong. However, once the single player and multiplayer modes were completed, I thought it wouldn't be too hard to add some sort of AI to one of the players. From a previous project, I had an existing neural network class (cjnn.py) that can create and train a fully-connected neural network, so I added it to the game.
As the user plays the single player and multiplayer modes, the game generates data for the neural network to learn from by getting the position of the paddle and the subsequent move associated with that position, and then feeding it through the neural network. The neural network reinforces these position-move pairs through gradient descent. 
One of the problems encountered with implementing a paddle that uses a neural network was that it would take too long to train if many inputs (such as the direction of the ball, x and y velocity of the ball, etc.) were fed into the neural network. In other words, if more inputs were added, the human player(s) would have to play a lot more rounds to see any progress in the neural net's paddle.
Therefore, this current version has the neural network only take in the difference in vertical position between its paddle and the ball and then decides to move up or down. This "AI" could probably just have been done with a perceptron or even a simple if-else statement, but it's kinda cool to see the paddle eventually figure out the right thing to do.
