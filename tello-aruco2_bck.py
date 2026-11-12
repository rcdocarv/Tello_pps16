import threading 
import socket
import sys
import time
import cv2
from djitellopy import Tello
from PIL import Image  
import PIL 
import numpy as np
import math


def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(lineA, lineB):
    try:
        # Get nicer vector form
        vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
        vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
        # Get dot prod
        dot_prod = dot(vA, vB)
        # Get magnitudes
        magA = dot(vA, vA)**0.5
        magB = dot(vB, vB)**0.5
        # Get cosine value
        cos_ = dot_prod/magA/magB
        # Get angle in radians and then convert to degrees
        angle = math.acos(dot_prod/magB/magA)
        # Basically doing angle <- angle mod 360
        ang_deg = math.degrees(angle)%360
        
        if ang_deg-180>=0:
            # As in if statement
            return 360 - ang_deg
        else:
            return ang_deg
    except:
        # print("erro no angle")
        return 0

i_center_x = 0
i_center_Y = 0
i_angle = 0

o_up = 0
o_down = 0
o_left = 0
o_right = 0

i = 0

start_step_0 = False
start_step_1 = False
start_step_2 = False
start_step_3 = False

end_step_0 = False
end_step_1 = False
end_step_2 = False
end_step_3 = False

error_step_0 = False
error_step_1 = False
error_step_2 = False
error_step_3 = False

def do_step_0():
    global tello, end_step_0, end_step_1, end_step_2, end_step_3
    try:
        #tello.takeoff()
        err = tello.send_command_with_return('takeoff')
        if (err == 'ok'):
            end_step_0 = True
            return True
        else: 
            tello.send_command_with_return('land')
            error_step_0 = True
            
    except:
        print('erro etapa 0')
        pass

def do_step_1():
    global tello, end_step_0, end_step_1, end_step_2, end_step_3
    try:
        if (end_step_0):
            
            cmd_return_11 = tello.send_command_with_return('forward 180')
            if (cmd_return_11 != 'ok'): #and type(cmd_return_11) is not None    
                tello.send_command_with_return('land')
                error_step_1 = True
            elif (cmd_return_11 == 'ok'):
                
                #time.sleep(0.5)
                cmd_return_12 = tello.send_command_with_return('ccw 90')
                if (cmd_return_12 != 'ok'):
                    tello.send_command_with_return('land')
                    error_step_1 = True
                elif (cmd_return_12 == 'ok'):
                    
                    cmd_return_13 = tello.send_command_with_return('up 60') 
                    if (cmd_return_13 != 'ok'):
                        tello.send_command_with_return('land')
                        error_step_1 = True
                    elif (cmd_return_13 == 'ok'):
                        end_step_1 = True
                        return True
    except:
        print('erro etapa 1')
        pass

def do_step_2():
    global tello, end_step_0, end_step_1, end_step_2, end_step_3
    try:
        if (end_step_1):

            cmd_return_21 = tello.send_command_with_return('forward 20')
            if (cmd_return_21 != 'ok'):
                tello.send_command_with_return('land')
                error_step_2 = True
            elif (cmd_return_21 == 'ok'):
                
                cmd_return_22 = tello.send_command_with_return('ccw 90')
                if (cmd_return_22 != 'ok'):
                    tello.send_command_with_return('land')
                    error_step_2 = True
                elif (cmd_return_22 == 'ok'):
                    end_step_2 = True
                    return True
    except:
        print('erro etapa 2')
        pass

def do_step_3():
    global tello, end_step_0, end_step_1, end_step_2, end_step_3
    try:
        print('----------------------')
        print(end_step_2)
        if (end_step_2):

            cmd_return_31 = tello.send_command_with_return('forward 100')
            print('----------------------')
            print(cmd_return_31)
            
            if (cmd_return_31 != 'ok'):
                tello.send_command_with_return('land')
                error_step_3 = True
            elif (cmd_return_31 == 'ok'):
            
                cmd_return_32 = tello.send_command_with_return('land')
                if (cmd_return_32 != 'ok'):
                    tello.send_command_with_return('land')
                    error_step_3 = True
                elif (cmd_return_32 == 'ok'):
                    end_step_3 = True
                    return True
    except:
        print('erro etapa 3')
        pass

#t0 = threading.Timer(0, do_step_0)
#t0.setDaemon(True)
#t1 = threading.Timer(0, do_step_1)
#t1.setDaemon(True)
#t2 = threading.Timer(0, do_step_2)
#t2.setDaemon(True)
#t3 = threading.Timer(0, do_step_3)
#t3.setDaemon(True)

# Connect to Tello
tello = Tello()
tello.connect()
tello.streamon()

# Set Speed
tello.set_speed(100)

'''
imu_error = tello.send_command_with_return('rc 0 100 0 0')
print("-------------------------------")
print("IMU ERROR: ", imu_error)
print("-------------------------------")
time.sleep(2)
imu_error = tello.send_command_with_return('rc 0 0 0 0')
tello.send_command_with_return('land')
'''

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)


while (True):
    try:

        img_bgr = tello.get_frame_read().frame
        img = img_bgr

        batt =  tello.get_battery()
        cv2.putText(img_bgr, "Batt: " + str(batt) + "%", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
               
        (corners, ids, rejected) = arucoDetector.detectMarkers(img)
        if len(corners) > 0:
            
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                
                if (markerID == 1 or markerID == 2 or markerID == 3):
            
                    # extract the marker corners (which are always returned in
                    # top-left, top-right, bottom-right, and bottom-left order)
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners

                    # convert each of the (x, y)-coordinate pairs to integers
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))

                    # draw the bounding box of the ArUCo detection
                    cv2.line(img_bgr, topLeft, topRight, (0, 255, 0), 1)
                    cv2.line(img_bgr, topRight, bottomRight, (0, 255, 0), 1)
                    cv2.line(img_bgr, bottomRight, bottomLeft, (0, 255, 0), 1)
                    cv2.line(img_bgr, bottomLeft, topLeft, (0, 255, 0), 1)

                    # compute and draw the center (x, y)-coordinates of the ArUco
                    # marker
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(img_bgr, (cX, cY), 4, (0, 0, 255), -1)

                    # draw the ArUco marker ID on the image
                    cv2.putText(img_bgr, str(markerID),
                        (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1)
                    
                    cv2.imshow("PPS16 Drone Delivery System", img)
                    
                    # send Navigation commands
                    # ------------------------------------------------------------------------------------------------------------                        
                    
                    if (not start_step_0 and markerID == 1):
                        print(" ################### STARTING STEP 0 ######################## ")
                        start_step_0 = True
                        #t0.start()
                        do_step_0()
                      
                    elif (end_step_0 and not start_step_1 and markerID == 1):
                        print(" ################### STARTING STEP 1 ######################## ")
                        start_step_1 = True
                        #t1.start()
                        do_step_1()

                        time.sleep(0.5)
                    
                    elif (end_step_1 and not start_step_2 and markerID == 2):
                        print(" ################### STARTING STEP 2 ######################## ")
                        start_step_2 = True
                        #t2.start()
                        do_step_2()

                        time.sleep(0.1)
                    
                    elif (end_step_2 and not start_step_3 and markerID == 3):
                        print(" ################### STARTING STEP 3 ######################## ")
                        start_step_3 = True
                        #t3.start()
                        do_step_3()
                    
        cv2.imshow("PPS16 Drone Delivery System", img)
        
        if error_step_0 or error_step_1 or error_step_2 or error_step_3:
            cv2.destroyAllWindows()
            break
        
        # time.sleep(0.1)
        # wait for ESC key to exit
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()         
            break
    except:
        print("[Error] Tello não conectado ou ArUco não encontrado")
        pass

print(":: End Program ::")
cv2.destroyAllWindows()

tello.land()
tello.get_frame_read().stop()
tello.streamoff()
        













'''
                    # end Navigation handle
                    # ------------------------------------------------------------------------------------------------------------

                    LineA = (topLeft, topRight)
                    lineB = (bottomLeft , bottomRight)
                    angle = round(ang(LineA, lineB), 2)
                    area = (bottomRight[1] - topLeft[1]) * (bottomRight[0] - topLeft[0])
                    
                    i_center_x = cX
                    i_center_y = cY
                    i_angle = angle
                    i_area = area

                    cv2.putText(img_bgr, "Angle: " + str(angle), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(img_bgr, "X Y: (" + str(cX) + ", " + str(cY) + ")", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(img_bgr, "Distance: (" + str(area) + ")", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

'''