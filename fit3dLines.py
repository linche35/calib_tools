import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as m3d

# def getLineEquation(pointCloud):
def getLineEquation(pointCloud):
# # Params: pointCloud -> Point cloud of one side of the board
# # Returns: The 3D line equation fitted by SVD (the line is the best approximation in a least squared sense)

	data = pointCloud

	# Calculate the mean of the points, i.e. the 'center' of the cloud
	datamean = data.mean(axis=0)

	# Do an SVD on the mean-centered data.
	uu, dd, vv = np.linalg.svd(data - datamean)

	# Now vv[0] contains the first principal component, i.e. the direction
	# vector of the 'best fit' line in the least squares sense.
	linepts = vv[0] * np.mgrid[-7:7:2j][:, np.newaxis]

	# shift by the mean to get the line in the right place
	linepts += datamean

	a = vv[0][1]
	b = - (vv[0][0] + vv[0][2])
	c = vv[0][1]
	d = vv[0][1]*datamean[0] + (-(vv[0][0] + vv[0][2]))*datamean[1] + vv[0][1]*datamean[2]

	# ax + by + cz = d
	l = np.asarray([a,b,c,d])
	return l, vv[0], datamean

def getCornerCoordinates(pointCloud1, pointCloud2):
	l_1,d_1,A_1 = getLineEquation(pointCloud1)
	l_2,d_2,A_2 = getLineEquation(pointCloud2)


	delta_matrix = np.asarray([[np.inner(d_1, d_1), np.inner(d_1,d_2)], 
						[np.inner(d_1, d_2), np.inner(d_2,d_2)]])

	delta_t1_matrix = np.asarray([[np.inner(A_2-A_1, d_1), np.inner(d_1,d_2)], 
						  [np.inner(A_2-A_1, d_2), np.inner(d_2,d_2)]])

	delta_t2_matrix = np.asarray([[np.inner(d_1, d_1), np.inner(d_1,A_1-A_2)], 
						  [np.inner(d_1, d_2), np.inner(d_2,A_1-A_2)]])

	delta = np.linalg.det(delta_matrix)
	delta_t1 = np.linalg.det(delta_t1_matrix)
	delta_t2 = np.linalg.det(delta_t2_matrix)

	B1 = A_1 + (delta_t1/delta)*d_1
	B2 = A_2 + (delta_t2/delta)*d_2

	cornerCoord = (B1 + B2)/2

	return cornerCoord, d_1, A_1, d_2, A_2

if __name__ == '__main__':
	getCornerCoordinates()