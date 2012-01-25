#Heith Seewald 2012
# just proof of concept to embed metadata indo openEXR files from maya... needs cleaning...

#IMPORTS
from pymel.core import *
import basicStats
import os,sys
import OpenEXR
import Imath
import shutil


# Get the absolute path of the Desktop...
hsHome = os.path.expanduser("~/Desktop")

#The fold
exrPath = '%s/exrTests/' % (hsHome)

#Why am I doing this next part? I can't remember... sad.
oldDir = os.getcwd()
hsDir = os.chdir(exrPath)


#create an object for the default mental ray options...
hsRend = PyNode("miDefaultOptions")

#grab some attributes.... (just but this in here for example, it should pull from database)
maxSamp = hsRend.maxReflectionRays.get()
maxRefl = hsRend.maxRefractionRays.get()



start = timerX() #We're going to time the render to embed into the EXR... this 'starts' it
renderedFile = Mayatomr( preview=True, v=0, camera='perspShape' ) #Kick off the render...
totalTime = timerX(startTime=start) # figure out the time and load it into totalTime
#print "Total time: ", totalTime

#extremely poor choice for var name... 
hshs = maxSamp

#shell utilities... let me know if there is a better way... this works for now.
shutil.copy(renderedFile, 'FROM_MAYA.exr')


infile = OpenEXR.InputFile("FROM_MAYA.exr")#This is the raw exr that maya rendered out.
h = infile.header()
channels = h['channels'].keys()
newchannels = dict(zip(channels, infile.channels(channels)))

#Start the EXR injecting... 

h['author'] = "Heith Seewald"
h['renderTime'] = str(totalTime)
h['maxReflection'] = str(maxRefl)
h['maxSamples'] = str(maxSamp)



out = OpenEXR.OutputFile("hsOutMaya_Renderedee_higher.exr", h) #Right out the exr with the metadata
out.writePixels(newchannels)

