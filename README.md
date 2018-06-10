# **Finding Lane Lines on the Road** 

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road

[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

### Reflection

### 1. Image processing pipeline

My pipeline consisted of 5 steps.

1. Convert Color image to Grayscale image

2. Understand the underlying structure in the image by finding edges in the grayscale image, thi is achived by using caany edge detector algorithm. Before detecting edges, we first smoothen the image using gaussian filter this is done to remove weak gradients which serve as noise in our process

3. Extract region of interest which is a region in image where lanes are present

4. Find Line segments for the edges present in images after region of interest filtering, these lines are calculated using Hough transform

5. These Hough lines are consumed by draw_lines() used to draw left lane and right lane on the original color image

### 2. draw_lines()

1. Input to draw_lines() function is number of line segments found by Hough transform

2. Slope and y-intercept of each line segment is calcualted using the two-point equation of line

3. Next, we group lines segments as left lane line segments and right lane line segments this grouping is done on the basis of slope value slope < 0 are left side and vice versa. 

4. These group would have some outliers, to tackle this issue, we first sort the group, and then find mean of central window, the width of window is determined by clip paramter. For e.g.: clip = 25, indicates finding mean of elemnts between 1st and 3rd quartile. 

5. Finally, we use the calculated approximate slope and intercept to draw left and right lane on the original color images.

