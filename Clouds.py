from math import cos, pi
from noise import SimplexNoiseGen
from threading import Thread
from Queue import Queue
from time import time
import Config

class ObjectManager(object):
	def __init__(self, ObjectClass):
		self.Object = {}
		self.ObjectClass = ObjectClass

	def GetObject(self, X):
		if self.Object.has_key(X):
			return self.Object[X]

		Obj = self.ObjectClass(X, self)
		self.Object[X] = Obj

		return Obj

class CloudManager(ObjectManager):
	def __init__(self, CloudClass = None):
		self.Noise = SimplexNoiseGen(Config.Seed)

		if CloudClass == None:
			CloudClass = CloudChunk
		super(CloudManager, self).__init__(CloudClass)


class CloudChunk(object):
	def __init__(self, XPos, Generator):
		self.X = XPos
		self.Noise = Generator.Noise
		self.Generator = Generator

		self.Finished = False

		T = Thread(target=self.Generate)
		T.daemon = True
		T.start()

	def Generate(self):
		print "Starting Generation at",self.X
		start = time()
		Points = []
		Colours = []
		Length = 0

		#Generation stuff
		PixelSize = Config.PixelSize

		YOffset = Config.CloudHeight / 2.0

		Noise = self.Noise
		NoiseOffset = Config.NoiseOffset

		for X in xrange(0, Config.CloudWidth - 1, PixelSize):
			XOff = X+self.X

			for Y in xrange(0, Config.CloudHeight, PixelSize):
				Points.append(XOff)
				Points.append(Y)

				Colours.append(1)
				Colours.append(1)
				Colours.append(1)

				#Get noise, round and clamp
				NoiseGen = Noise.fBm(XOff, Y) + NoiseOffset
				NoiseGen = max(0, min(1, NoiseGen))
				
				# Fade around the edges - use cos to get better fading
				Diff = abs(Y - YOffset) / YOffset
				NoiseGen *= cos(Diff * pi / 2)
				
				Colours.append(NoiseGen)

				Length += 1

		#Assign variables
		self.Points = Points
		self.Colours = Colours
		self.Length = Length

		print "Finished Generation at", self.X
		print "\tTook",time() - start
		self.Finished = True

	def GenerateFinshed(self):
		pass
		

	def Draw(self):
		if self.Finished:
			self.Finished = False
			self.GenerateFinshed()
