HasPyglet = True

try:
	import pyglet
except ImportError:
	HasPyglet = False

if HasPyglet:
	print "Using Pyglet"
	import PygletCore
else:
	print "Install Pyglet or Pygame to run"