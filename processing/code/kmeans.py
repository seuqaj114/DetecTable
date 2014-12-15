import numpy as np
from random import random
import sys
from math import sqrt

def get_threshold_dots(pic,threshold):
	"""
		Get the array of coordinates of dots below threshold
	"""

	dots = []
	for i in range(len(pic)):
		for j in range(len(pic[i])):
			if pic[i][j] < threshold:
				dots.append([i,j])

	return np.array(dots)


def euclid_distance(x1,x2):
	#	x1 and x2 must be array-like objects
	return sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)

def kmeans(image,width,height,epochs,clusters=None,threshold=140):

	if type(width) != int or type(height) != int:
		return "ERROR - width and height must be integers!"

	image = np.array(image)

	dots = []
	for i in range(len(image)):
		for j in range(len(image[i])):
			if image[i][j] < threshold:
				dots.append([i,j])

	print "Dots: %s" % (len(dots))

	if not clusters:
		n_clusters = width*height
	else:
		n_clusters = clusters

	clusters = [[random()*width,random()*height] for i in range(n_clusters)]
	#clusters = [[image.shape[0]/(n_clusters+1)*(i+1),image.shape[1]/2] for i in range(n_clusters)]

	for j in range(epochs):
		#print j
		location_array = np.array([[0,0]]*n_clusters)
		count_array = [0]*n_clusters

		for dot in dots:
			distance_array = [euclid_distance(dot,cluster) for cluster in clusters]
			min_index = distance_array.index(min(distance_array))
			location_array[min_index] += np.array(dot)
			count_array[min_index] += 1
			#print count_array

		clusters = [location/count for location, count in zip(location_array,count_array)]

	return clusters


def horizontal_kmeans(image,width,height,epochs,clusters=None):

	"""
		image must be a width x height matrix, in standard grayscale 0-255
	"""

	if type(width) != int or type(height) != int:
		return "ERROR - width and height must be integers!"

	image = np.array(image)

	dots = []
	for i in range(len(image)):
		for j in range(len(image[i])):
			if image[i][j] < 140:
				dots.append([i,j])

	dots = [[x[0],height/2] for x in dots]

	print "Dots: %s" % (len(dots))

	if not clusters:
		n_clusters = width*height
	else:
		n_clusters = clusters

	clusters = [[width/n_clusters/2+i*width/n_clusters,height/2] for i in range(n_clusters)]

	for j in range(epochs):
		print j
		location_array = np.array([[0,0]]*n_clusters)
		count_array = [0]*n_clusters

		for dot in dots:
			distance_array = [euclid_distance(dot,cluster) for cluster in clusters]
			min_index = distance_array.index(min(distance_array))
			location_array[min_index] += np.array(dot)
			count_array[min_index] += 1
			#print count_array

		clusters = [location/count for location, count in zip(location_array,count_array)]

	return clusters

def horizontal_flat_kmeans(image,width,height,epochs,clusters=None):

	"""
		image must be a width x height matrix, in standard grayscale 0-255
	"""

	if type(width) != int or type(height) != int:
		return "ERROR - width and height must be integers!"

	image = np.array(image)

	dots = []
	for i in range(len(image)):
		for j in range(len(image[i])):
			if image[i][j] < 140:
				print "%s,%s" % (i,j)
				dots.append([i,j])

	dots = [[x[0],height/2] for x in dots]
	#print dots

	flat_dots=[]
	for x in dots:
		if x not in flat_dots:
			flat_dots.append(x)

	print "Dots: %s" % (len(flat_dots))
	print flat_dots

	if not clusters:
		n_clusters = width*height
	else:
		n_clusters = clusters

	clusters = [[width/n_clusters/2+i*width/n_clusters,height/2] for i in range(n_clusters)]

	for j in range(epochs):
		print j
		location_array = np.array([[0,0]]*n_clusters)
		count_array = [0]*n_clusters

		for dot in flat_dots:
			distance_array = [euclid_distance(dot,cluster) for cluster in clusters]
			min_index = distance_array.index(min(distance_array))
			location_array[min_index] += np.array(dot)
			count_array[min_index] += 1
			#print count_array

		clusters = [location/count for location, count in zip(location_array,count_array)]

	return clusters
