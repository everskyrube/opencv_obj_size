from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import argparse
import cv2
import numpy as np
import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def on_destroy(window):
    cv2.destroyAllWindows()

def showImg(displayName, image):
    cv2.imshow(displayName, image)
    cv2.waitKey(0)
    window = Gtk.Window() # Be properly registering the window and connecting the destroy event.
    window.connect("destroy", on_destroy)

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
    mark_start_point = mark_end_point = [0, 0]
    max_distance = 0
    x = 0
    while (x < img_width):
        flag_start_counter = False
        y = 0
        while (y < img_height -1):
            if (flag_start_counter == False and image[y,x] == 0 and image[y+1, x] == 1):
                flag_start_counter = True
                start_point = [x, y]
                explorer = y + 1
                while (explorer < img_height - 1):
                    if (image[explorer,x] == 0 and image[explorer+1, x] == 1):
                        end_point = [x, explorer]
                        distance = dist.euclidean(start_point, end_point)
                        if (distance > max_distance):
                            max_distance = distance
                            mark_start_point = start_point
                            mark_end_point = end_point
                        flag_start_counter = False
                        y = explorer+1
                        break
                    explorer = explorer + 1
            y = y + 1
        x = x + 1 
    return mark_start_point, mark_end_point, max_distance 
    
def cal_horizontal_LineSegment(image):
    (img_height, img_width) = image.shape
    mark_start_point = mark_end_point = [0, 0]
    max_distance = 0
    y = 0
    while (y < img_height):
        flag_start_counter = False
        x = 0
        while (x < (img_width-1)):
            if (flag_start_counter == False and image[y,x] == 0 and image[y, x + 1] == 1): 
                flag_start_counter = True
                start_point = [x, y]
                if flag_start_counter: 
                    explorer = x + 1
                    while (explorer < img_width - 1):
                        if (image[y,explorer] == 0 and image[y, explorer + 1]== 1): #This may cause edge problem
                            end_point = [explorer, y]
                            distance = dist.euclidean(start_point, end_point)
                            if (distance > max_distance):
                                max_distance = distance
                                mark_start_point = start_point
                                mark_end_point = end_point
                            flag_start_counter = False
                            x = explorer + 1 
                            break
                        explorer = explorer + 1      
            x = x + 1
        y = y + 1  

    return mark_start_point, mark_end_point, max_distance
    
def cal_one_LineSegment(image):
    (img_height, img_width) = image.shape
    img_intersection = image.copy()
    mark_start_point = mark_end_point = [0, 0]
    max_distance = 0
    y = 136
    flag_start_counter = False
    x = 0
    while (x < (img_width-1)):
        #next_x = x + 1 # the (edge point + 1) is out of bounds for the image []; and image[y, next_x] == 1
        if (flag_start_counter == False and image[y,x] == 0 and image[y, x+1] ==1): 
            flag_start_counter = True
            start_point = [x, y]
            print("start Point: ", start_point)
            if flag_start_counter: #if the startpoint is found, explore the endpoint
                explorer = x + 1
                while (explorer < img_width):
                    if (image[y,explorer] == 0 and image[y, explorer+1] ==1):
                        end_point = [explorer, y]
                        print("End Point: ", end_point)
                        distance = calDist(start_point, end_point)
                        if (distance > max_distance):
                            max_distance = distance
                            mark_start_point = start_point
                            mark_end_point = end_point
                        flag_start_counter = False
                        x = explorer + 1 #if endpoint is found, start a new searching process
                        break
                    explorer = explorer + 1      
        x = x + 1
        
    img_intersection = cv2.line(image, mark_start_point, mark_end_point, 0, 1)
    #print("Max horizontal thickness: ", max_distance)
    cv2.imwrite("horizontal_result.jpg", 255*img_intersection) 
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

def findContours(image, cal_operation, ppm):
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
    cntAreaThres = 10 # set the threshold of contour area to filter small contour
    #showImg("edged", edged)
    
    max_distance = 0
    for c in cnts.copy(): #loop over the contours individually
        mask = np.ones(gray.shape)
        if cv2.contourArea(c) < cntAreaThres: #if the contour area is insufficiently large, ignore it
            cnts.remove(c)
            continue
        mask = cv2.drawContours(mask, c, -1, 0, 1) ##NOT keep drawing here!
        if (cal_operation == "horizontal"):
            start_point, end_point, distance = cal_horizontal_LineSegment(mask)
            if(distance > max_distance):
                max_distance = distance
                mark_start_point = start_point
                mark_end_point = end_point

        elif (cal_operation == "vertical"):
            start_point, end_point, distance = cal_vertical_LineSegment(mask)
            if(distance > max_distance):
                max_distance = distance
                mark_start_point = start_point
                mark_end_point = end_point

    image_name = "horizontal_result.jpg" if (cal_operation == "horizontal") else "vertical_result.jpg"
    base_img = cv2.drawContours(mask, cnts, -1 , 0, 1) # -1 to draw all, color and thickness
    img_intersection = cv2.line(base_img, mark_start_point, mark_end_point, 0, 1)
    # print("PPM: ", ppm)
    # physical_dist = (max_distance / ppm) * 1000
    # print("Max ", cal_operation, " thickness: ", physical_dist)
    print("Calculation: ", cal_operation)
    print("Start Point: ", mark_start_point) # Mark pixel coordinate for the thickness calculation
    print("End Point: ", mark_end_point)
    cv2.imwrite(image_name, 255 * img_intersection) 
    showImg(image_name, img_intersection)

def showPixelValue(image, type = "grayscale_image"):
    if (type =="grayscale_image"):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if(image[i][j]!=1): #0 black; 1 white
                    print(image[i][j])
    else:
        if(image.shape[2] == 1): #grayscale image 
            for i in range(image.shape[0]): #traverses through height of the image
                for j in range(image.shape[1]): #traverses through width of the image
                    #if (image[i][j]!= 0 and image[i][j]!= 255):
                        print(image[i][j])

        if(image.shape[2] == 3): ## Three channels
            for i in range (image.shape[0]): 
                for j in range (image.shape[1]): 
                    if not (image[i][j][0]==255 and image[i][j][1]==255 and image[i][j][2] == 255):
                        print(image[i][j])
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
    ap.add_argument("-o", "--operation", required=False, default="horizontal", help="cal horizontal or vertical line segment")
    ap.add_argument("-ppm", "--pixelsPerMetric", type=float, required=False, default="1000", help ="calculate the physical distance")
    args = vars(ap.parse_args())
    image = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
    ppm = args["pixelsPerMetric"]
    findContours(image, args["operation"], ppm)

if __name__ == "__main__":
      main()

   
