import os
import subprocess
import numpy as np
import cv2
import sys

class shot:
	startPath = 0
	endPath = 0
	matchingPickedPath = ""

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def matchingScore(output,num):
	scoreM = 0.0
	maxVal = 0.0
	cnt = 0
	for line in output:
		line = line.split()
		if not line or len(line)!=6 or not line[0][0].isdigit():  continue
		x0, y0, x1, y1, score, index = line

		if(float(score) > maxVal):
			maxVal = float(score)

		scoreM = scoreM + float(score)
		cnt = cnt + 1

	scoreM = scoreM/(num*maxVal)
	return scoreM


path1 = "input/"    #video frames path
path2 = "input/in000001.jpg"   #image path 

# template image
image = cv2.imread(path2)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
height, width = image.shape
numberOfPatches = height*width/16

listing = sorted(os.listdir(path1))    

im1 = image
frames=[]

files = len(listing)
cnt=0
for index, file in enumerate(listing):
	if(index==0):
		im1 = cv2.imread(path1+file)
		im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
	else:
		im2 = cv2.imread(path1+file)
		im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

		diff = mse(im2,im1)
		#print path1+file
		#print diff

		if index == (files-1):
			index = index+1
		if(diff > 15.0 or index==files):
			print "Shot from "+ str(cnt)+" to "+ str(index-1) #boundary

			frame=shot()
			frame.startPath = cnt
			frame.endPath = (index-1)
			frame.matchingPickedPath = path1+listing[(cnt+index-1)/2]

			frames.append(frame)

			cnt = index
		'''else:
			#not a boundary, move
			print "not a boundary"'''

		im1=im2

#video-writer
'''height, width = im1.shape
fourcc = cv2.cv.CV_FOURCC(*'mp4v') # Be sure to use lower case
out = cv2.VideoWriter('result.mp4', fourcc, 20.0, (width, height))'''

for f in frames:
	print f.matchingPickedPath

for f in frames:
	#cmd = './deepmatching-static climb1.png climb2.png'
	print " "
	print "Matching: " + f.matchingPickedPath
	cmd = './deepmatching-static '+ f.matchingPickedPath + ' ' + path2

	output = subprocess.check_output(cmd, shell=True)
	output = output.split('\n')

	score = matchingScore(output,numberOfPatches)
	if(score >= 0.15):
		print "Match found with score: " + str(score)