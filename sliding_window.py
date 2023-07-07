from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import argparse
import cv2
import numpy as np


def showImg(displayName, image):
    cv2.imshow(displayName, image)
    cv2.waitKey(0)
    cv2.destroyWindow(displayName)

def findContours(image):
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = image
    # gray = cv2.GaussianBlur(gray, (7,7), 0) #removes high-frequence components 
    ## perform edge detection, then perform a dilation + erosion to close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    #find contours in the edge map
    #contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    #sort the contours from left-to-right (allowing to extract the reference object)
    #(cnts, _) = contours.sort_contours(cnts) #the contours parameter name may be conflict with the opencv package name
    cnts = sorted(cnts, key=cv2.contourArea)
    cntAreaThres = 300
    #showImg("edged", edged)
    #loop over the contours individually
    
    for c in cnts.copy():
        if cv2.contourArea(c) < cntAreaThres: #if the contour area is insufficiently large, ignore it
            cnts.remove(c)
            #continue
    mask = np.ones(gray.shape)
    cntImg = cv2.drawContours(mask, cnts, -1 , 0, 3) # -1 to draw all, color and thickness
    showImg("contour", cntImg)
    #print(len(cnts))

def showPixelValue(image):
    for i in range (image.shape[0]): #traverses through height of the image
        for j in range (image.shape[1]): #traverses through width of the image
            if (image[i][j] != 0 and image[i][j] != 255):
                print(image[i][j]) #(x, y), x is column wise, and y is row wise
    #print(type(image))
    #print(image.shape)

def transformImage(image):
    lowerThreshold = 10
    upperThreshold = 240
    for i in range (image.shape[0]):
        for j in range (image.shape[1]):
            if (image[i][j] < lowerThreshold or image[i][j] > upperThreshold):
                image[i][j] = 255
    return image
    #edged = cv2.Canny(image, 50, 100)
    #return image
    #showImg("transformed image", edged)
   
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, default="images/sheep_anno.png", help="path to the input image")
    args = vars(ap.parse_args())
    #image = cv2.imread(args["image"]) 
    #findContours(image)
    image = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
    interpo_image = transformImage(image)
    findContours(interpo_image)
    #showPixelValue(image)

if __name__ == "__main__":
      main()

   
