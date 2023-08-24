# Measuring-size-of-objects-in-an-image-with-OpenCV
## (Estimate the physical size from CV approach)

Using the segmented crack image, we can accurately calculate various metrics of the crack using computer vision techniques.
These metrics, in the form of pixel coordinates, can then be used to determine the thickness of the crack.
Additionally, when combined with the depth frame obtained during the inspection, a more comprehensive analysis can be conducted.
 
![image](https://github.com/everskyrube/opencv_obj_size/blob/main/images/demo.jpg?raw=true)

Just run the following command

'''
python3 min_rect.py -i crack_seg.jpg
python3 sliding_window.py -i crack_seg.jpg -o horizontal
python3 sliding_window.py -i crack_seg.jpg -o vertical
'''

#Add a module for the selection of horizontal / vertical line segment calculation
#the output of text is in white color, thus, you cannot see the text if the image background is in white color

#The input image format can be jpg
#For the sliding window algorithm, the input of segmented area should be in black color
#Therefore, image pre-process is needed, if the interested areas in the raw image are not annotated in black color.


