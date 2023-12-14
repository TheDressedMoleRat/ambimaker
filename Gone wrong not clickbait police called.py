from PIL import Image
from itertools import product
import random

# todo: assymetric
# "Enter word or number to save image"

# variables

# resize = 1 means no resize
resizeMultiplier = .1
downStrokeWidth = int(500 * resizeMultiplier)
glyphSideLength = int(3000 * resizeMultiplier)

# spacing of the vertical final stack
verticalSpacing = 0

anywhereGlyphs = [[], [], ['c1', 'c2'], [], ['e1'], [], ['g2'], ['h2'], ['i1'],
			 ['j1', 'j2'], ['k2'], ['l1'], ['m3'], ['n2'], [], [], ['q1', 'q2'],
			 ['r1', 'r2'], ['s1', 's2'], ['t1'], ['u2'], ['v1', 'v2'], ['w2', 'w3'],
			 ['x1', 'x2'], ['y1', 'y2'], ['z1', 'z2']]

startGlyphs = [['a1', 'a2i'], ['b2i'], [], ['d2'], ['e2'], ['f1i'], [], ['h2i'], [],
				 [], [], [], ['m2'], [], ['o2i', 'o1'], ['p1i'], [], [], [], [], [],
				 [], [], [], [], []]

middleGlyphs = [['a2'], ['b2'], [], ['d2i'], ['e2i'], ['f1'], [], [], [], [], [], [],
					[], [], ['o2i'], ['p1'], [], [], [], [], [], [], [], [], [], []]

endGlyphs = [['a1i', 'a2'], ['b2'], [], ['d2i'], ['e2i'], ['f1'], [], ['h1'], [], [],
			 [], [], [], ['n1'], ['o2'], ['p1'], [], [], [], [], [], [], [], [], [],
			 []]

extrudingStartGlyphs = ['a1', 'o1']

extrudingEndGlyphs = ['a1i', 'n1']

colors = [(255, 192, 203, 255), (255, 209, 220, 255), (255, 223, 186, 255),
					(255, 228, 196, 255), (255, 240, 245, 255), (249, 236, 191, 255),
					(220, 220, 255, 255), (240, 255, 240, 255), (223, 240, 216, 255),
					(214, 234, 230, 255), (173, 216, 230, 255), (144, 238, 144, 255)]

for i in range(len(anywhereGlyphs)):
	startGlyphs[i] += anywhereGlyphs[i]
	middleGlyphs[i] += anywhereGlyphs[i]
	endGlyphs[i] += anywhereGlyphs[i]

word = input("Enter a word >").lower()


# functions
def letterIndex(letter):
	abc = 'abcdefghijklmnopqrstuvwxyz'
	return abc.index(letter)


def getImageNames(letter, imageList):
	img = imageList[letterIndex(letter)]
	imageNames.append(img)


def getAndCombineImages(imageList):
	width = downStrokeWidth * 3
	for image in imageList:
		width += int(image[1]) * downStrokeWidth
	size = (width, glyphSideLength)
	color = (0, 0, 0, 0)
	out = Image.new('RGBA', size, color)
	x = 0
	for name in imageList:
		img = Image.open('C:/Users/alvar/Programming/Python/ambimaker/g/' + name + '.png')
		size = (glyphSideLength, glyphSideLength)
		if resizeMultiplier != 1:
			img = img.resize(size, Image.NEAREST)
		out.paste(img, (x, 0), img)
		x += int(name[1]) * downStrokeWidth
	return out


def combineVertical(images):
	single = images[0].height
	height = single * len(images)
	height += verticalSpacing * (len(images)-1)
	
	widths = []
	for i in images:
		widths.append(i.width)
	width = max(widths)
	
	color = random.choice(colors)
	size = (width, height)
	bg = Image.new('RGBA', size, color)
	for i in range(len(images)):
		y = i * (single + verticalSpacing)
		x = (width - images[i].width) // 2
		bg.paste(images[i],(x,y),images[i])
	return bg


# code
# Remove all duplicate letters in word
firstLetter = word[0]
lastLetter = word[-1]
middleLetters = list(set(word[1:-1]))

imageNames = []

# Get all the image names
getImageNames(firstLetter, startGlyphs)
for letter in middleLetters:
	getImageNames(letter, middleGlyphs)
getImageNames(lastLetter, endGlyphs)

print("imageNames:", imageNames)

imageNamePermutations = list(product(*imageNames))

# Filter through permutations to remove starters and enders matching
oldPermutations = imageNamePermutations.copy()
imageNamePermutations = []
for combo in oldPermutations:
	hasStarter = combo[0] in extrudingStartGlyphs
	hasEnder = combo[-1] in extrudingEndGlyphs
	if not (hasStarter and hasEnder):
		imageNamePermutations.append(combo)

# Remove all but the first letter, if it is a starter
oldPermutations = imageNamePermutations.copy()

imageNamePermutations = [[] for i in oldPermutations]

for i in range(len(oldPermutations)):
	if oldPermutations[i][0] in extrudingStartGlyphs:
		imageNamePermutations[i] = [oldPermutations[i][0]]

# Re-add duplicate letters
for permutationIndex in range(len(oldPermutations)):
	for letter in word[1:]:
		# Search for "letter" in permutation[1:]
		# currentLetterList = middleGlyphs[letterIndex(letter)] + endGlyphs[letterIndex(letter)]
		currentLetterList = middleGlyphs[letterIndex(letter)]

		imageNamePermutations[permutationIndex] = list(imageNamePermutations[permutationIndex])
		for guess in oldPermutations[permutationIndex][1:]:
			if guess in currentLetterList:
				imageNamePermutations[permutationIndex].append(guess)

ambigramImages = []
for index in range(len(imageNamePermutations)):
	print('making ambigram number', index + 1)
	imageNames = imageNamePermutations[index]
	topHalf = getAndCombineImages(imageNames)
	bottomHalf = topHalf.rotate(180)

	size = topHalf.size
	color = (0,0,0,0)
	bg = Image.new('RGBA', size, color)
	bg.paste(topHalf, (0, 0), topHalf)
	bg.paste(bottomHalf, (0, 0), bottomHalf)
	ambigramImages.append(bg)

imageColumn = combineVertical(ambigramImages)
imageColumn.save('C:/Users/alvar/Programming/Python/ambimaker/o.png')
print('done!')