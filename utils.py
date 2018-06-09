import math
import cv2
import numpy as np


def color_threshold(image, threshold, buffer):
    """
    removes every other color except the ones in the range (threshold-buffer, threshold+buffer)
    """
    threshold = np.array(threshold)
    threshold = threshold.reshape((1, 1, 3))
    t1 = image <= (threshold - buffer)
    t2 = image >= (threshold + buffer)
    image[t1] = 0
    image[t2] = 0
    return image


def color_in_range(image, low_threshold, high_threshold, format="RGB"):
    if format == "RGB":
        hsv = rgb_to_hsv(image)
    elif format == "BGR":
        hsv = bgr_to_hsv(image)
    else:
        raise Exception("Unsupported Image Format")

    # Threshold the HSV image to get only colors in range
    mask = cv2.inRange(hsv, low_threshold, high_threshold)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(hsv, hsv, mask=mask)
    return res


def unsharp_mask(image, kernel_size, α=0.8, β=1.0, γ=0.0):
    guass_img = gaussian_blur(image, kernel_size)
    return weighted_img(guass_img, image, α=α, β=β, γ=γ)


def grayscale(img, format="RGB"):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if format == "RGB":
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif format == "BGR":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif format == "HSV":
        """
        The conversion from HSV to gray is not necessary: you already have it.
        You can just select the V channel as your grayscale image
        """
        return img[:, :, 2]


def rgb_to_bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def bgr_to_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def rgb_to_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def quartiled_mean(arr, clip=25):
    """
    Returns the mean of elements between user defined quartiles
    when clip = 25 mean of elements between 1st and 3rd quartiles
    """
    if clip >= 50:
        return None
    arr = np.array(arr)
    arr_len = arr.size
    left_index = int((clip) / 100.0 * arr_len)
    right_index = int((100.0 - clip) / 100.0 * arr_len)
    arr = np.sort(arr)
    arr = arr[left_index:right_index + 1]
    # print("Out of {}, only middle {} [{}, {}] are considered".
    #        format(arr_len, arr.size, left_index, right_index))
    return arr.sum() / arr.size


def draw_lines(img, lines, color=[255, 0, 0], thickness=6, draw_hough_lines=False, clip=25):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below

    from OpenCV Documentation
    All the functions include the parameter color that uses an RGB value
    for color images and brightness for grayscale images.
    For color images, the channel ordering is normally Blue, Green, Red.

    Important
    BGR format is used when image was loaded using cv2.imread(...)
    RGB format is used when image was loaded using mpt.imread(...)
    """
    lslopes = []
    lintercepts = []
    rslopes = []
    rintercepts = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            if (x1 - x2) == 0 or (y1 - y2) == 0:
                continue
            slope = (y1 - y2) / ((x1 - x2) * 1.0)
            intercept = y1 - slope * x1
            if slope < 0.0:
                lslopes.append(slope)
                lintercepts.append(intercept)
                if draw_hough_lines:
                    cv2.line(img, (x1, y1), (x2, y2),
                             [0, 0, 255], 2)  # left lane
            else:
                rslopes.append(slope)
                rintercepts.append(intercept)
                if draw_hough_lines:
                    cv2.line(img, (x1, y1), (x2, y2),
                             [0, 255, 0], 2)  # right lane

    lslope = quartiled_mean(lslopes, clip=clip)
    lintercept = quartiled_mean(lintercepts, clip=clip)
    rslope = quartiled_mean(rslopes, clip=clip)
    rintercept = quartiled_mean(rintercepts, clip=clip)

    # print(lslope, (180 / np.pi) * np.arctan(lslope), lintercept)
    # print(rslope, (180 / np.pi) * np.arctan(rslope), rintercept)

    try:
        y, x, _ = img.shape
        y1 = 0.60 * y
        y2 = y
        x1 = int((y1 - lintercept) / lslope)
        x2 = int((y2 - lintercept) / lslope)
        y1 = int(y1)
        # draw left lane line (BGR)
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)
        # print(x1, y1, x2, y2)
        x1 = int((y1 - rintercept) / rslope)
        x2 = int((y2 - rintercept) / rslope)
        y1 = int(y1)
        # draw right lane line (BGR)
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)
        # print(x1, y1, x2, y2)
    except Exception:
        print("Num points left lane: ", len(lslopes))
        print("Num points right lane: ", len(rslopes))
        print(lslope, (180 / np.pi) * np.arctan(lslope), lintercept)
        print(rslope, (180 / np.pi) * np.arctan(rslope), rintercept)
        raise Exception('draw_lines(...)')

    # print("\n\n")


def hough_lines(img, rho, theta, threshold, min_line_len,
                max_line_gap, draw_hough_lines=False, clip=25):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold,
                            np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, draw_hough_lines=draw_hough_lines, clip=clip)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)


def draw_quadrilateral(img, points, color = (255, 255, 255), thickness=1):
    p1, p2, p3, p4 = points
    cv2.line(img, p1, p2, color, thickness)
    cv2.line(img, p2, p3, color, thickness)
    cv2.line(img, p3, p4, color, thickness)
    cv2.line(img, p4, p1, color, thickness)
    return img
