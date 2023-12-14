from PIL import Image
from itertools import product
import random
import cv2

# todo: assymetric
# "Enter word or number to save image"

# variables

downStrokeWidth = 50
glyphSideLength = 300

# spacing of the vertical final stack
verticalSpacing = 0

glyphFolder = 'g/'

anywhereGlyphs = [[], [], ['c1', 'c2'], [], ['e1'], [], ['g2'], ['h2'], ['i1'],
                  ['j1', 'j2'], ['k2'], ['l1'], ['m3'], ['n2'], [], [],
                  ['q1', 'q2'], ['r1', 'r2'], ['s1', 's2'], ['t1'], ['u2'],
                  ['v1', 'v2'], ['w2', 'w3'], ['x1', 'x2'], ['y1', 'y2'],
                  ['z1', 'z2']]

startGlyphs = [['a1', 'a2i'], ['b2i'], [], ['d2'], ['e2'], ['f1i'], [],
               ['h2i'], [], [], [], [], ['m2'], [], ['o2i', 'o1'], ['p1i'], [],
               [], [], [], [], [], [], [], [], []]

middleGlyphs = [['a2'], ['b2'], [],
                ['d2i'], ['e2i'], ['f1'], [], [], [], [], [], [], [], [],
                ['o2i'], ['p1'], [], [], [], [], [], [], [], [], [], []]

endGlyphs = [['a1i', 'a2'], ['b2'], [], ['d2i'],
             ['e2i'], ['f1'], [], ['h1'], [], [], [], [], [], ['n1'], ['o2'],
             ['p1'], [], [], [], [], [], [], [], [], [], []]

bannedPairs = [['h2i', 'y2'], ['r1', 'r2'], ['h1', 'y2'], ['v1', 'v2'], ['e1', 'e2i'], ['s1', 's2']]

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

word = input("Enter a word > ").lower()
images = []


# functions
def letterIndex(letter):
  abc = 'abcdefghijklmnopqrstuvwxyz'
  return abc.index(letter)


def getImageNames(letter, imageList):
  img = imageList[letterIndex(letter)]
  images.append(img)


def getAndCombineImages(imageList):
  # Idk why 3 downstrokes is correct
  width = downStrokeWidth * 3
  for image in imageList:
    width += int(image[1]) * downStrokeWidth
  size = (width, glyphSideLength)
  color = (0, 0, 0, 0)
  out = Image.new('RGBA', size, color)
  x = 0
  for name in imageList:
    img = Image.open(glyphFolder + name + '.png')
    # print(name[0])
    out.paste(img, (x, 0), img)
    x += int(name[1]) * downStrokeWidth
  return out


def combineVertical(images):
  single = images[0].height
  height = single * len(images)
  height += verticalSpacing * (len(images) - 1)

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
    bg.paste(images[i], (x, y), images[i])
  return bg

def makeAmbigram(permutationList):
  ambigrams = []
  for index in range(len(permutationList)):
    if glyphFolder == 'g/':
      a = index + 1
      print('making ambigram number', a)
    else:
      print('making ambigram at index', bestIndex+1)
    images = permutationList[index]
    top = getAndCombineImages(images)
    bottom = top.rotate(180)
    top.paste(bottom, (0, 0), bottom)
  
    size = top.size
    color = (0,0,0,0)
    bg = Image.new('RGBA', size, color)
    bg.paste(top, (0, 0), top)
    ambigrams.append(bg)
  return ambigrams if len(ambigrams) > 1 else ambigrams[0]


# code
for index in range(len(word)):
  if index == 0:
    imageList = startGlyphs
  elif index == len(word) - 1:
    imageList = endGlyphs
  else:
    imageList = middleGlyphs
  getImageNames(word[index], imageList)

imageNamePermutations = list(product(*images))

newPermutations = []
for combo in imageNamePermutations:
  startGlyphs = combo[0] in extrudingStartGlyphs
  endGlyphs = combo[-1] in extrudingEndGlyphs
  a = startGlyphs and endGlyphs
  
  b = False
  for i in bannedPairs:
    if i[0] in combo and i[1] in combo:
      b = True
      break

  if not (a or b):
    newPermutations.append(combo)

ambigrams = makeAmbigram(newPermutations)

column = combineVertical(ambigrams)
column.save('o.png')

img = cv2.imread('o.png')

# Create a resizable window and display the image
cv2.namedWindow('Resizable Image', cv2.WINDOW_NORMAL)
cv2.imshow('Resizable Image', img) 

print('''
Done!''')

bestIndex = int(input(f'''
Type a number between 1 and {len(ambigrams)} > '''))
print()
bestIndex -= 1

downStrokeWidth*=10
glyphSideLength*=10
glyphFolder = 'g2/'

combineVertical([makeAmbigram([newPermutations[bestIndex]])]).save('o.png')

print('Done!')