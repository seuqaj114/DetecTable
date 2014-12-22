import numpy as np 
import Image, ImageDraw,ImageFilter
import sys
import matplotlib.pyplot as pyplot
import time

import kmeans
from kmeans import get_threshold_dots

"""
Steps: 
	- expand values to full range
	- crop around table
	- increase contrast
	- further contrast (to binary)
	- downsample
	- find clusters

To do:
	- remove noise before cropping around table
	- consider if abs is usefull, if negative minimum of slope can be used for cell cropping

Na obtencao dos digitos a partir das zonas, decidir o que e digito ou nao a partir nao so do threshold
mas tambem do desvio em sigmas

test_digit = table_rec.reformat_image(digits[2]).resize((28,28))
test_pic = np.array([(255-t[0])/255.0 for t in test_digit.getdata()]).reshape((784,1))
net.feedforward(test_pic)

"""

def classify(image,net):
	test_digit = reformat_image(image).resize((28,28))
	test_pic = np.array([(255-t[0])/255.0 for t in test_digit.getdata()]).reshape((784,1))
	res = net.feedforward(test_pic)

	return res, np.argmax(res)

def func(item):
	return len(item[0])

def image_to_matrix(image):
	"""
		Receives an image and returns its numpy matrix representation,
		with correct height and width.
		The returned matrix is is grayscale 0-255.
	"""

	pic = np.array([t[0] for t in image.getdata()]).reshape(image.size[1],image.size[0])

	return pic

def reformat_image(image):
	blank = Image.new("RGB",map(int,(image.size[1]*1.1,image.size[1]*1.1)),(255,255,255)).convert("LA")

	blank.paste(image,(blank.size[0]/2-image.size[0]/2,blank.size[1]/2-image.size[1]/2))

	return blank

def get_digits(image,threshold=3):
	"""
		Receives a cell and returns its isolated digits.
	"""

	vertical_digits = get_vertical_digits(image,threshold)

	digits = []
	for vertical_digit in vertical_digits:
		new_digit = get_digit_from_vertical_digit(vertical_digit,0)
		digits.append(new_digit)

	return digits

def get_digit_from_vertical_digit(image,threshold=3):

	spec = row_spectrum(image,threshold)
	zones = get_zones(spec,1,True,threshold)

	digit_zone = max(zones,key=func)
	#print digit_zone

	image.crop((0,digit_zone[1],image.size[0],digit_zone[1]+len(digit_zone[0]))).show()

	return image.crop((0,digit_zone[1],image.size[0],digit_zone[1]+len(digit_zone[0])))

def get_vertical_digits(image,threshold=3):
	
	spec = column_spectrum(image,threshold)

	zones = get_zones(spec,1,True,threshold)

	vertical_digits = []
	for zone in zones:
		#print zone
		#print (zone[1]-len(zone[0]),0,zone[1],image.size[1])
		vertical_digit = image.crop((zone[1],0,zone[1]+len(zone[0]),image.size[1]))
		vertical_digits.append(vertical_digit)

	return vertical_digits

def get_relevant_zones(array,threshold=3):
	"""
		Returns only the elements of array whose len(item[0])>threshold.
		array must be the return of get_same_kind_set
	"""

	return [item for item in array if len(item)>3]


def get_zones(array,kind,relevant=False,threshold=3):
	"""
		Returns that resulting_set of tuples that contain an array which is a consecutive set
		of entry's matching kind and the location of the first entry in the set.
	"""

	resulting_set=[]

	i=0
	if array[i]==kind:
		count=1
	else:
		count=0

	while i<len(array):
		
		if array[i]==kind:
			count+=1
		elif array[i]!=kind and array[i-1]==kind:
			resulting_set.append(([kind]*count,i-count))
			count=0
		else:
			pass

		i+=1

	if count>0:
		resulting_set.append(([kind]*count, i-count))

	if relevant == False:
		return resulting_set
	else:
		return [item for item in resulting_set if len(item[0])>threshold]

def column_spectrum(image,threshold=3):
	"""
		Receives an image and uses its matrix representation to allow horizontal probing.

		It goes through the columns and:
		- Removes columns that have less than threshold black pixels;
		- Removes groups of columns that have less than threshold adjacent pixels;
	"""

	pic = image_to_matrix(image).transpose()

	spec = [0]*len(pic)

	for i in range(len(pic)):
		if len(filter(lambda x:x==0,pic[i])) > threshold:
			spec[i]=1

	return spec

def row_spectrum(image,threshold=3):
	"""
		Receives an image and uses its matrix representation to allow horizontal probing.

		It goes through the columns and:
		- Removes columns that have less than threshold black pixels;
		- Removes groups of columns that have less than threshold adjacent pixels;
	"""

	pic = image_to_matrix(image)

	spec = [0]*len(pic)

	for i in range(len(pic)):
		if len(filter(lambda x:x==0,pic[i])) > threshold:
			spec[i]=1

	return spec



def get_cell(ROWS,COLS,dims):

	"""
		dims is a tuple like 
		(top_left_corner_x,top_left_corner_y,bottom_right_corner_x,bottom_right_corner_y)
	"""

	print "rows: %s; columns: %s" % (ROWS,COLS)

	main_image = Image.open("../fig/table.jpg").convert("LA")
	
	croped_image = main_image.crop(dims)
	croped_image.show()

	#	Set the search rectangle's geometry
	BASE_WIDTH = croped_image.size[0]/COLS
	BASE_HEIGHT = croped_image.size[1]/ROWS
	RECT_CENTER = (BASE_WIDTH/2,BASE_HEIGHT/2)

	#	Run ever smaller rectangles over a cell to isolate the number
	#	Using height as reference!
	croped_cells = []
	for i in range(ROWS):
		for j in range(COLS):
			#	Set the search limits
			WIDTH_MIN = j*croped_image.size[0]/COLS
			WIDTH_MAX = croped_image.size[0]/COLS + j*croped_image.size[0]/COLS
			HEIGHT_MIN = i*croped_image.size[1]/ROWS
			HEIGHT_MAX = croped_image.size[1]/ROWS + i*croped_image.size[1]/ROWS

			#	Apply gaussian threshold to cell
			cell = croped_image.crop((WIDTH_MIN,HEIGHT_MIN,WIDTH_MAX,HEIGHT_MAX))
			cell_pic = np.array([t[0] for t in cell.getdata()])

			MEAN = np.mean(cell_pic)
			STD = np.std(cell_pic)

			cell = cell.point(lambda x: 0 if x <= MEAN-1.5*STD else 255)
			cell.show()

			#	Set cell's ratio ( > 0 ) for number search
			RECT_RATIO = float(BASE_WIDTH)/BASE_HEIGHT

			#	Search cicle, rectangles from outside to center
			cell_count_array = []
			for inc in range((BASE_HEIGHT/2)/2):
				croped_cell = cell.crop(map(int,(
					RECT_CENTER[0]-(BASE_WIDTH/2-inc*RECT_RATIO),
					RECT_CENTER[1]-(BASE_HEIGHT/2-inc),
					RECT_CENTER[0]+(BASE_WIDTH/2-inc*RECT_RATIO),
					RECT_CENTER[1]+(BASE_HEIGHT/2-inc)
					)))
				#if inc%5 == 0:
				#	croped_cell.show()
				croped_cell_pic = [t[0] for t in croped_cell.getdata()]
				cell_count_array.append(croped_cell_pic.count(0))

			#	Find minimum of number of pixels rate of change
			cell_slope_array = [abs(cell_count_array[k]-cell_count_array[k-1]) for k in range(1,len(cell_count_array))]
			cell_height = cell_slope_array.index(min(cell_slope_array))

			#	Get croped cell (final)
			croped_cell = cell.crop(map(int,(
					RECT_CENTER[0]-(BASE_WIDTH/2-cell_height*RECT_RATIO),
					RECT_CENTER[1]-(BASE_HEIGHT/2-cell_height),
					RECT_CENTER[0]+(BASE_WIDTH/2-cell_height*RECT_RATIO),
					RECT_CENTER[1]+(BASE_HEIGHT/2-cell_height)
					)))	

			#croped_cell.show()
			croped_cells.append((cell,croped_cell))
			#croped_cell.filter(ImageFilter.SMOOTH).show()
			
	return croped_cells


def get_optimal_clusters(cell,threshold=140):
	"""
		This function receives an Image object and returns the optimal
		number of clusters, representing number of digits.

		Method: find the number of clusters for which the average of the
				variances is minimum.

		Number of clusters limited to 7 so far, to avoid having to use optimization.
	"""

	#	Turn image to numpy array
	pic = image_to_matrix(cell)

	#	Get the array of coordinates of dark dots
	dots = get_threshold_dots(pic,threshold)

	scores = []

	for n_clusters in range(1,10):
		clusters = kmeans.kmeans(pic,pic.shape[0],pic.shape[1],50,n_clusters,threshold)
		print clusters

		square_sum_array = [0]*n_clusters
		count_array = [0]*n_clusters

		for dot in dots:
			distance_array = [kmeans.euclid_distance(dot,cluster) for cluster in clusters]
			min_index = distance_array.index(min(distance_array))
			square_sum_array[min_index] += kmeans.euclid_distance(clusters[min_index],dot)
			count_array[min_index] += 1

		variances = [square_sum/(count+0.001) for square_sum, count in zip(square_sum_array,count_array)]

		print variances
		scores.append(sum(variances)/len(variances))

	return scores










	