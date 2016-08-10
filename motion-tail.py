#python 2.7
'''Credit: http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-
tracking-with-python-and-opencv/'''
#u will need to pip install imutils
import imutils
#http://opencv-python-tutroals.readthedocs.io/en/latest/
#py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
import cv2
import time
import winsound

#Capture from webcam. Uncomment below to capture from video file
#camera = cv2.VideoCapture('video_file.extension')
camera = cv2.VideoCapture(0)
time.sleep(0.25)

#Adjust the threshold by pressing 'u' to adjust sensitivity of motion detection
thres = 25
cpt=0

#this loop is what shows a 'video'
while 1:
    #Grab a frame from webcam. this is the 1st instance of frame grabbing.
    #it will be compared below to a 2nd instance of frame grabbing which
    #the difference between the 2 frames will tell whether there was motion
    #PARDON MY GRAMMAR
    (grabbed, baseframe) = camera.read()
    #Flip it to make it mirror exact activity
    baseframe = cv2.flip(baseframe,180)
    #resize the frame
    baseframe = imutils.resize(baseframe,width = 500)
    
    #convert frame into b/w frame. it's necessary for motion detection
    graybaseframe = cv2.cvtColor(baseframe, cv2.COLOR_BGR2GRAY)

    #2nd instance of frame grabbing. purpose of this instance is explained above
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame,180)
    
    frame = imutils.resize(frame, width = 500)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #below gets the 'difference' between the initial and the 2nd frame
    #a difference image will be created which is an image based on 2nd frame
    #minus 1st frame
    differenceimage = cv2.absdiff(graybaseframe, gray)
    #cannot remember what thresholding does but it is a MUST
    #we threshold the diffrence image
    thresholdimage = cv2.threshold(differenceimage, thres, 255, cv2.THRESH_BINARY)[1]
    
    #the thresholded image is blurred to remove the noises which would
    #otherwise raise a false alarm of detected motion
    thresholdimage=cv2.GaussianBlur(thresholdimage, (21, 21), 0)
    #this line will be used to display the threshold image after blurring
    #later on
    thresholdimageD=cv2.GaussianBlur(thresholdimage, (21, 21), 0)

    #this is the badboy (or girl) of the hour
    #find contours only works for an image with only very black and very
    #white 'surface'. and this image will be the threshold image above
    #finding contours is basically finding the white parts in the threshold
    #image. and this white parts will be formed only when there is motion
    (irr, cnts, irr2) = cv2.findContours(thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #honestly idk what happens in this for loop but it is a must
    #but i think c is a single contour and cnts is all contours
    #(white part)
    for c in cnts:
        #if a white part is less than this, yes there is motion since
        #there is a contour but dont raise an alarm
        #the number on right of the if can be changed. works good for me
        #between 500 and 10000. idk what that number is. ask this guy
        #change than n0. depending on size of object / person to be busted
        #http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
        if cv2.contourArea(c) < 1000:
            print 'no movement'
            #continue
        else:
            #if contour area is larger than that no. then call it motion and do
            #something
            print 'movement detected.'
            #in my case its supposed to beep. winsound comes with python 2.7
            winsound.Beep(1000,50)
            #write an image file if it detect motion(stackoverflow)
            cv2.imwrite("motion-tail%d.jpg" %cpt, frame)
            cpt += 1

    #below is windows for normal feed, blurred threshold image and
    #contour image respectively. idk how the 3rd one happened
    cv2.imshow("NormalFeed", frame)
    cv2.imshow("threshold", thresholdimageD)
    cv2.imshow("contour", thresholdimage)
    
    #below are the hotkeys. q to quit and u to increase threshold
    #(sensitivity)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key==ord('u'):
        thres=thres+1
        print thres

#when u press q the above loop is broken and the lines below
#make program let go of your webcam and kills all windows respectively
camera.release()
cv2.destroyAllWindows()
