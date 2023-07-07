import cv2
import numpy as np

# Read image
img = cv2.imread('./images/ppm_1100_Color.png')
#hh, ww = img.shape[:2]
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# threshold on white
# Define lower and uppper limits
#lower = np.array([200, 200, 200])
#upper = np.array([255, 255, 255])

lower = np.array([22, 93, 0])
upper = np.array([45, 255, 255])
# Create mask to only select black
thresh = cv2.inRange(img, lower, upper)

cv2.imwrite('result_3.jpg', thresh)
cv2.imshow('thresh', thresh)

'''
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20)) # apply morphology
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


mask = 255 - morph # invert morp image

# apply mask to image
result = cv2.bitwise_and(img, img, mask=mask)


# save results
cv2.imwrite('img_thresh.jpg', thresh)
cv2.imwrite('img_morph.jpg', morph)
cv2.imwrite('img_mask.jpg', mask)
cv2.imwrite('img_result.jpg', result)

cv2.imshow('thresh', thresh)
cv2.imshow('morph', morph)
cv2.imshow('mask', mask)
cv2.imshow('result', result)

'''
cv2.waitKey(0)
cv2.destroyAllWindows()