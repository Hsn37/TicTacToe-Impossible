import pyglet
import time
from random import randint
import tkinter as tk
from tkinter import messagebox as mb


# hide the tk window that comes with the dialog box
root = tk.Tk()
root.withdraw()

# turn choice
AI_SYMBOL = None
val = mb.askyesno('First Turn', 'Should AI take the first turn?')
if val:
	AI_SYMBOL = 1
else:
	AI_SYMBOL = 0

window = pyglet.window.Window(400, 450, "Tic Tac Toe Impossible")
window.set_location(x=500, y=100)

board = []
symbolSprites = []
boardFill = []
grid = pyglet.resource.image('src/Grid.png')
# cross = 1, circle = 0
cross_img = pyglet.resource.image('src/Cross.png')
circle_img = pyglet.resource.image('src/Circle.png')
IMAGES = [circle_img, cross_img]
turn = 1

# using two flags so that we can delay the drawing of the AI image
intermedFlag = False
drawAI = False
gameEnd = False
winner = None

# choosing the best action
# max == true means max player's turn
# scores: won = 1, draw = 0, loss = -1
# flags: winner = 1 or 0 depending on player. winner = 2 if draw
# tuples returned: (score, nextMove)
# -5 set as nextMove, if leaf node
def MinMaxAgent(maxPlayer, board):
	
	# if the board is empty, simply take the center or one of the corners.
	# doing this as it was taking considerable time to build the tree when board was empty. 
	if board == [-1 for x in range(9)]:
		# randomly choose one of these squares.
		p = [0, 2, 4, 6, 8]
		return (1, p[randint(0, len(p) - 1)])

	win = CheckWinner(board)
	if win != -1:
		if win == AI_SYMBOL:
			return (AI_SYMBOL, -5)
		elif win == 2:
			return (0, -5)
		else:
			return (-1, -5)
	
	scores = []
	moves = []
	for x in range(len(board)):
		if board[x] == -1:
			temp = board.copy()
			if maxPlayer:
				temp[x] = AI_SYMBOL
			else:
				temp[x] = 1 - AI_SYMBOL

			sc = MinMaxAgent(not maxPlayer, temp)[0]
			scores.append(sc)
			moves.append(x)

	# since board is symmetric. if two actions have same advantage, we can choose any of them, for the AI
	if maxPlayer:
		maxVal = max(scores)
		possibilities = [moves[x] for x in range(len(scores)) if scores[x] == maxVal]

		ind = randint(0, len(possibilities)-1)
		return (maxVal, possibilities[ind])
	else:
		minKey = scores.index(min(scores))
		return (scores[minKey], moves[minKey])


def SetBoardUp():
	# coords for the images
	# traversing from bottom left. go thru row first. then go to second row
	board.append([58, 50])		# row 1 col 1
	board.append([170, 50])		# row 1 col 2
	board.append([282, 50])		# row 1 col 3
	board.append([58, 164])		# row 2 col 1
	board.append([170, 164])	# row 2 col 2
	board.append([282, 164])	# row 2 col 3
	board.append([58, 278])		# row 3 col 1
	board.append([170, 278])	# row 3 col 2
	board.append([282, 278])	# row 3 col 3

	for p in range(0, 9):
		boardFill.append(-1)


def IdentifyBox(x, y):
	box = -1

	if x <= 139 and y <= 132:
		box = 0
	elif x <= 260 and y <= 132:
		box = 1
	elif x <= 400 and y <= 132:
		box = 2
	elif x <= 139 and y <= 251:
		box = 3
	elif x <= 260 and y <= 251:
		box = 4
	elif x <= 400 and y <= 251:
		box = 5
	elif x <= 139 and y <= 375:
		box = 6
	elif x <= 260 and y <= 375:
		box = 7
	elif x <= 400 and y <= 375:
		box = 8

	return box


@window.event
def on_mouse_press(x, y, button, modifiers):

	global turn, intermedFlag

	if turn != AI_SYMBOL and gameEnd == False:
		box = IdentifyBox(x, y)

		# user input
		if boardFill[box] == -1:
			symbolSprites.append(pyglet.sprite.Sprite(img=IMAGES[1-AI_SYMBOL], x=board[box][0], y=board[box][1]))
			boardFill[box] = 1 - AI_SYMBOL
			turn = AI_SYMBOL

			intermedFlag = True


def CheckWinner(board=boardFill):
	winningIndices = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

	for p in winningIndices:
		firstItem = board[p[0]]
		if firstItem != -1 and all([board[x] == firstItem for x in p]):
			return firstItem
	
	if all([x != -1 for x in board]):
		return 2

	return -1


@window.event
def on_draw():
	global gameEnd, drawAI, turn, intermedFlag, winner

	if gameEnd:
		textToShow = None
		if winner == 2:
			textToShow = 'DRAW'
		elif winner == AI_SYMBOL:
			textToShow = 'AI won'
		else:
			textToShow = 'Human won'

		mb.showinfo('Game Over', textToShow)

		time.sleep(1)
		pyglet.app.exit()

	if drawAI:
		drawAI = False;
		
		a, b = MinMaxAgent(True, boardFill.copy())
		if b != -5:
			symbolSprites.append(pyglet.sprite.Sprite(img=IMAGES[AI_SYMBOL], x=board[b][0], y=board[b][1]))
			boardFill[b] = AI_SYMBOL
			turn = 1 - AI_SYMBOL

		time.sleep(0.3)

		w = CheckWinner()
		if w != -1:
			winner = w
			gameEnd = True

	if intermedFlag:
		intermedFlag = False
		drawAI = True

	grid.blit(0, 0)
	for p in symbolSprites:
		p.draw()

	
def ProgLoop(dt):
	pass	


SetBoardUp()
if AI_SYMBOL == 1:
	intermedFlag = True

# for some reason, if i remove the scheduled function, the program doesnt draw properly.
pyglet.clock.schedule(ProgLoop)
pyglet.app.run()