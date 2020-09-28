from cv2 import cv2 
import numpy as np
import delaunay as D
import os
import __main__ as im

# calculates the area for the triangle with points (x1,y1) , (x2,y2) , (x3,y3)
def area(x1, y1, x2, y2, x3, y3): 
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def isInside(x1, y1, x2, y2, x3, y3, x, y): 
    A = area (x1, y1, x2, y2, x3, y3) 
    # Calculate area of triangle PBC  
    A1 = area (x, y, x2, y2, x3, y3) 
    # Calculate area of triangle PAC  
    A2 = area (x1, y1, x, y, x3, y3) 
    # Calculate area of triangle PAB  
    A3 = area (x1, y1, x2, y2, x, y) 
    # Check if sum of A1, A2 and A3  
    # is same as A 
    if(A == A1 + A2 + A3): 
        return True
    else: 
        return False
  
def generateFrames(src_img,dest_img,num_frames, src_control_pts, dest_control_pts):
   
    for i in range(0,num_frames+1):
        print("Generating frame["+ str(i) + "]")
        # frame_control_pts stores the linearly interpolated coordinates of control points
        frame_control_pts=[]
        for j in range(0,len(src_control_pts)):
            new_x=int(((num_frames-i)/num_frames)*src_control_pts[j][0] + (i/num_frames)*dest_control_pts[j][0])
            new_y=int(((num_frames-i)/num_frames)*src_control_pts[j][1] + (i/num_frames)*dest_control_pts[j][1])
            frame_control_pts.append((new_x,new_y))
        img_size = src_img.shape
        # triangle_List is a list of all the delauny traingles on this image
        triangle_List = D.triangulation(src_img,"im1_newp.txt", frame_control_pts,generate_points=True)
        # intermediate_img is the intermediate i frame
        intermediate_img = np.zeros((img_size[0],img_size[1],3), np.uint8)
        # iterating over all the points in the intermediate frame
        for new_x in range(0,img_size[1]):
            for new_y in range(0,img_size[0]):
                for t in triangle_List:
                    # check if point (new_x , new_y) lies within the triangle t
                    if(isInside(frame_control_pts[t[0]][0],frame_control_pts[t[0]][1],
                                frame_control_pts[t[1]][0],frame_control_pts[t[1]][1],
                                frame_control_pts[t[2]][0],frame_control_pts[t[2]][1],
                                new_x,new_y)):
                                
                                a = np.array([[frame_control_pts[t[1]][0] - frame_control_pts[t[0]][0] , frame_control_pts[t[2]][0] - frame_control_pts[t[0]][0]],
                                                [frame_control_pts[t[1]][1] - frame_control_pts[t[0]][1] , frame_control_pts[t[2]][1] - frame_control_pts[t[0]][1]]])
                                b = np.array([new_x - frame_control_pts[t[0]][0] , new_y - frame_control_pts[t[0]][1]])
                                # this library solves the two linear equations and returns alpha and beta
                                val = np.linalg.solve(a, b)
                                
                                alpha=val[0]
                                beta=val[1]
                                
                                # find the corresponding points in the source and destination image
                                src_x = int(alpha*(src_control_pts[t[1]][0] - src_control_pts[t[0]][0]) + 
                                            beta*(src_control_pts[t[2]][0] - src_control_pts[t[0]][0]) + 
                                                src_control_pts[t[0]][0])
                                src_y = int(alpha*(src_control_pts[t[1]][1] - src_control_pts[t[0]][1]) + 
                                            beta*(src_control_pts[t[2]][1] - src_control_pts[t[0]][1]) + 
                                                src_control_pts[t[0]][1])
                                
                                dest_x = int(alpha*(dest_control_pts[t[1]][0] - dest_control_pts[t[0]][0]) + 
                                            beta*(dest_control_pts[t[2]][0] - dest_control_pts[t[0]][0]) + 
                                                dest_control_pts[t[0]][0])
                                dest_y = int(alpha*(dest_control_pts[t[1]][1] - dest_control_pts[t[0]][1]) + 
                                            beta*(dest_control_pts[t[2]][1] - dest_control_pts[t[0]][1]) + 
                                                dest_control_pts[t[0]][1])
                                # Linearly interpolate their color 
                                for channel in range(0,3):
                                    intermediate_img[new_y][new_x][channel] = np.uint8(((num_frames-i)/num_frames)*src_img[src_y][src_x][channel] + 
                                                                    (i/num_frames)*dest_img[dest_y][dest_x][channel])

                                break      
        # inter_img , this is the directory that stores the intermedite images
        path = 'inter_img'
        file_name = 'img' + str(i) + '.jpg'
        cv2.imwrite(os.path.join(path , file_name), intermediate_img)