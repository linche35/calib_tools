import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from laspy.file import File
from matplotlib import pylab
from mpl_toolkits import mplot3d
from ransac import *
from fit3dLines import *
from ePnP import *


from getBorderPoints import *
from loadLAS import *

# 1. load side points
# 2. get corner coordinates
# 3. run ePnP


# Controls
showRawData =  not False

useProjectedBorderPoints =  True
useRawBorderPoints = not useProjectedBorderPoints

showProjectedBorderPoints = useProjectedBorderPoints
showRawBorderPoints = not showProjectedBorderPoints

viewRansacPlane = not True

if viewRansacPlane:
	useProjectedBorderPoints = True
	useRawBorderPoints = False
	showProjectedBorderPoints = True
	showRawBorderPoints = False
	showRawData = True


# ransac
def augment(xyzs):
	axyz = np.ones((len(xyzs), 4))
	axyz[:, :3] = xyzs
	return axyz

def estimate(xyzs):
	axyz = augment(xyzs[:3])
	return np.linalg.svd(axyz)[-1][-1, :]

def is_inlier(coeffs, xyz, threshold):
	return np.abs(coeffs.dot(augment([xyz]).T)) < threshold

def plot_plane(a, b, c, d, xlim, ylim):
		xx, yy = np.meshgrid(np.arange(xlim[0], xlim[1]), np.arange(ylim[0], ylim[1]))
		return xx, yy, (-d - a * xx - b * yy) / c

def getProjected3DCoord(points, plane_fit):
	origin = np.asarray([0,0,-(plane_fit[3]/plane_fit[2])] ) 

	output = np.zeros(points.shape)

	for i in range(points.shape[0]):
		v = points[i] - origin
		normal = np.asarray([plane_fit[0], plane_fit[1], plane_fit[2]])
		normal = normal / np.linalg.norm(normal)
		dist = np.inner(v, normal)
		projected_point = points[i] - dist*normal

		output[i] = projected_point
	return output

# Reads a .las file containing all 3D points on the board
# Note that there is an offset for all points if the .las file is cropped out in cloud compare

# load points
path = raw_input("Input board file path: ")
data = loadLAS(path)

xs = data[:,0]
ys = data[:,1]
zs = data[:,2]

fig1 = pylab.figure(1)

ax = mplot3d.Axes3D(fig1)


# ransac
n = data.shape[0]
max_iterations = 200
goal_inliers = n * 0.8

# test data
xyzs = data

if showRawData:
	# plot data
	ax.scatter3D(xyzs.T[0], xyzs.T[1], xyzs.T[2], color='b', marker='.')



# Setting up display
max_range = np.array([xs.max()-xs.min(), ys.max()-ys.min(), zs.max()-zs.min()]).max() / 2.0
mid_x = (xs.max()+xs.min()) * 0.5
mid_y = (ys.max()+ys.min()) * 0.5
mid_z = (zs.max()+zs.min()) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)


# RANSAC
m, b = run_ransac(xyzs, estimate, lambda x, y: is_inlier(x, y, 0.003), 3, goal_inliers, max_iterations)
a, b, c, d = m


# plot plane
xlim = ax.get_xlim() #[xs.min(), xs.max()]
ylim = ax.get_ylim() #[ys.min(), ys.max()]
zlim = ax.get_zlim() #[zs.min(), zs.max()]
xx, yy, zz = plot_plane(a, b, c, d, xlim, ylim)
# ax.plot_surface(xx, yy, zz, color='k')#(0, 1, 0, 0.5))
if showRawData:
	ax.plot_wireframe(xx,yy,zz, color='k')

projectedP = getProjected3DCoord(data, m)
# ax.scatter3D(projectedP[:,0], projectedP[:,1], projectedP[:,2], color='r', marker='.')


# Load side points (Doing this manually for now)
prompt = ["upperLeft", "lowerLeft", "lowerRight", "upperRight"]
borderPoints = []
projectedBoarder = []

for i in prompt:
	path = raw_input("Input " + i + " file path: ")
	pnt = loadLAS(path)
	borderPoints.append( pnt )
	projectedBoarder.append( getProjected3DCoord(pnt, m) )


if useRawBorderPoints:
	borderData = borderPoints
if useProjectedBorderPoints:
	borderData = projectedBoarder


cornerPos = ['Left', 'Down', 'Right', 'Up']

cornerFile = open("cornerFile.txt","w")

prjCorners = []
rawCorners = []
# using projected side points
for i in range(4):
	if i == 3:
		corner, d1, A1, d2, A2 = getCornerCoordinates(borderData[3], borderData[0])
	else:
		corner, d1, A1, d2, A2 = getCornerCoordinates(borderData[i], borderData[i+1])
	
	prjCorners.append(corner)

	ul_linepts = d1 * np.mgrid[-0.5:0.5:20j][:, np.newaxis]
	ul_linepts += A1
	ll_linepts = d2 * np.mgrid[-0.5:0.5:20j][:, np.newaxis]
	ll_linepts += A2

	# plot lines
	ax.plot3D(*ul_linepts.T)
	ax.plot3D(*ll_linepts.T)

	# plot corner
	ax.scatter3D(corner[0], corner[1], corner[2], color = 'g', marker='s', s=40, label="ransac")

	# print corner coordinates
	print(cornerPos[i] + " corner: ")
	np.set_printoptions(precision=8, suppress=True)
	print(corner)
	corner = np.expand_dims(corner,axis=1)
	cornerFile.write(str(corner))
	cornerFile.write("\n")
cornerFile.close()

# using raw side points
borderData = borderPoints
for i in range(4):
	if i == 3:
		corner, d1, A1, d2, A2 = getCornerCoordinates(borderData[3], borderData[0])
	else:
		corner, d1, A1, d2, A2 = getCornerCoordinates(borderData[i], borderData[i+1])
	
	rawCorners.append(corner)

	ul_linepts = d1 * np.mgrid[-0.5:0.5:20j][:, np.newaxis]
	ul_linepts += A1
	ll_linepts = d2 * np.mgrid[-0.5:0.5:20j][:, np.newaxis]
	ll_linepts += A2

	# plot lines
	ax.plot3D(*ul_linepts.T)
	ax.plot3D(*ll_linepts.T)

	# plot corner
	ax.scatter3D(corner[0], corner[1], corner[2], color = 'r', marker='s', s=40, label="raw")

	# print corner coordinates
	print(cornerPos[i] + "corner: ")
	np.set_printoptions(precision=8, suppress=True)
	print(corner)

# compare error of 2 corner calculation methods
prj = np.asarray(prjCorners)
raw = np.asarray(rawCorners)
err = []
for i in range(len(prjCorners) ):
	err.append(np.linalg.norm(prj[i] - raw[i]))
print("\nThe error between raw corners and projected corners is: ")
print err



ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# print "Line equation: " + "%f x + %f y + %fz + %f = 0" % (a, b, c, d)


ax.set_aspect('equal')

print
print("[R|t]:")
# print(Rt)
np.set_printoptions(precision=8, suppress=True)
for i in range(Rt.shape[0]):
	print(Rt[i])

objMat = np.squeeze(objectPoints, axis=2) # objectPoints is in ePnP.py #shape is 8x2 after np.squeeze

imgMat = np.squeeze(imagePoints, axis=2)  # imagePoints is in ePnP.py  #shape is 8x2 after np.squeeze

reprojected = cv2.projectPoints(objMat, rvec, tvec, cameraMatrix, distCoeffs)

reprojectionCoords = np.squeeze(reprojected[0], axis=1)

error = reprojectionCoords - imgMat
eachError = np.linalg.norm(error, axis=1)
avgError = np.average(eachError)


for i in range(imgMat.shape[0]/4):
	plt.figure(10 + i)
	plt.title('img ' + str(i) )
	plt.scatter(imgMat[4*i:4*i+4, 0], imgMat[4*i:4*i+4, 1], label='Image Coordinate')
	plt.scatter(reprojectionCoords[4*i:4*i+4, 0], reprojectionCoords[4*i:4*i+4, 1], label='Reprojected Coordinate')
	plt.xlim((0,6000))
	plt.ylim((0,4000))
	plt.legend()
	avgError = np.average(eachError[4*i:4*i+4])
	plt.text(1000,500,"Average error: " + str(avgError) + " pixels", fontsize=15)

ax.legend()
pylab.show()