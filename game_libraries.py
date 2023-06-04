# Written by Panagiotis Kourtidis

# =============================================================================
# Import pygame libraries

import pygame
from pygame.locals import *
from pygame import mixer
from pygame import freetype
import math
import base64
import os
import queue


class clsSimpleGameEngine:

	def __init__(self, strGameName, intWindowWidth, intWindowHeight, intGameWidth, intGameHeight):
		
		print("sge> Initialize...")
		
		# =============================================================================
		# Initialize pygame
		# =============================================================================

		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption(strGameName)	

		self.screen = pygame.display.set_mode((intWindowWidth, intWindowHeight), RESIZABLE)
		
		# =============================================================================
		# Initialize autoscaler variables
		# =============================================================================
		
		self.decScaleWidth = 1.0
		self.decScaleHeight = 1.0
		self.decScaleGame = 1.0;
		self.decOffsetWidth = 0.0;
		self.decOffsetHeight = 0.0;
		self.intGameWidth = float(intGameWidth)
		self.intGameHeight = float(intGameHeight)

		# =============================================================================
		# Initialize color values		
		# =============================================================================

		self.colors = {}
		self.colors["white"] = (255, 255, 255)
		self.colors["black"] = (0, 0, 0)
		self.colors["transparent"] = (0, 255, 255)
		
		# =============================================================================
		# Container to keep resources
		# =============================================================================

		self.dicImages = {}
		self.dicSounds = {}
		self.dicMusic = {}
		self.dicFonts = {}
		
		# =============================================================================
		# Initialize input variables
		# =============================================================================
		
		self.intPressedQueueSize = 100
		self.queKeyPressedQueue = queue.Queue(self.intPressedQueueSize)
		self.dicKeyDown = {}

		# =============================================================================
		# Initialize Menu Variables
		# =============================================================================

		self.intMenuPlacement = 0
		self.intSelectedItem = 0
		self.dicMenuItems = {}

	def __del__(self):
		
		print("sge> Cleaning Up...")
	
		pygame.quit()
		
	def loadResources(self,listResources):

		print("sge> Loading Resources: ",end="")

		intCountImages = 0
		intCountSounds = 0
		intCountMusic = 0
		intCountFonts = 0

		for resources in listResources:
			if (resources["type"] == "image"):
				intCountImages = intCountImages + 1
				self.dicImages[resources["name"]] = pygame.image.load(resources["src"])
			elif (resources["type"] == "sound"):
				intCountSounds = intCountSounds + 1
				self.dicSounds[resources["name"]] = pygame.mixer.Sound(resources["src"])
			elif (resources["type"] == "music"):
				intCountMusic = intCountMusic + 1
				self.dicMusic[resources["name"]] = pygame.mixer.music.load(resources["src"])
			elif (resources["type"] == "font"):
				intCountFonts = intCountMusic + 1
				self.dicFonts[resources["name"]] = pygame.font.Font(resources["src"], resources["size"])
				self.dicFonts[resources["name"]+"_src_ref"] = resources["src"]

		print("images (" + str(intCountImages) + ")" + ", sounds(" + str(intCountSounds) + ")" + ", fonts(" + str(intCountFonts) + ")" )

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# When the screen is re-sized this function is triggered
	# We calculate some variables to help up scale and center the whole game 
			  
	def resizeDisplay(self):
		
		#calculate the scale to be used and the offset from center
		
		# get the screen size
		x, y = self.screen.get_size()

		self.decScaleWidth = float(x) / self.intGameWidth
		self.decScaleHeight = float(y) / self.intGameHeight
		
		# set a few scaling variables
		if (self.decScaleWidth < self.decScaleHeight):
			self.decScaleGame = self.decScaleWidth
			self.decOffsetHeight = (y - (self.intGameHeight*self.decScaleGame))/2
			self.decOffsetWidth = 0.0
		else:
			self.decScaleGame = self.decScaleHeight;
			self.decOffsetWidth = (x - (self.intGameWidth*self.decScaleGame))/2
			self.decOffsetHeight = 0.0	

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# Create a function to play a previously loaded sound

	def playSound(self, strSndObject):
		
		pygame.mixer.Sound.play(self.dicSounds[strSndObject])

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# Create a function to play a previously loaded music
	
	def playMusic(self):
		
		pygame.mixer.music.play(-1)

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# Create a function to draw an image on the canvas honoring the scale

	def drawImage(self, objImgObject, intOffsetX, intOffsetY, intWidth, intHeight, alpha = 255, intRotate = 0):

		intDimW = math.ceil(intWidth*self.decScaleGame)
		intDimH = math.ceil(intHeight*self.decScaleGame)

		intOffsetWidth = 0
		intOffsetHeight = 0

		imgObjectResized = None

		if isinstance(objImgObject, str):
			if (objImgObject in self.dicImages):
				imgObjectResized = pygame.transform.scale(self.dicImages[objImgObject], (intDimW,intDimH))
		else:
			imgObjectResized = pygame.transform.scale(objImgObject, (intDimW,intDimH))

		if (intRotate > 0):
			intImgWidth, intImgHeight = imgObjectResized.get_size()
			imgObjectResized = pygame.transform.rotate(imgObjectResized, intRotate)
			intImgWidthAfter, intImgHeightAfter = imgObjectResized.get_size()
			intOffsetWidth = (intImgWidth - intImgWidthAfter) / 2
			intOffsetHeight = (intImgHeight - intImgHeightAfter) / 2

		if (alpha != 255):
			if (alpha > 255 or alpha < 0):
				alpha = 255
			else:
				imgObjectResized.set_alpha(alpha)

		self.screen.blit(imgObjectResized, (self.decOffsetWidth + (intOffsetX*self.decScaleGame)+intOffsetWidth, self.decOffsetHeight + (intOffsetY*self.decScaleGame) + intOffsetHeight))


	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# Create a function to draw a sentence using a font reference
	# This function honors the scale

	def drawSentence(self, strFontObject, strSentence, intOffsetX, intOffsetY, strColor="white"):
		if (strColor not in self.colors):
			strColor = "white"

		if (strFontObject in self.dicFonts):
			imgConvertFont = self.dicFonts[strFontObject].render(self.dicFonts[strFontObject+"_src_ref"], True, self.colors[strColor])
			rectImage = imgConvertFont.get_rect()
			sizeImage = (rectImage.width, rectImage.height)
			srfConvertFont = pygame.Surface(sizeImage)
			srfConvertFont.blit(imgConvertFont,(0,0))
			self.drawImage(srfConvertFont, intOffsetX, intOffsetY, rectImage.width, rectImage.height)

			# self.screen.blit(imgConvertFont, (20, 20))

	def displayClear(self):
		self.screen.fill(self.colors["black"])
	
	def displayUpdate(self):
		pygame.display.update()
	
	def checkKeyDown(self, keyCode):
		if (keyCode in self.dicKeyDown):
			return self.dicKeyDown[keyCode]
		else:
			return False

	def getKeyPressed(self):
		if (self.queKeyPressedQueue.qsize() > 0):
			return self.queKeyPressedQueue.get()

	def clearKeyPressed(self):
		self.queKeyPressedQueue.queue.clear()

	def saveData(self,strData,strFilePath):
		bytesData = strData.encode("ascii")
		base64Data = base64.b64encode(bytesData)
		base64String = base64Data.decode("ascii")
		hdlFile = open(strFilePath, "w")
		hdlFile.write(base64String)
		hdlFile.close()

	def loadData(self,strFilePath):
		#check if file is present
		if os.path.isfile(strFilePath):
			
			hdlFile = open(strFilePath, "r")
			base64Data = hdlFile.read()
			hdlFile.close()
			bytesData = base64Data.encode("ascii")

			base64String = base64.b64decode(bytesData)
			strData = base64String.decode("ascii")

			return strData
		return ""

	def drawRect(self, intX1, intY1, intX2, intY2, lstRGBValue):
		# Initialing Color
		color = lstRGBValue


		# print("Rect : " + str(intX1) + ", " + str(intY1) + ", " + str(intX2) + ", " + str(intY2))
		# print("Scale: :" + str(self.decScaleGame))
		# print("Offsets: x: " + str(self.decOffsetWidth) + " y: " + str(self.decOffsetHeight))
		# print("Rect : " + str(intX1*self.decScaleGame) + ", " + str(intY1*self.decScaleGame) + ", " + str(intX2*self.decScaleGame) + ", " + str(intY2*self.decScaleGame))

		# Drawing Rectangle
		pygame.draw.rect(self.screen, color, pygame.Rect(int((self.decOffsetWidth + (intX1*self.decScaleGame))),int((self.decOffsetHeight + (intY1*self.decScaleGame))), int( (intX2*self.decScaleGame)), int((intY2*self.decScaleGame))))

	# 
	def processEvents(self):
		blnContinue = True
		for event in pygame.event.get():

			if event.type == QUIT:
				blnContinue = False

			elif event.type == pygame.KEYDOWN:
				self.dicKeyDown[event.key] = True

			elif event.type == pygame.KEYUP:
				if (self.dicKeyDown[event.key] == True):
					
					if (self.queKeyPressedQueue.qsize() > self.intPressedQueueSize - 1):
						self.queKeyPressedQueue.get()

					self.queKeyPressedQueue.put(event.key)
				
				self.dicKeyDown[event.key] = False

			elif event.type == VIDEORESIZE:
				self.resizeDisplay()
		return blnContinue
	
class clsSimpleTimer:
    
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()

    def resetTimer(self):
        self.start_ticks = pygame.time.get_ticks()
    
    def checkTimePassed(self, intMsCheck):
        
        intMsPassed = (int(pygame.time.get_ticks()) - int(self.start_ticks))
        
        if (intMsPassed > intMsCheck):
            return True
        else:
            return False

		
