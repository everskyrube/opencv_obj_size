from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import argparse
import cv2
import numpy as np
import math


def showImg(displayName, image):
    cv2.imshow(displayName, image)
    cv2.waitKey(0)
    cv2.destroyWindow(displayName)

def drawPoint(image, centerOfCircle): #Draw black point on the grayscale image only
    (x, y) = centerOfCircle
    image = cv2.circle(image, (x,y), radius=2, color=(0,255,0), thickness= -1)
    return image

def drawLine(image, lineType, column):
    (img_height, img_width) = image.shape
    line_thickness = 1 # 2 points (x1, y1), (x2, y2)
    if (lineType =="vertical"):
        img_intersection = cv2.line(image, (column, 0), (column, img_height), (0, 255 , 0), thickness = line_thickness)
    
    return img_intersection
    #showImg("intersection", img_intersection)

def lineIntersection(image, lineType, value):
    (img_height, img_width) = image.shape
    if lineType == "vertical":
        for y in range(img_height):
            if image[y, value] ==0:
                image = drawPoint(image, (value, y))
    return image

def calDist(p, q):
    distance = math.sqrt(((p[0] - q[0])**2)+ ((p[1]-q[1])**2))
    return distance

def cal_vertical_LineSegment(image):
    (img_height, img_width) = image.shape
    img_intersection = image.copy()
    mark_start_point = mark_end_point = [0, 0]
    max_distance = 0
    x = 0
    while (x < img_width):
        flag_start_counter = False
        y = 0
        while (y < img_height):
            next_y = y + 1
            if (flag_start_counter == False and image[y,x] == 0 and image[next_y, x] == 1):
                flag_start_counter = True
                start_point = [x, y]
                while (next_y < img_height):
                    if image[next_y,x] == 0:
                        end_point = [x, next_y]
                        y = next_y
                        distance = calDist(start_point, end_point)
                        if (distance > max_distance):
                            max_distance = distance
                            mark_start_point = start_point
                            mark_end_point = end_point
                        flag_start_counter = False
                        break
                    next_y = next_y + 1
            y = y + 1
        x = x + 1   
    img_intersection = cv2.line(img_intersection, mark_start_point, mark_end_point, 0, 2)
    print("Max vertical thickness: ", max_distance) 
    showImg("Line Segments", img_intersection)
    
def cal_horizontal_LineSegment(image):
    (img_height, img_width) = image.shape
    img_intersection = image.copy()
    mark_start_point = mark_end_point = [0, 0]
    max_distance = 0
    y = 0
    while (y < img_height):
        flag_start_counter = False
        x = 0
        while (x < img_width):
            next_x = x + 1
            if (flag_start_counter == False and image[y,x] == 0 and image[y, next_x] == 1):
                flag_start_counter = True
                start_point = [x, y]
                while (next_x < img_width):
                    if image[y,next_x] == 0:
                        end_point = [next_x, y]
                        x = next_x
                        distance = calDist(start_point, end_point)
                        if (distance > max_distance):
                            max_distance = distance
                            mark_start_point = start_point
                            mark_end_point = end_point
                        flag_start_counter = False
                        break
                    next_x = next_x + 1
            x = x + 1
        y = y + 1   
    img_intersection = cv2.line(img_intersection, mark_start_point, mark_end_point, 0, 2)
    print("Max horizontal thickness: ", max_distance) 
    showImg("Line Segments", img_intersection)

def findIntersection(image):
    (img_height, img_width) = image.shape
    total_intersection = 0 
    odd_flag = False
    for x in range(img_width):
        if odd_flag:
            break
        total_intersection = 0
        for y in range(img_height):
            if image[y,x] == 0:
                total_intersection += 1
        if (total_intersection % 2 != 0):
            odd_flag = True
            odd_column = x
            #drawLine(image, "vertical", x)
            odd_intersection_num = total_intersection
            break

    if(odd_flag):
        print("Total intersection points are odd, num = ", odd_intersection_num)
        print("The odd_intersection points in column: ", odd_column)
    else:
        print("Total insection points are even")

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
    cntImg = cv2.drawContours(mask, cnts, -1 , 0, 1) # -1 to draw all, color and thickness
    #cal_vertical_LineSegment(cntImg)
    cal_horizontal_LineSegment(cntImg)
    #findIntersection(cntImg)
    #point_img = lineIntersection(cntImg, "vertical", 400)
    #drawLines(cntImg)
    #showImg("Point Img", point_img)
    #print(len(cnts))

def showPixelValue(image):
    for i in range (image.shape[0]): #traverses through height of the image
        for j in range (image.shape[1]): #traverses through width of the image
            if (image[i][j] != 0 and image[i][j] != 255):
                print(image[i][j]) #(x, y), x is column wise, and y is row wise
    #print(type(image))

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

   
