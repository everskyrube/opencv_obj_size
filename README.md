# Measuring-size-of-objects-in-an-image-with-OpenCV
## 1. pixel per metrics (resolution to the physical size)

Property #1: We should know the dimensions of this object (in terms of width or height) in a measurable unit (such as millimeters, inches, etc.).

pixels_per_metric = 150px / 0.955in = 157px pixels per inches

Using this ratio, pixels_per_metric, we can compute the size of objects in an image.
 
![image](https://github.com/joehalfish/Measuring-size-of-objects-in-an-image-with-OpenCV/blob/master/images/example_01.png)
