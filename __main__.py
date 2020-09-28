#Single click on the image then to store the point press 'a'
#then to complete list, press 'c'

#Enter the paths of the directory in which the code is
#and in the same directory make a folder named "inter_img"

"""
GLOBAL VARIABLES ACCORDING TO USER
"""
# Please change the directory, image1, image2 path and number of frames parameter here
dir_path = "/home/norman/Desktop/MPA_Project/"
img1_path = "/home/norman/Desktop/MPA_Project/img1.jpeg"
img2_path = "/home/norman/Desktop/MPA_Project/img2.jpeg"

no_intermediate_frames = 5


"""
GLOBAL VARIABLES ACCORDING TO USER
"""

from cv2 import cv2
import numpy as np 
import os
import sys
import delaunay as D
import affine as af
import mouse_handling as mh

# source and destination control points are stored in the respective list
src_control_pts=[]
dest_control_pts=[]
# corner_pts, are the corners of the resized image
corner_pts= [(0,0),(0,399),(299,0),(299,399)]


if __name__ == '__main__':
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    #Printing the size of the original images
    print(img1.shape , img2.shape)

    re_img1 = cv2.resize(img1, (300, 400),interpolation = cv2.INTER_NEAREST) 
    re_img2 = cv2.resize(img2, (300, 400),interpolation = cv2.INTER_NEAREST)

    cv2.imwrite("re_img1.jpg",re_img1)
    cv2.imwrite("re_img2.jpg",re_img2)
    no_use = []
    # point_mouse funtionality allows user to select any number of control points on the image and save them in a file
    print("Coordinates of control points of first image")
    count1 = mh.point_mouse("re_img1.jpg", "im1_newp.txt",src_control_pts)
    
    print("Coordinates of control points of second image")
    count2 = mh.point_mouse("re_img2.jpg", "im2_newp.txt",dest_control_pts)
    # the number of control points should be same for both, source and destination images, else an error occurs
    if(count1 == count2):
        # The triangulation functionality is used for delauny triangulation on the image,
        # animate = True allows you to visualize the triangles formed on the image
        triangulated_img1 = D.triangulation(re_img1, "im1_newp.txt", no_use, animate = True)
        triangulated_img2 = D.triangulation(re_img2, "im2_newp.txt", no_use, animate = True)
    else:
        print("[Exit Case] Unequal number of control points")
        exit(0)
    
    # save the triangulated source and destination images
    cv2.imwrite("img1_triangle.jpg", triangulated_img1)
    cv2.imwrite("img2_triangle.jpg", triangulated_img2)
    
    src_img = cv2.imread("re_img1.jpg")
    dest_img = cv2.imread("re_img2.jpg")
    # generateFrames functionality, generates all the intermediate frames using interpolation
    af.generateFrames(src_img,dest_img,no_intermediate_frames+1, src_control_pts, dest_control_pts)

    # ffmpeg is used to convert all the generated frames into an video, with framerate of 5
    os.system("ffmpeg -framerate 15 -i inter_img/img%d.jpg morphing.avi")