# #include < stdio.h>
# #include < iostream>

# #include < opencv2\opencv.hpp>
# #include < opencv2/core/core.hpp>
# #include < opencv2/highgui/highgui.hpp>
# #include < opencv2/video/background_segm.hpp>


# #ifdef _DEBUG        
# #pragma comment(lib, "opencv_core247d.lib")
# #pragma comment(lib, "opencv_imgproc247d.lib")   //MAT processing
# #pragma comment(lib, "opencv_objdetect247d.lib") //HOGDescriptor
# //#pragma comment(lib, "opencv_gpu247d.lib")
# //#pragma comment(lib, "opencv_features2d247d.lib")
# #pragma comment(lib, "opencv_highgui247d.lib")
# #pragma comment(lib, "opencv_ml247d.lib")
# //#pragma comment(lib, "opencv_stitching247d.lib");
# //#pragma comment(lib, "opencv_nonfree247d.lib");
# #pragma comment(lib, "opencv_video247d.lib")
# #else
# #pragma comment(lib, "opencv_core247.lib")
# #pragma comment(lib, "opencv_imgproc247.lib")
# #pragma comment(lib, "opencv_objdetect247.lib")
# //#pragma comment(lib, "opencv_gpu247.lib")
# //#pragma comment(lib, "opencv_features2d247.lib")
# #pragma comment(lib, "opencv_highgui247.lib")
# #pragma comment(lib, "opencv_ml247.lib")
# //#pragma comment(lib, "opencv_stitching247.lib");
# //#pragma comment(lib, "opencv_nonfree247.lib");
# #pragma comment(lib, "opencv_video247d.lib")
# #endif 

# using namespace cv;
# using namespace std;



# int main()
# {

#  //global variables
#  Mat frame; //current frame
#  Mat resize_blur_Img;
#  Mat fgMaskMOG2; //fg mask fg mask generated by MOG2 method
#  Mat binaryImg;
#  //Mat TestImg;
#  Mat ContourImg; //fg mask fg mask generated by MOG2 method
#  Ptr< BackgroundSubtractor> pMOG2; //MOG2 Background subtractor
 
#  pMOG2 = new BackgroundSubtractorMOG2(300,32,true);//300,0.0);
 
#  char fileName[100] = "mm2.avi"; //video\\mm2.avi"; //mm2.avi"; //cctv 2.mov"; //mm2.avi"; //";//_p1.avi";
#  VideoCapture stream1(fileName);   //0 is the id of video device.0 if you have only one camera   

#  //morphology element
#  Mat element = getStructuringElement(MORPH_RECT, Size(7, 7), Point(3,3) );   

#  //unconditional loop   
#  while (true) {   
#   Mat cameraFrame;   
#   if(!(stream1.read(frame))) //get one frame form video   
#    break;
  
#   //Resize
#   resize(frame, resize_blur_Img, Size(frame.size().width/3, frame.size().height/3) );
#   //Blur
#   blur(resize_blur_Img, resize_blur_Img, Size(4,4) );
#   //Background subtraction
#   pMOG2->operator()(resize_blur_Img, fgMaskMOG2, -1);//,-0.5);
  
#   ///////////////////////////////////////////////////////////////////
#   //pre procesing
#   //1 point delete
#   //morphologyEx(fgMaskMOG2, fgMaskMOG2, CV_MOP_ERODE, element);
#   morphologyEx(fgMaskMOG2, binaryImg, CV_MOP_CLOSE, element);
#   //morphologyEx(fgMaskMOG2, testImg, CV_MOP_OPEN, element);

#   //Shadow delete
#   //Binary
#   threshold(binaryImg, binaryImg, 128, 255, CV_THRESH_BINARY);

#   //Find contour
#   ContourImg = binaryImg.clone();
#   //less blob delete
#   vector< vector< Point> > contours;
#   findContours(ContourImg,
#             contours, // a vector of contours
#             CV_RETR_EXTERNAL, // retrieve the external contours
#             CV_CHAIN_APPROX_NONE); // all pixels of each contours

#   vector< Rect > output;
#   vector< vector< Point> >::iterator itc= contours.begin();
#   while (itc!=contours.end()) {
# 
#    //Create bounding rect of object
#    //rect draw on origin image
#    Rect mr= boundingRect(Mat(*itc));
#    rectangle(resize_blur_Img, mr, CV_RGB(255,0,0));
#    ++itc;
#   }
  

#   ///////////////////////////////////////////////////////////////////

#   //Display
#   imshow("Shadow_Removed", binaryImg);
#   imshow("Blur_Resize", resize_blur_Img);
#   imshow("MOG2", fgMaskMOG2);

#   if (waitKey(5) >= 0)   
#    break;   
#  }

# }

import cv2 
import numpy as np 

cap = cv2.VideoCapture('micetest.avi')

ok, frame = cap.read() 
if not ok:
        print("Error occured in fetching the first frame")

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
width = cap.get(3)
height = cap.get(4)

firstFrame = None
count = 0
while ok:
        ok, frame = cap.read() 
        count += 1
        if count == 1:
                firstFrame = frame
        print(str(count))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.resize(frame, (int(width // 3), int(height // 3)))
        frame = cv2.resize(frame, (500, 500))
       
        frame = cv2.blur(frame,(21, 21)) 
        fgmask = fgbg.apply(frame, 0.005) 
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel) 
        # cv2.imwrite("morphology.jpg", fgmask)
        thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]
        # thresh = cv2.adaptiveThreshold(fgmask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite("thresh_b4_dilate.jpg", thresh)
        thresh = cv2.dilate(thresh, kernel=kernel, iterations=2)
        cv2.imwrite("thresh_after_dilate.jpg", thresh) 

        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # for c in contours:
        #         if cv2.contourArea(c) < 1000:
        #                 continue
        #         (x, y, w, h) = cv2.boundingRect(c)
        #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        #         print("count: " + str(count) + " x: " + str(x) +" y: " + str(y) + " w: " + str(w) + " h: " + str(h))
        # # cv2.imshow("Shadow_removed", thresh) 
        for c in contours:  
                if cv2.contourArea(c) > maxArea:
                        maxArea = cv2.contourArea(c)
                        (x, y, w, h) = cv2.boundingRect(c)
        # (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        # print("x: " + str(x) + " y: " + str(y) + " w: " + str(w) + " h: " + str(h)) 
        cv2.imshow("frame", frame) 
        # cv2.imshow("mog2", fgmask) 
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(5) >= 0:
                break 

print(str(count))
