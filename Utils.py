# Third-party packages
import pyglet
from pyglet.gl import *

# Define a simple function to create ctypes arrays of floats:
def vec(*args):
	"""Creates GLfloat arrays of floats"""
	return (GLfloat * len(args))(*args)


# fast math algorithms
class FastRandom(object):
	def __init__(self, seed):
		self.seed = seed

	def randint(self):
		self.seed = (214013 * self.seed + 2531011)
		return (self.seed >> 16) & 0x7FFF