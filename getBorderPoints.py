from laspy.file import File
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
from mpl_toolkits import mplot3d

def getBorderPoints():

	path = raw_input("Input file path: ")
	# lasFile = File('/home/linche/Desktop/Foresight/ROS/0615_las_test/1648443908000pcdboardSeg.las', mode='r')
	lasFile = File(path, mode='r')

	##############Getting all border points################
	# Look at what laser_id values there are and store in a list
	readDic = {}
	for idNum in lasFile.pt_src_id:
		readDic[idNum] = 1
	idList = readDic.keys()

	# Build a dictionary with laser_id as keys and a list of cloud point indices as values
		# Initialize dictionary
	idDic = {}
	for i in range(len(idList)):
		idDic.setdefault(idList[i], [])

		# Store cloud points in their repective laser_ids
	for i in range(len(lasFile.pt_src_id)):
		idDic[ lasFile.pt_src_id[i] ].append(i)

	# Get timestamp of each point in each laser_id and select out the min and max indices
		# Initialize output array: Nx2 -> N id channels, 2 columns corresponding to min, max
	borderPointIdx = np.zeros( (len(idList), 2) )
	for i in range(len(idList)): # for each laser_id
		idx = idDic[ idList[i] ] # the index of points in a given laser_id
		ts_vals = lasFile.gps_time[idx]
		# print("ts_vals: ")
		# print(ts_vals)
		min_idx = np.argmin(ts_vals)
		max_idx = np.argmax(ts_vals)
		borderPointIdx[i, 0] = idx[min_idx]
		borderPointIdx[i, 1] = idx[max_idx]

	print("borderPointIdx: ")
	print(borderPointIdx)

	borderPointIdx = borderPointIdx.flatten()
	borderPointIdx = borderPointIdx.astype(int)

	offset = lasFile.header.offset
	x_offset = offset[0] 
	y_offset = offset[1]
	z_offset = offset[2]

	xs_border = lasFile.X[borderPointIdx]/100.0 + x_offset
	ys_border = lasFile.Y[borderPointIdx]/100.0 + y_offset
	zs_border = lasFile.Z[borderPointIdx]/100.0 + z_offset

	borderPoints = np.vstack((xs_border,ys_border))
	borderPoints = np.vstack((borderPoints,zs_border))
	borderPoints = borderPoints.T

	print("borderPoints.shape: ")
	print(borderPoints.shape)

	return borderPoints


if __name__ == '__main__':
	borderPoints = getBorderPoints()

	fig1 = pylab.figure(1)
	ax = mplot3d.Axes3D(fig1)
	# max_range = np.array([xs_border.max()-xs_border.min(), ys_border.max()-ys_border.min(), zs_border.max()-zs_border.min()]).max() / 2.0
	max_range = np.array([borderPoints[:,0].max()-borderPoints[:,0].min(), borderPoints[:,1].max()-borderPoints[:,1].min(), borderPoints[:,2].max()-borderPoints[:,2].min()]).max() / 2.0
	mid_x = (borderPoints[:,0].max()+borderPoints[:,0].min()) * 0.5
	mid_y = (borderPoints[:,1].max()+borderPoints[:,1].min()) * 0.5
	mid_z = (borderPoints[:,2].max()+borderPoints[:,2].min()) * 0.5
	ax.set_xlim(mid_x - max_range, mid_x + max_range)
	ax.set_ylim(mid_y - max_range, mid_y + max_range)
	ax.set_zlim(mid_z - max_range, mid_z + max_range)
	ax.scatter3D(borderPoints.T[0], borderPoints.T[1], borderPoints.T[2], color='b', marker='.')
	# ax.scatter3D(lr_data[:,0], lr_data[:,1], lr_data[:,2], color='r', marker='.')
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.set_aspect('equal')
	pylab.show()