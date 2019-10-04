'''
#======= DESCRIPTION =======
This program works by using Region of Interest (ROI) selection to find key src
and dst points. Then it uses the normal method for the transforming the image
into BEV. For some reason, when selecting ROI, I couldn't see the actual marks
on the ground, so I translated the image for selected, and then undid the
translation later on after points were selected. Maybe this step won't be
needed on other devices.

To Use:
1) Set fileName to the name of the image being transformed.
2) Ensure the image and this file are in the same folder.
3) Run the program.
4) A Select ROI box will appear. Select a point or rectangular region that
    captures the top left marker on the ground. Press space.
5) Another Select ROI box will appear. Do the same thing, but for the top right
    marker. Repeat twice more for the bottom right and bottom left markers, in
    that order.
6) A final Select ROI box will appear. Select the rectangular region which will
    define the 4 corners of the dst points. When this region is selected, press
    space again.
7) Two images will be output. First, "fileName_transformed.png" will contain
    the transformed image. Second, "fileName_pts_shown.png" will show the src
    and dst points you selected in red and green, respectively.
'''


import numpy as np
import cv2


#======= Helper Functions =======

# Function to get src points - select points clockwise from top left
def get_src(img,vertical_shift):
    topL_ROI = cv2.selectROI(img)
    topL_x = topL_ROI[0] + 0.5*topL_ROI[2]
    topL_y = topL_ROI[1] + 0.5*topL_ROI[3] + vertical_shift
    topL = np.float32([topL_x,topL_y])

    topR_ROI = cv2.selectROI(img)
    topR_x = topR_ROI[0] + 0.5*topR_ROI[2]
    topR_y = topR_ROI[1] + 0.5*topR_ROI[3] + vertical_shift
    topR = np.float32([topR_x,topR_y])
    
    botR_ROI = cv2.selectROI(img)
    botR_x = botR_ROI[0] + 0.5*botR_ROI[2]
    botR_y = botR_ROI[1] + 0.5*botR_ROI[3] + vertical_shift
    botR = np.float32([botR_x,botR_y])
    
    botL_ROI = cv2.selectROI(img)
    botL_x = botL_ROI[0] + 0.5*botL_ROI[2]
    botL_y = botL_ROI[1] + 0.5*botL_ROI[3] + vertical_shift
    botL = np.float32([botL_x,botL_y])
    
    src = np.float32([topL,topR,botR,botL])
    
    return src


# Function to get dst points - select ROI
def get_dst(img,vertical_shift):
    
    dst_ROI = cv2.selectROI(img)
    
    topL_x = dst_ROI[0]
    topL_y = dst_ROI[1] + vertical_shift
    topL = np.float32([topL_x,topL_y])
    
    topR_x = dst_ROI[0] + dst_ROI[2]
    topR_y = dst_ROI[1] + vertical_shift
    topR = np.float32([topR_x,topR_y])
    
    botR_x = dst_ROI[0] + dst_ROI[2]
    botR_y = dst_ROI[1] + dst_ROI[3] + vertical_shift
    botR = np.float32([botR_x,botR_y])
    
    botL_x = dst_ROI[0]
    botL_y = dst_ROI[1] + dst_ROI[3] + vertical_shift
    botL = np.float32([botL_x,botL_y])
    
    dst = np.float32([topL,topR,botR,botL])
    
    return dst


# Test the selection of the any points by plotting them on img
def test_pts(img,pts,colour):
    for i in range(int(pts[0][1])-1,int(pts[0][1])+2):
        for j in range(int(pts[0][0])-1,int(pts[0][0])+2):
            img[i][j] = colour
    
    for i in range(int(pts[1][1])-1,int(pts[1][1])+2):
        for j in range(int(pts[1][0])-1,int(pts[1][0])+2):
            img[i][j] = colour
            
    for i in range(int(pts[2][1])-1,int(pts[2][1])+2):
        for j in range(int(pts[2][0])-1,int(pts[2][0])+2):
            img[i][j] = colour
    
    for i in range(int(pts[3][1])-1,int(pts[3][1])+2):
        for j in range(int(pts[3][0])-1,int(pts[3][0])+2):
            img[i][j] = colour
            
    return



#======= Main =======

# Get image and size
fileName = "left_bev.png"
img = cv2.imread(fileName,-1)
img_size = (img.shape[1], img.shape[0])


# Resize matrix to nxm pixels (n width, m height)
vertical_shift = 0
(n,m) = (512,512)
img_size = (n, m)
img = cv2.resize(img,(n,m))
cv2.imwrite(fileName[:len(fileName)-4] + "_resized.png",img)


# Select and process all src points - clockwise from top left
src = get_src(img,vertical_shift)
print("src")
print(src)


# Select ROI for dst points and find dst
dst = get_dst(img,vertical_shift)
print("dst")
print(dst)


# Get and apply BEV transform
M = cv2.getPerspectiveTransform(src, dst)
bev = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
cv2.imwrite(fileName[:len(fileName)-4] + "_transformed.png", bev)
print("M")
print(M)


# Test selection of src and dst points
img_test = img
test_pts(img_test,src,(0,0,255))
test_pts(img_test,dst,(0,255,0))
cv2.imwrite(fileName[:len(fileName)-4] + "_pts_shown.png",img_test)


# Clean up windows
cv2.destroyAllWindows()