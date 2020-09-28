# image-morphing
An object oriented project developed in Python3 to morph image into another using Delaunay Triangulation. Implemented OpenCV functions and store the Output as an .avi file


***SETTING UP***
Make sure OpenCV, Numpy are installed
In the project folder make sure there is a 'inter_img' folder present, where the intermediate 
frames would be saved. 
In the __main__.py file, make changes to the global variables according to the user. In dir_path 
mention the address of the project folder. 
In img1_path and img2_path mention the addresses of the images which need to be morphed.
The no_intermediate_frames, determine the number of frames that need to be generated. The more no.
of frames, the smoother will be the transition.
Make sure ffmpeg is installed in your system, as it would be used to generate the video of images
and a suitable video player

***RUNNING THE PROGRAM***
1. Execute the __main__.py file
2. Choose equal number of control points on both the imagesby pressing 'a' after clicking on the 
   corresponding points and when done with the corresponding image press 'c'. (Make sure the order 
   of selecting the points are same of the corresponding facial features)
3. Press any key for each triangulated image output to save
4. When the intermediate frames are generatyed, prompt will come to overwrite a previous video if 
   generated, press 'y' to continue or 'n' to discontinue
