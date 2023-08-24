##Usage: python3 min_rect.py --image images/example_01.png

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, default="images/example_01.png", help="path to the input image")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it slightly; 
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# sort the contours from left-to-right and initialize the
# pixels_per_metric calibration variable
(cnts, _) = contours.sort_contours(cnts)

# loop over the contours individually
orig = image.copy()
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 100:
        continue

    box = cv2.minAreaRect(c) # compute the rotated bounding box of the contour
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)  # order the points in the contour such that they appear in top-left, top-right, bottom-right, and bottom-left order
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)  # then draw the outline of the rotated bounding box

    for (x, y) in box: # loop over the original points and draw them
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

    (tl, tr, br, bl) = box # unpack the ordered bounding box, then compute four midpoints
    (tltrX, tltrY) = midpoint(tl, tr) # between the top-left and top-right coordinates, followed by
    (blbrX, blbrY) = midpoint(bl, br) # the midpoint between bottom-left and bottom-right coordinates
    (tlblX, tlblY) = midpoint(tl, bl) # compute the midpoint between the top-left and bottm-left points,
    (trbrX, trbrY) = midpoint(tr, br) # followed by the midpoint between the top-righ and bottom-right

    # draw the midpoints on the image
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # draw lines between the midpoints
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)
    print("Midpoint between top-left and top-right: (", int(tltrX), "," , int(tltrY), ")")
    print("Midpoint between bottem-left and bottom-right: (", int(blbrX), "," , int(blbrY), ")")
    print("Midpoint between top-left and bottom-left: (", int(tlblX), "," , int(tlblY), ")")
    print("Midpoint between top-right and bottom-right: (", int(trbrX), "," , int(trbrY), ")")
    # dA and DB are distance in pixels
    #dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY)) #compute the Euclidean distance of between the midpoints (height)
    #dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY)) #compute the Euclidean distance of between the midpoints (width)

cv2.imshow("Image", orig)
cv2.imwrite("size_estimation_result.jpg", orig)
cv2.waitKey(0)
cv2.destroyAllWindows()