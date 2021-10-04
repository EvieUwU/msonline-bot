import mouse, time
from PIL import ImageGrab

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
	x += corners[diff][0]
	y += corners[diff][1]
	mouse.move(x, y)
	time.sleep(0.01)
	mouse.click(button=button)
	time.sleep(0.01)

def getBoard():
	time.sleep(0.01)
	ss = ImageGrab.grab(screenRegion)
	#ss.show()
	ss.convert("RGB")
	board = []
	for y in range(msWidth):
		board.append([])
		currentY = int(mineHeight / 2 + (mineHeight + 2) * y)
		for x in range(msHeight):
			currentX = int(mineWidth / 2 + (mineWidth + 2) * x)
			pixelColour = ss.getpixel((currentX, currentY))
			#ss.putpixel((currentX, currentY), (200, 200, 200))
			#ss.show()
			if pixelColour in colours:
				if colours.index(pixelColour) == 7:
					above = ss.getpixel((currentX, currentY - 10))
					if above == (255, 0, 0):
						board[y].append("F")
						continue
				elif colours.index(pixelColour) == 0:
					above = ss.getpixel((currentX, currentY - 15))
					if above == (255, 255, 255):
						board[y].append("#")
						continue
				board[y].append(str(colours.index(pixelColour)))
			else:
				board[y].append("/")
	return board

def printboard(board):
	for y in board:
		for x in y:
			print(x, end="")
		print()

msWidth = 9
msHeight = 9
areaWidth = msWidth * 30 + msWidth * 2 - 2
areaHeight = msHeight * 30 + msHeight * 2 - 2
print(f"Minesweeper region dimensions: {areaWidth} {areaHeight}")

corners = [(563, 249), (519, 249), (295, 249)]
reset = [(700, 200), (770, 189), (764, 184)]
mines = [10, 40, 99]

diff = int(input("Please enter the difficulty (0: Beginner, 1: Advanced, 2: Expert):\t"))

screenRegion = (corners[diff][0], corners[diff][1], 563 + areaWidth, 249 + areaHeight)
print(f"Region: {screenRegion}")

mineWidth = (areaWidth - msWidth * 2 + 2) / msHeight
mineHeight = (areaHeight - msHeight * 2 + 2) / msWidth
print(f"Mine dimensions: {mineWidth} {mineHeight}")

tries = 0

def main():  # sourcery no-metrics
	global tries
	tries += 1
	mouse.move(reset[diff][0], reset[diff][1])
	time.sleep(0.01)
	mouse.click()
	time.sleep(0.01)

	print("Board reset")

	firstClickX = int(mineWidth / 2 + (mineWidth + 2) * int(msWidth / 2))
	firstClickY = int(mineHeight / 2 + (mineHeight + 2) * int(msHeight / 2))
	click(firstClickX, firstClickY, "left")
	time.sleep(0.1)

	numMines = mines[diff]
	numFlags = 0
	timesDone = 0
	prevBoards = []
	confused = False
	while numFlags != numMines:
		timesDone += 1
		board = getBoard()
		matching = sum(board == b for b in prevBoards)
		if matching == len(prevBoards) and len(prevBoards) == 2:
			flagCount = 0
			for y in board:
				for x in y:
					flagCount += 1 if x == "F" else 0
			if flagCount != numMines:
				confused = True
				print("I'm confused :/")
				break
			break
		toClick = []
		for yi, y in enumerate(board):
			for xi, x in enumerate(y):
				if x == "0":
					continue
				if x in ["#", "F"]:
					continue
				if x == "/":
					main()
				blankAdjacent = []
				flagAdjacent = []
				for changeY in range(-1, 2):
					for changeX in range(-1, 2):
						if changeX == 0 and changeY == 0:
							continue
						if xi + changeX < 0 or xi + changeX >= msWidth:
							continue
						if yi + changeY < 0 or yi + changeY >= msHeight:
							continue
						if board[yi + changeY][xi + changeX] == "#":
							blankAdjacent.append((xi + changeX, yi + changeY))
						if board[yi + changeY][xi + changeX] == "F":
							flagAdjacent.append((xi + changeX, yi + changeY))
				remainingMines = str(int(x) - len(flagAdjacent))
				if str(len(flagAdjacent)) == x:
					for neighbour in blankAdjacent:
						if board[neighbour[1]][neighbour[0]] != "#":
							continue
						clickX = int(mineWidth / 2 + (mineWidth + 2) * (neighbour[0]))
						clickY = int(mineHeight / 2 + (mineHeight + 2) * (neighbour[1]))
						if (clickX, clickY, "left") not in toClick:
							toClick.append((clickX, clickY, "left"))
					continue
				if str(len(blankAdjacent)) == remainingMines:
					for neighbour in blankAdjacent:
						if board[neighbour[1]][neighbour[0]] != "#":
							continue
						board[neighbour[1]][neighbour[0]] = "F"
						numFlags += 1
						clickX = int(mineWidth / 2 + (mineWidth + 2) * (neighbour[0]))
						clickY = int(mineHeight / 2 + (mineHeight + 2) * (neighbour[1]))
						if (clickX, clickY, "right") not in toClick:
							toClick.append((clickX, clickY, "right"))
		for c in toClick:
			click(c[0], c[1], c[2])
		prevBoards.insert(0, board)
		if len(prevBoards) >= 3:
			prevBoards.pop()

	if not confused:
		for yi, y in enumerate(board):
			for xi, x in enumerate(y):
				if x == "#":
					clickX = int(mineWidth / 2 + (mineWidth + 2) * xi)
					clickY = int(mineHeight / 2 + (mineHeight + 2) * yi)
					click(clickX, clickY, "left")
		print("Finished!")
	else:
		if tries > 50:
			print("I've tried too many times ;w;")
			return
		main()

if __name__ == "__main__":
	main()