import cv2
import numpy as np

lowerLeftAsOrigin = False

imagePoints = np.zeros((8,2,1))
# origin at top left corner
# DSC04422 (img2) order: Up Left Right Down
#Up
imagePoints[0] = [ [2637.0], [1318.0] ]
#Left
imagePoints[1] = [ [2180.0], [2361.0] ]
#Right
imagePoints[2] = [ [3516.0], [1741.0] ]
#Down
imagePoints[3] = [ [2912.0], [2959.0] ]
# DSC04433 (img3)
#Up
imagePoints[4] = [ [2978.0], [1348.0] ]
#Left
imagePoints[5] = [ [2502.0], [2331.0] ]
#Right
imagePoints[6] = [ [3995.0], [1824.0] ]
#Down
imagePoints[7] = [ [3509.0], [2821.0] ]


if lowerLeftAsOrigin:
	temp = imagePoints[1,1,0]
	imagePoints[:,1,:] = 4000.0 - imagePoints[:,1,:]
	print("imagePoints changed from %d to %d" %(temp, imagePoints[1,1,0]))


objectPoints = np.zeros((8,3,1))
# DSC04422 (img2) order: Up Left Right Down
#Up
objectPoints[0] = [ [-0.14397575], [1.74583382], [0.45730083] ] # [-0.14397575], [1.74583382], [0.45730083] not projected
#Left
objectPoints[1] = [ [-0.39424357], [1.88058042], [0.02838033] ] # [-0.39424357], [1.88058042], [0.02838033] not projected
#Right
objectPoints[2] = [ [0.17626824], [1.44518216], [0.24786017] ] # [0.17626824], [1.44518216], [0.24786017] not projected
#Down
objectPoints[3] = [ [-0.02585048], [1.52798301], [-0.20434375] ] # [-0.02585048], [1.52798301], [-0.20434375] not projected

# DSC04433 (img3)
#Up
objectPoints[4] = [ [-0.04426136], [1.8908094], [0.4388457] ] # [-0.04426136], [1.8908094], [0.4388457] not projected
#Left
objectPoints[5] = [ [-0.2040881], [1.88380723], [0.02392199] ] # [-0.2040881], [1.88380723], [0.02392199] not projected
#Right
objectPoints[6] = [ [0.45825793], [1.83634941], [0.27529686] ] # [0.45825793], [1.83634941], [0.27529686] not projected
#Down
objectPoints[7] = [ [0.20627633], [1.83469337], [-0.22166976] ] # [0.20627633], [1.83469337], [-0.22166976] not projected


# Intrinsics
cameraMatrix = np.array([[3996.55856145,		0.0	  , 3036.33424987],
						 [0.0 		   ,3994.99660007 , 1910.90155857],
						 [0.0		   ,		0.0   ,	1.0]])

# Distortion Coefficients
distCoeffs = np.array([[-0.07782397],
					   [0.09337429],
					   [-0.0034919],
					   [0.00104407]])

_, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs, cv2.SOLVEPNP_EPNP)

R_mat = cv2.Rodrigues(rvec)[0]

Rt = np.concatenate((R_mat, tvec), axis=1)
print("Rotation matrix (R): ")
print(R_mat)
print("Translation matrix (T): ")
print(tvec)
print("Extrinsics matrix ([R|t]): ")
print(Rt)