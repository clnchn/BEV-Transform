# BEV-Transform
Camera testing for WATonomous Camera Calibration team for Bird's Eye View Perspective Transformation. 


## Introduction 

Parallel lines appear to converge on images from a front facing camera due to perspective. In order to keep parallel lines parallel for photogrammetry a bird’s eye view transformation should be applied. The program describes how to transform images for lane lines detection.


### BEV Transformation

(1) Extract its region of interest

Two Methods

(1) stretch the top row of pixels while keeping the bottom row unchanged

(2) shrinking the bottom of the image while keeping the top row unchanged


One may consider the first variant more obvious. However, it ** increases the spatial resolution ** (without adding information) for the distant part of the image and it could lead to line bounds erosion, hence, ** gradient algorithms may have difficulties with its detection **. It also reduce viewing angle, therefore it is impossible to track other than central lanes.

The second way of transformation was selected as a better one because it preserves all avalable pixels from the raw image on the top edge where there is lower relative resolution. To find correct transformation, source and destinations points a test image with flat and straight road can be used for perspective measurements.


## Description

This program works by using Region of Interest (ROI) selection to find key src
and dst points. Then it uses the normal method for the transforming the image
into BEV. For some reason, when selecting ROI, I couldn't see the actual marks
on the ground, so I translated the image for selected, and then undid the
translation later on after points were selected. Maybe this step won't be
needed on other devices.


## To Use

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
