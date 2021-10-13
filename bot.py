import time
from pynput.mouse import Controller, Button
from PIL import ImageGrab
from pprint import pprint

class Board:
	def __init__(self, width, height, mines):
		print("Creating board", end="")
		self.width = width
		self.height = height
		self.mines = mines
		self.flags = 0
		self.clicks = []
		self.flagged = []
		print(".", end="")
		self.tiles = []
		print(".", end="")
		for y in range(height):
			self.tiles.append([])
			for x in range(width):
				self.tiles[y].append(Tile(self, x, y))
		print(".")
		print("Setting neighbours", end="")
		for x in range(width):
			print(".", end="")
			for y in range(height):
				self.tiles[y][x].setNeighbours(self)
		print("\nBoard created:")

	def addClick(self, x, y, button):
		c = (x, y, button)
		self.clicks.append(c)

	def setValue(self, x, y, value):
		self.tiles[y][x].value = value

	def isFinished(self):
		return self.mines <= self.flags

	def getY(self, y):
		return int(mineHeight / 2 + (mineHeight + 2) * y)
	
	def getX(self, x):
		return int(mineWidth / 2 + (mineWidth + 2) * x)

	def updateBoard(self):
		time.sleep(0.07)
		ss = ImageGrab.grab(screenRegion)
		ss.convert("RGB")
		for y in range(self.height):
			currentY = self.getY(y)
			for x in range(self.width):
				currentX = self.getX(x)
				pixelColour = ss.getpixel((currentX, currentY))
				if pixelColour in colours:
					if colours.index(pixelColour) == 7:
						above = ss.getpixel((currentX, currentY - 10))
						if above == (255, 0, 0):
							self.setValue(x, y, "F")
							continue
					elif colours.index(pixelColour) == 0:
						above = ss.getpixel((currentX, currentY - 15))
						if above == (255, 255, 255):
							self.setValue(x, y, "#")
							continue
					self.setValue(x, y, colours.index(pixelColour))
				else:
					self.setValue(x, y, "?")
					print(currentX, currentY)
					print(x, y)
					input()
					ss.putpixel((currentX, currentY), (255, 0, 0))
					ss.show()

	def performIteration(self):
		for y in range(self.height):
			for x in range(self.width):
				self.tiles[y][x].update()
		self.performClicks()
	
	def performClicks(self):
		for c in self.clicks:
			click(c[0], c[1], c[2])
		self.clicks = []
	
	def getValue(self, x, y):
		return self.tiles[y][x].value
	
	def clearUncleared(self):
		for y in range(self.height):
			for x in range(self.width):
				if self.getValue(x, y) == "#":
					self.addClick(self.getX(x), self.getY(y), Button.left)
		self.performClicks()

class Tile:
	def __init__(self, board, x, y):
		self.board = board
		self.x = x
		self.y = y
		self.value = "?"
		self.neighbours = []
	
	def setNeighbours(self, board):
		self.neighbours = []
		for x in range(self.x - 1, self.x + 2):
			for y in range(self.y - 1, self.y + 2):
				if x >= 0 and x < board.width and y >= 0 and y < board.height:
					self.neighbours.append(board.tiles[y][x])
	
	def update(self):
		if self.value in ["#", "F", "?"]:
			return
		flaggedNeighbours = []
		unvisitedNeighbours = []
		for neighbour in self.neighbours:
			if neighbour.value == "#":
				unvisitedNeighbours.append(neighbour)
			elif neighbour.value == "F":
				flaggedNeighbours.append(neighbour)
		if (len(flaggedNeighbours) + len(unvisitedNeighbours) == int(self.value)
		    and unvisitedNeighbours):
			for neighbour in unvisitedNeighbours:
				pos = (neighbour.x, neighbour.y)
				if pos not in self.board.flagged:
					neighbour.value = "F"
					self.board.flags += 1
					currentX = int(mineWidth / 2 + (mineWidth + 2) * neighbour.x)
					currentY = int(mineHeight / 2 + (mineHeight + 2) * neighbour.y)
					self.board.addClick(currentX, currentY, Button.right)
					self.board.flagged.append(pos)
		elif len(flaggedNeighbours) == int(self.value):
			for neighbour in unvisitedNeighbours:
				currentX = int(mineWidth / 2 + (mineWidth + 2) * neighbour.x)
				currentY = int(mineHeight / 2 + (mineHeight + 2) * neighbour.y)
				self.board.addClick(currentX, currentY, Button.left)


"""
	COLOURS
"""
colours = [(189, 189, 189),
(0, 0, 255),
(0, 123, 0),
(255, 0, 0),
(0, 0, 123),
(123, 0, 0),
(0, 128, 128),
(0, 0, 0),
(128, 128, 128)]

def click(x, y, button):
	global controller
	x += corners[diff][0]
	y += corners[diff][1]
	move(x, y)
	controller.press(button)
	controller.release(button)

def move(x, y):
	global controller
	controller.position = (x, y)

def printBoard(b):
	for y in range(b.height):
		for x in range(b.width):
			print(b.getValue(x, y), end="")
		print()
	print()

msSize = [(9, 9), (16, 16), (30, 16)]
corners = [(563, 249), (518, 249), (294, 249)]
reset = [(700, 200), (770, 189), (764, 184)]
mines = [10, 40, 99]

diff = int(input("Please enter the difficulty (0: Beginner, 1: Advanced, 2: Expert):\t"))

msWidth = msSize[diff][0]
msHeight = msSize[diff][1]
areaWidth = msSize[diff][0] * 30 + msSize[diff][0] * 2 - 2
areaHeight = msSize[diff][1] * 30 + msSize[diff][1] * 2 - 2
print(f"Minesweeper region dimensions: {areaWidth} {areaHeight}")

screenRegion = (corners[diff][0], corners[diff][1], corners[diff][0] + areaWidth, corners[diff][1] + areaHeight)
print(f"Region: {screenRegion}")

mineWidth = 30
mineHeight = 30
print(f"Mine dimensions: {mineWidth} {mineHeight}")

controller = Controller()

board = Board(msSize[diff][0], msSize[diff][1], mines[diff])

tries = 0

def main():  # sourcery no-metrics
	global tries, board
	tries += 1
	controller.position = (reset[diff][0], reset[diff][1])
	controller.press(Button.left)
	controller.release(Button.left)

	print("Board reset")

	firstClickX = int(mineWidth / 2 + (mineWidth + 2) * int(msWidth / 2))
	firstClickY = int(mineHeight / 2 + (mineHeight + 2) * int(msHeight / 2))
	click(firstClickX, firstClickY, Button.left)

	timesDone = 0
	while not board.isFinished():
		timesDone += 1
		board.updateBoard()
		#printBoard(board)
		board.performIteration()
		print("Performed iteration!")
		#printBoard(board)

	board.clearUncleared()

if __name__ == "__main__":
	main()