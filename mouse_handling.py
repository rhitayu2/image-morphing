from cv2 import cv2

def point_mouse(given_img, file_name,array):
    count = 0 
    file = open(file_name, "w+")
    def draw_circle(event,x,y,flags,param):
            global ix,iy
            #On the event of a left click, store the coordinates of the
            #in the global variable ix and iy
            if (event == cv2.EVENT_LBUTTONDOWN):
                cv2.circle(img,(x,y),2,(0,0,255),-1)
                print(str(x) + ","+str(y), end=" ")
                ix,iy = x,y

    img = cv2.imread(given_img)
    #bind the window to the displayed image
    cv2.namedWindow('image')
    #function used for intercepting mouse events, calls the draw_circle function
    cv2.setMouseCallback('image',draw_circle)

    while(1):
        
        cv2.imshow('image',img)
        k = cv2.waitKey(30)
        #if after the mouseclick, we get an input 'a', we write the global variable
        #in a file, which would be used for Delaunay triangulation
        if k == ord('a'):
            print(":(stored)")
            count = count + 1
            array.append([ix,iy])
            file.write(str(ix) + " " + str(iy) + "\n")
        #On pressing 'c', we will stop and also input the corner points in the 
        #respective array
        if k == ord('c'):
            array.append([0,0])
            array.append([0,399])
            array.append([299,0])
            array.append([299,399])
            break
    cv2.destroyAllWindows()
    #we are returning count as a measure that the both the images have similar number of clicks
    #and if otherwise, we can handle the error in the __main__.py file
    return count