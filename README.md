# **Finding Lane Lines on the Road** 

Overview
---

When we drive, we use our eyes to decide where to go. The lines on the road that show us where the lanes are act as our constant reference for where to steer the vehicle. Naturally, one of the first things we would like to do in developing a self-driving car is to automatically detect lane lines using an algorithm.

In this project we will detect lane lines in images using Python and OpenCV. OpenCV means "Open-Source Computer Vision", which is a package that has many useful tools for analyzing images. The goals / steps of this project are the following: Make a pipeline that finds lane lines on the road.

<img src="examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

Reflection
---

#### 1. Image processing pipeline

My pipeline consisted of 5 steps.

1. Convert Color image to Grayscale image

2. Understand the underlying structure in the image by finding edges in the grayscale image, thi is achived by using caany edge detector algorithm. Before detecting edges, we first smoothen the image using gaussian filter this is done to remove weak gradients which serve as noise in our process

3. Extract region of interest which is a region in image where lanes are present

4. Find Line segments for the edges present in images after region of interest filtering, these lines are calculated using Hough transform

5. These Hough lines are consumed by draw_lines() used to draw left lane and right lane on the original color image

#### 2. draw_lines()

1. Input to draw_lines() function is number of line segments found by Hough transform

2. Slope and y-intercept of each line segment is calcualted using the two-point equation of line

3. Next, we group lines segments as left lane line segments and right lane line segments this grouping is done on the basis of slope value slope < 0 are left side and vice versa. 

4. These group would have some outliers, to tackle this issue, we first sort the group, and then find mean of central window, the width of window is determined by clip paramter. For e.g.: clip = 25, indicates finding mean of elemnts between 1st and 3rd quartile. 

5. Finally, we use the calculated approximate slope and intercept to draw left and right lane on the original color images.

#### 3. Improved Pipeline

1. Original Image pipeline was modified to make it more robust to light intensity variation. This algorithm was later tested on challenge.mp4 video.

2. Yellow lane mark is highly sensitive to brightness variation, to tackle this issue we first convert Color image from RGB/BGR format to HSV format. Later we filter this HSV image for yellow color and then convert to grayscale image. This grayscale image now indicates region in images which have yellow color region.

3. Next we linearly add grayscaled_hsv_yellow_only_image with grayscaled_original_image. The idea is that we want to increase the intensity of yellow regions in the grayscaled_original_image so that it gets easier for canny edge detector to find edges.

4. Another improvement done was, instead of using singular region of intrest we now have two regions of intrest one for each lane, therby further reducing the noise in the image.

#### 4. Potential shortcomings and improvements

1. The pipeline assume lane marking to be always present in the image for it to function properly.
2. A potential improvement here is to use the history of lanes lines detected so far to assist in the current lane marking process.  
3. While the pipeline does a good job of finding lanes, a lot of features in the pipeline are handcrafted. We can use a higher capacity function to find lanes that generalizes well for most of the use cases.
4. Experiment other image formats like HSL
