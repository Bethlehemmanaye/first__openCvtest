
import  cv2 as cv
import numpy as np 



capture = cv.VideoCapture('/home/bethlehem/Documents/Vehicle-counting/Video/carv.mp4')


min_width_react = 80 #min width reactangle
min_height_react = 80 # min height 

count_line_postion = 550

# Initialize substructor
algo = cv.bgsegm.createBackgroundSubtractorMOG()

def center_handle(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx,cy

detect = []
offset = 4#Allowable error between pixel 
counter = 0


while True:
    ret, frame = capture.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(3,3),5)
    # extract region of interest
    height,width,_ = frame.shape
    print(height,width)
    roi = frame[200:8000,250:1000]
    # appling on each frame, method to get the foreground mask.
    img_sub = algo.apply(blur)
    dilat = cv.dilate(img_sub, np.ones((5,5)))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
    dilatada = cv.morphologyEx(dilat, cv.MORPH_CLOSE, kernel)
    dilatada = cv.morphologyEx(dilatada, cv.MORPH_CLOSE, kernel)
    counterShape,h = cv.findContours(dilatada,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    
    cv.line(frame,(25,count_line_postion), (1050, count_line_postion),(255,255,204),3)
    
    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv.boundingRect(c)
        validate_counter = (w>= min_width_react) and (h>= min_height_react)
        if not validate_counter:
            continue
        cv.rectangle(frame,(x,y),(x+w, y+h),(182, 203, 222),2)
        cv.putText(frame, "Vehicle"+str(counter), (x,y-20),cv.FONT_HERSHEY_SIMPLEX,2,(0,127,255),2) 
        
        center = center_handle(x,y,w,h)
        detect.append(center)
        cv.circle(frame,center,4,(0,0,255),-1)
        
        for (x,y) in detect:
            if y<(count_line_postion+offset) and y>(count_line_postion-offset):
                counter+=1
                cv.line(frame,(25,count_line_postion), (1000, count_line_postion),(255,127,255),3) 
                detect.remove((x,y))
                print("Vehicle Counter:" +str(counter))
                
    cv.putText(frame, "VEHICLE COUNTER :"+str(counter), (450,70),cv.FONT_HERSHEY_SIMPLEX,2,(82, 161, 222),5)        
            
    cv.imwrite('messi.png', frame)

    cv.imshow('ror', roi)
 
    # cv.imshow('Detector',dilatada)
    
    k = cv.waitKey(17) & 0xff
    if k == 27:
            break
      
cv.destroyAllWindows()
capture.release()
  
