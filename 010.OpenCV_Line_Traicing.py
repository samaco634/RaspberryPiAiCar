import RPi.GPIO as GPIO

import cv2

import numpy as np

from motor import CarMotor

motors = CarMotor()

def main():


    camera = cv2.VideoCapture(0)

    camera.set(3,160)

    camera.set(4,120)

    try:
        while( camera.isOpened() ):

            ret, frame = camera.read()

            crop_img =frame[60:120, 0:160]

            imgHsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
            #black color detection : HSV range
            lower = np.array([0, 0, 0])

            upper = np.array([180, 255, 60])

            mask = cv2.inRange(imgHsv, lower, upper)

            mask = cv2.dilate(mask,None,iterations=2)

            mask = cv2.erode(mask,None,iterations=2)

            mask = cv2.GaussianBlur(mask,(3,3),0)

            _, contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
            #opencv버전에 따라 findContours 리턴 값 개수가 다름.
            #contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)


            if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)

                crop_img = cv2.drawContours(crop_img, contours, -1, (255, 0, 255), 2)


                M = cv2.moments(c)


                cx = int(M['m10']/M['m00'])

                cy = int(M['m01']/M['m00'])


                crop_img = cv2.circle(crop_img, (cx, cy), 3, (0, 255, 0), -1)


                cv2.imshow('mask',mask)
                cv2.imshow('normal',frame)
              
                print(cx)
            
                if cx >= 96:
                    print("Turn Right!")
                    motors.motor_right(80)
                elif cx <= 65:
                    print("Turn Left")
                    motors.motor_left(80)
                else:
                    print("go")
                    motors.motor_forward(80)
            else:
                print("there are no line")
                motors.motor_stop()


            if cv2.waitKey(1) == ord('q'):
                motors.motor_stop()
                break
                
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
