from PIL import Image, ImageDraw, ImageFont
import random
import os
import time
import string






def generateRandomString(setOfLetters, lenght):
    return ''.join(random.choice(setOfLetters) for i in range(lenght))


def generateText(img):
    textString = generateRandomString(textLetters, textLenght)
    
    d = ImageDraw.Draw(img)

    pos = [textPosition[0], textPosition[1]]
    
    for c in textString:
        
        selectedFontIndex = random.randint(0, len(fnt) - 1)
        selectedFont = fnt[selectedFontIndex]
        
        if debug: print(c + ' | ' + fontFileList[selectedFontIndex])

        if textRandomColor:
            charColor = generateRandomColor()
        else:
            charColor = mainColor
        
        d.text((pos[0], pos[1]), c, font = selectedFont, fill = charColor)

        charSize = d.textsize(c, font = selectedFont)
        pos[0] += charSize[0] * fontSpacing
        pos[1] = textPosition[1] + random.randint(-fontVerticalDivergence, fontVerticalDivergence)


def generateRandomCoordinates():
    return (random.randint(0, width), random.randint(0, height))

def generateRandomColor():
    if theme == 'DARK':
        vMin = 128
        vMax = 255
    elif theme == 'LIGHT':
        vMin = 0
        vMax = 128
    else:
        vMin = 0
        vMax = 255
        
    return (random.randint(vMin, vMax), random.randint(vMin, vMax), random.randint(vMin, vMax))


def generateRandomLines(img):
    d = ImageDraw.Draw(img)
    numberOfLines = random.randint(linesCountMin, linesCountMax)
    for i in range(numberOfLines):
        p1 = generateRandomCoordinates()
        p2 = generateRandomCoordinates()
        lineWidth = random.randint(linesWidthMin, linesWidthMax)
        if linesRandomColor:
            color = generateRandomColor()
        else:
            color = mainColor
        d.line([p1, p2], fill = color, width = lineWidth)

def generateRandomPoints(img):
    d = ImageDraw.Draw(img)
    numberOfPoints = random.randint(pointsCountMin, pointsCountMax)
    for i in range(numberOfPoints):
        p1 = generateRandomCoordinates()
        p2 = (p1[0] + random.randint(pointsSizeMin, pointsSizeMax), p1[1] + random.randint(pointsSizeMin, pointsSizeMax))
        if linesRandomColor:
            color = generateRandomColor()
        else:
            color = mainColor
        d.rectangle([p1, p2], fill = color)













# CONFIG

availableThemes = ['DARK', 'LIGHT', 'NONE']
theme = availableThemes[1]

width = 900
height = 400

textLenght = 6                          # Lenght of the captcha
textPosition = [75, 150]                # Starting position (x, y)
textLetters = string.ascii_uppercase    # Set of letters. Can be any string

mainColor = (0, 0, 0)
textRandomColor = False
backgroundColor = (255, 255, 255)

fontFolder = "font/"                    # Where are the font located
fontSizeMin = 130
fontSizeMax = 160
fontSpacing = 0.9                         # Seperation factor. 1 = no overlaying and no seperation.
fontVerticalDivergence = 50

linesEnabled = True
linesRandomColor = False
linesCountMin = 3
linesCountMax = 10
linesWidthMin = 1
linesWidthMax = 2

pointsEnabled = True
pointsRandomColor = False
pointsCountMin = 200
pointsCountMax = 1000
pointsSizeMin = 1
pointsSizeMax = 3

exportFolder = 'output/'
exportBatch = True
exportBatchCount = 100
exportName = 'captcha'
jpgQuality = 0

debug = False

# END CONFIG


# Get the list of font in the font folder
# Only otf and ttf files are accepted
fnt = []
fontFileList = os.listdir(fontFolder)

if debug: print('\n\nIMPORTING THE FONT FROM THIS FOLDER: ' + fontFolder + '\n')
for filepath in fontFileList:
    filename, file_extension = os.path.splitext(filepath)
    
    if file_extension.lower() == '.otf' or file_extension.lower() == '.ttf':
        fontSize = random.randint(fontSizeMin, fontSizeMax)
        fnt += [ImageFont.truetype(fontFolder + filename + file_extension, fontSize)]
        if debug: print(filename + file_extension + ' has been imported.')

    elif debug:
        print(fontFolder + filename + file_extension + ' is not a valid font file. Skipping it.')
    


numberOfCatcha = 1
if exportBatch: numberOfCatcha = exportBatchCount

for i in range(numberOfCatcha):
    
    if debug: print('')
    
    img = Image.new('RGB', (width, height), color = backgroundColor)

    generateText(img)
    if linesEnabled:  generateRandomLines(img)
    if pointsEnabled: generateRandomPoints(img)

    if exportBatch:
        img.save(exportFolder + exportName + '_' + str(i) + '.jpg', quality = jpgQuality)
    else:
        img.save(exportFolder + exportName + '.jpg', quality = jpgQuality)
        
    if debug: print('')

    

    
