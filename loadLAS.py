from laspy.file import File
import numpy as np

def loadLAS(path):

	lasFile = File(path, mode='r')

	# Get offset value
	offset = lasFile.header.offset
	x_offset = offset[0] 
	y_offset = offset[1]
	z_offset = offset[2]

	xs = lasFile.X/100.0 + x_offset
	ys = lasFile.Y/100.0 + y_offset
	zs = lasFile.Z/100.0 + z_offset

	points = np.vstack( (xs, ys) )
	points = np.vstack( (points, zs) ) 
	points = points.T

	return points