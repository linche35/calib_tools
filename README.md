# Calibration_tools

3 simple tools to help manual calibration.

## Dependencies
* OpenCV
* [Laspy](https://pypi.org/project/laspy/)  `pip install laspy`

## Outline
**1.Tool for manually selecting feature points in images: `clickTool.py`** 

**2.Tool for running ePnP: `ePnp.py`** 

**3.Tool for inlab calibration: `inlab_Calib.py`** 

**4.Automated inlab calibration tool (unfinished):`getBorderPoints.py`**

## Detail Description
### 1. Tool for manually selecting feature points in images
#### Description:
This simple tool loads images in a folder, allows the user to click on feature points, and appends the pixel coordinates of those features in a list.
#### Instruction:
* Step 1. Create a directory and put images of interest in that path
* Step 2. In command line, type: `$ python clickTool.py`
* Step 3. Paste directory path in command line when program prompts `Input image dataset path: `
* Step 4. Images will show up in a window, use mouse scroll wheel to enlarge and click on feature points. Once clicked, you will see the pixel coordinates printed out in the terminal.
* Step 5. When done clicking on an image, press any key, the next image will show up, then you can repeat Step 4. for all images.

### 2. Tool for ePnP
#### Description:
`ePnP.py`, This code is very straight forward, just type in all the paramters for `cv2.solvePnP` and you will get the extrinsics printed out in the terminal.
The 2D image coordinates can be obtained by Tool 1.
As of now, The 3D coordinates can be obtained by Tool 3. for inlab calibration, or using lidar_colorize for outdoor calibration missions.

### 3. Tool for inlab calibration
#### Description:
This code takes in .las files as input to calculate the 3D coordinates of the four corners of a rigid board. This is done by fitting 3D lines to the side lidar points of the board and calculating the intersecting points of the line.
Two methods are used and compared in this code:

**Method 1:**
* Fit a plane to the board using RANSAC
* Project side points onto this plane
* Fit 3D lines to the projected side points
* Compute the intersections of the four lines

**Method 2:**
* Fit 3D lines to the raw side points (not projected to a plane)
* Take the common perpendicular line of two 3D lines and take the mid point of the common perpendicular line as the 3D corner coordinate.
#### Instruction:
* Step 1. Put Yellowscan drone static on the cart, point camera towards a rigid board.
* Step 2. Turn on Yellowscan, record lidar points, and take pictures of the board at different locations in the image. Keep the face of the board parallel to the image plane, this will ensure that the lidar points are cleaner.
* Step 3. Export images of different board positions and the corresponding lidar scans. (More details to be added by Sean?)
* Step 4. Use CloudCompare to crop out the lidar points on the board and save it as a separate .las file. (ex: 1626400903665pcdboardSeg)
* Step 5. This step can be automated once Tool 4. is finished. For now, I am manually cropping out the upper-left, lower-left, upper-right, lower-right sides of the board in CloudCompare and saving it as four separate .las files
* Step 6. In terminal, run `$ python inlab_Calib.py`
* Step 7. Input file paths according to the program.
