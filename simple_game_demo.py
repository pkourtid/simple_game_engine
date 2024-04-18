# Written by Panagiotis Kourtidis

# =============================================================================
# Import Simple Game Engine Libraries
from game_libraries import *

# Import game resources (images, sounds, music)
from game_resources import *

# We need some standard modules for the game
from random import *
import math
import time
import operator

# Some needed functions
usleep = lambda x: time.sleep(x/1000000.0)
cotrans = lambda x,y,w: x + (w*y)

# Start the Simple Game Engine
objMyGame = clsSimpleGameEngine("Simple Game", 800, 600, 400, 300)

# Load the resources using the object found in game_resources.py
objMyGame.loadResources(listResources)

tmrCheckCombo = clsSimpleTimer()
tmrCheckCombo.resetTimer()

# =============================================================================
# Game Variables

intGameState = -1 # Indicates what state the game is in
intRotateAngle = 0

# ===========================================================================
# Define Game Functions

def drawWord(strWord, intStartPosX, intStartPosY, intCharSizeX, intCharSizeY, intSpacing):
	global objMyGame
	for i in range(len(strWord)):
		chrCharacter = strWord[i].upper()

		objMyGame.drawImage("chr"+chrCharacter, intStartPosX +(i*intSpacing), intStartPosY, intCharSizeX, intCharSizeY)


# ================================================================|
# MENU GENERATING METHODS
#
			
#
#
# ================================================================|

# ===========================================================================
# Start the Game Loop

objMyGame.resizeDisplay()

blnRunning = True
		
while blnRunning:

	# Clear the Screen
	objMyGame.displayClear()

	# Check what game state we are in and run the corresponding code

	match intGameState:

		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# Game main menu logic
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

		case -1:

			# Draw the game title
			objMyGame.drawImage("imgGameLogo", 1, 1, 20, 170)
			
			intRotateAngle = intRotateAngle + 1
			if (intRotateAngle > 360):
				intRotateAngle = 0
			objMyGame.drawSentence("ttfMenu", "This is a demo...", 0, 20, "yellow", intRotateFont=intRotateAngle)
			objMyGame.drawSentence("ttfMenu", "Panagiotis", 100, 100, "red", intRotateFont=intRotateAngle)

			# ================================================================|
			# KEYBOARD INPUT METHODS
			#

			# We can check if any key is pressed using the checkKeyDown process
			if (objMyGame.checkKeyDown(pygame.K_q) and objMyGame.checkKeyDown(pygame.K_LSHIFT)):
				blnRunning = False

			# We can check if a certain key was pressed. This process uses a fifo queue
			# You can use it when the sequence of the keys pressed is important to your game
			# Checking for the next available key press in the queue removes the key from the queue
			# You can also clear the queue if you want with the clearKeyPressed() method
			
			# Every 2 seconds check on the expected combo
			if (tmrCheckCombo.checkTimePassed(2000)):
				tmrCheckCombo.resetTimer()
				if (objMyGame.getKeyPressed() == pygame.K_UP and objMyGame.getKeyPressed() == pygame.K_DOWN):
					blnRunning = False

				objMyGame.clearKeyPressed()
			#
			#
			# ================================================================|

			
			

	# Display the screen
	objMyGame.displayUpdate()

	# Process all events
	objMyGame.processEvents()	

