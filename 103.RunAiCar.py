import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from car_motor import CarMotor
from camera_buffer_thread import CameraBufferCleanerThread


motors = CarMotor()
speedSet = 35
turnSpeedSet = 35

def img_preprocess(image):
#    height, _, _ = image.shape
#    image = image[int(height/2):,:,:]
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
#   image = cv2.resize(image, (200,66))
#    image = cv2.GaussianBlur(image,(3,3),0)
    #_,image = cv2.threshold(image,160,255,cv2.THRESH_BINARY_INV)
    image = image / 255
    
    return image


        
def main():
    
    model_path = './lane_navigation_check.h5'
    model = load_model(model_path)
    
    carState = "stop"
 
  
    camera = cv2.VideoCapture(-1)
    camera.set(3, 160)
    camera.set(4, 120)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Start the cleaning thread
    cam_cleaner = CameraBufferCleanerThread(camera)
    
    try:
        while True:
            keyValue = cv2.waitKey(1)
        
            if keyValue == ord('q') :
                break
            elif keyValue == 82 :
                print("go")
                carState = "go"
            elif keyValue == 84 :
                print("stop")
                carState = "stop"
                motors.motor_stop()
                
            if 1:
                getNewFrame, image = cam_cleaner.getFrame()

                if getNewFrame == True :
                    preprocessed = img_preprocess(image)
                    cv2.imshow('pre', preprocessed)
            
                    X = np.asarray([preprocessed])
                    steering_angle = int(model.predict(X)[0])
                    print("predict angle:",steering_angle, time.ctime())
                
                    if carState == "go":
                        if steering_angle >=75 and steering_angle <= 105:
                            print("go")
                            motors.motor_forward(speedSet)
                        
                            cv2.putText(
                            image, #numpy array on which text is written
                            "go:{} {}".format(steering_angle, time.ctime()), #text
                            (10,30), #position at which writing has to start
                            cv2.FONT_HERSHEY_SIMPLEX, #font family
                            1, #font size
                            (209, 80, 0, 255), #font color
                            3) #font stroke
                        elif steering_angle > 105:
                             print("right")
                             motors.motor_right(turnSpeedSet)

                        
                             cv2.putText(
                                image, #numpy array on which text is written
                            "right:{} {}".format(steering_angle, time.ctime()), #text
                            (10,30), #position at which writing has to start
                            cv2.FONT_HERSHEY_SIMPLEX, #font family
                            1, #font size
                            (209, 80, 0, 255), #font color
                            3) #font stroke
                        elif steering_angle < 75:
                             print("left")
                             motors.motor_left(turnSpeedSet)
                        
                             cv2.putText(
                            image, #numpy array on which text is written
                            "left:{} {}".format(steering_angle, time.ctime()), #text
                            (10,30), #position at which writing has to start
                            cv2.FONT_HERSHEY_SIMPLEX, #font family
                            1, #font size
                            (209, 80, 0, 255), #font color
                            3) #font stroke
                        #time.sleep(0.2)
                        #motors.motor_stop()
                 
                    cv2.imshow('org', image)
                
        cam_cleaner.terminate()  
        camera.release()
        time.sleep(1)
        cam_cleaner.join()
  
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    GPIO.cleanup()
    cv2.destroyAllWindows()
