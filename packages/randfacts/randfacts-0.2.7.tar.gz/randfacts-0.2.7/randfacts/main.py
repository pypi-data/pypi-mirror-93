from random import randint
import os
version = "0.2.7" # NOTE: REMEMBER TO CHANGE VERSION HERE

def getFact(filter=True):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(dir_path, "safe.txt")) as f:
		safelist = [fact.rstrip() for fact in f.readlines()]
	with open(os.path.join(dir_path, "unsafe.txt")) as f:
		unsafelist = [fact.rstrip() for fact in f.readlines()]
	if filter == False:
		safelist += unsafelist
	return safelist[randint(0, len(safelist) - 1)]

def getVersion():
	return version
