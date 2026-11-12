import threading 
import socket
import sys
import time
import cv2
from djitellopy import Tello
from PIL import Image  
import PIL 
import numpy as np
# from pyzbar.pyzbar import decode
# from pyzbar.pyzbar import ZBarSymbol
# import matplotlib.pyplot as plt
#import matplotlib.pyplot
#import numpy as np

import math



# from simple_pid import PID

# pid = PID(1, 0.1, 0.05, setpoint=1)


# v = controlled_system.update(0)


i_center_x = 0
i_center_Y = 0
i_angle = 0


o_up = 0
o_down = 0
o_left = 0
o_right = 0




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



# LineA = ((0.6,3.6),(1.6,3))
# lineB = ((1.6,3),(2,3.6))
        
# ARUCO_DICT = {
	# "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	# "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	# "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	# "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	# "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	# "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	# "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	# "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	# "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	# "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	# "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	# "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	# "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	# "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	# "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	# "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	# "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
#	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
#	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
#	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
#	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
# }


arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)


# dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
# parameters =  cv.aruco.DetectorParameters()
# detector = cv.aruco.ArucoDetector(dictionary, parameters)


tello = Tello()
tello.connect()

# tello.set_video_resolution(Tello.RESOLUTION_720P)

tello.streamon()

# tello.takeoff()

# cv2.namedWindow("drone")


#create image processing file

#create flight management file

#create main file

#create log file in the opencv image show




print("aaa")

# time.sleep(5)

# img = tello.get_frame_read().frame
# while img == None:
    # img = tello.get_frame_read().frame

i = 0



def move_up_down(input, target):
    global tello
    try:
        if (target > input):
            print("moving up")
            # tello.move_up(20)
            # tello.go_xyz_speed(0, 0, 20, 10)
            tello.send_command_without_return("up 20")
        else:
            print("moving down")
            # tello.move_down(20)
            # tello.go_xyz_speed(0, 0, -20, 10)
            tello.send_command_without_return("down 20")
    except:
        pass





def move_left_right(input, target):
    global tello
    try:
        if (target > input):
            print("moving right")
            # tello.move_up(20)
            # tello.go_xyz_speed(0, 0, 20, 10)
            tello.send_command_without_return("right 20")
        else:
            print("moving left")
            # tello.move_down(20)
            # tello.go_xyz_speed(0, 0, -20, 10)
            tello.send_command_without_return("left 20")
    except:
        pass




def move_xyz(input_x, input_y, input_distance, target_x, target_y, target_distance):
    global tello
    aux_x = 0
    move_right = False
    aux_y = 0
    move_left = False
    auz_z = 0
    move_up = False
    move_down = False
    move_forward = False
    move_backward = False
    try:
    
        if (target_distance > input_distance):
            aux_x = 100
            move_forward = True
        else:
            move_backward = True
            aux_x = -20
        
        
        if (target_x > input_x):
            aux_y = 20
            move_left = True
        else:
            aux_y = -20
            move_right = True
        
        
        if (target_y > input_y):
            aux_z = 20
            move_up = True
        else:
            aux_z = -20
            move_down = True
        
        
        print("Moving X Y Z: ", aux_x, aux_y, aux_z)
        
        # if (move_up):
            # time.sleep(0.3)
            # tello.send_command_without_return("up 20")
            
        # if (move_down):
            # time.sleep(0.3)
            # tello.send_command_without_return("down 20")
            
        # if (move_left):
            # time.sleep(0.3)
            # tello.send_command_without_return("left 20")
            
        # if (move_right):
            # time.sleep(0.3)
            # tello.send_command_without_return("right 20")
            
            
            
        tello.go_xyz_speed(aux_x, aux_y, aux_z, 100)
        
    except:
        pass


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
            
            cmd_return_11 = tello.send_command_with_return('forward 300')
            if (cmd_return_11 != 'ok'): #and type(cmd_return_11) is not None    
                tello.send_command_with_return('land')
                error_step_1 = True
            elif (cmd_return_11 == 'ok'):

                cmd_return_12 = tello.send_command_with_return('cw 90')
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
                
                cmd_return_22 = tello.send_command_with_return('cw 90')
                if (cmd_return_22 != 'ok'):
                    tello.send_command_with_return('land')
                    error_step_2 = True
                elif (cmd_return_22 == 'ok'):
                    end_step_2 = True
    except:
        print('erro etapa 2')
        pass



def do_step_3():
    global tello, end_step_0, end_step_1, end_step_2, end_step_3
    try:
        print('----------------------')
        print(end_step_2)
        if (end_step_2):

            cmd_return_31 = tello.send_command_with_return('forward 150')
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
    except:
        print('erro etapa 3')
        pass



t0 = threading.Timer(0, do_step_0)
t0.setDaemon(True)

t1 = threading.Timer(0, do_step_1)
t1.setDaemon(True)

t2 = threading.Timer(0, do_step_2)
t2.setDaemon(True)

t3 = threading.Timer(0, do_step_3)
t3.setDaemon(True)


# t1.start()


tello.set_speed(100)



while (True):
    try:
        # print(i)
        img_bgr = tello.get_frame_read().frame
        img = img_bgr
        # img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        # _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        # img = cv2.GaussianBlur(img,(5,5),0)
        # ret3,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # i += 1
        
        batt =  tello.get_battery()
        cv2.putText(img_bgr, "Batt: " + str(batt) + "%", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # cmd1 = cv2.imread("cmd1.png")
        # offSetX = 350
        # offsetY = 450
        # img_bgr[offsetY:offsetY+cmd1.shape[0], offSetX:offSetX+cmd1.shape[1]] = cmd1
        
        # tello.send_keepalive()
        # tello.set_speed(10)
        
        
        # print(img)
        # img = cv2.resize(img, (1080,720))
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
                        
                    LineA = (topLeft, topRight)
                    lineB = (bottomLeft , bottomRight)
                    
                    angle = round(ang(LineA, lineB), 2)
                    
                    area = (bottomRight[1] - topLeft[1]) * (bottomRight[0] - topLeft[0])
                    
                    # control = pid(v)
                    
                    
                    # ------------------------------------------------------------------------------------------------------------
                    # Navigation handle
                    
                    i_center_x = cX
                    i_center_y = cY
                    i_angle = angle
                    i_area = area
                    
                    
                    # move_up_down(i_center_y, 360)
                    # move_left_right(i_center_x, 480)
                    # move_xyz(i_center_x, i_center_y, i_area, 480, 360, 5000)
                    
                    if (not start_step_0 and markerID == 1):
                        print(" ################### STARTING STEP 0 ######################## ")
                        start_step_0 = True
                        t0.start()
                       
                    elif (end_step_0 and not start_step_1 and markerID == 1):
                        print(" ################### STARTING STEP 1 ######################## ")
                        start_step_1 = True
                        t1.start()
                    '''    
                    elif (end_step_1 and not start_step_2 and markerID == 2):
                        print(" ################### STARTING STEP 2 ######################## ")
                        start_step_2 = True
                        t2.start()
                        
                    elif (end_step_2 and not start_step_3 and markerID == 3):
                        print(" ################### STARTING STEP 3 ######################## ")
                        start_step_3 = True
                        t3.start()
                    '''
                    
                    # end Navigation handle
                    # ------------------------------------------------------------------------------------------------------------
                    
                    cv2.putText(img_bgr, "Angle: " + str(angle), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(img_bgr, "X Y: (" + str(cX) + ", " + str(cY) + ")", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(img_bgr, "Distance: (" + str(area) + ")", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        cv2.imshow("drone", img)

        
        if error_step_0 or error_step_1 or error_step_2 or error_step_3:
            cv2.destroyAllWindows()
            break
        
        k = cv2.waitKey(1) & 0xFF
        # time.sleep(0.1)
        # imgplot = plt.imshow(img)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            break
    except:
        #print("houve erro no main")
        pass


# pyzbarOut = decode(img, symbols=[ZBarSymbol.QRCODE])
# print(pyzbarOut)

# img_arr = np.array(img, dtype='int32')
# img_arr = img_arr.astype(dtype='uint8')
# img = Image.fromarray(img_arr, 'RGB')
# img.save("qr_1.bmp")


# pyzbarOut = decode(img, symbols=[ZBarSymbol.QRCODE])
# print("cccc")
# print(pyzbarOut)


print(" ------------------ A desligar tudo ------------------")
tello.get_frame_read().stop()
tello.streamoff()
        
tello.land()


# while True:
    # print("aaa")
    # img = tello.get_frame_read().frame
    # print("bbb")
    
    # cv2.imshow("drone", img)

    # key = cv2.waitKey(0) & 0xff
    # if key == ord('q'):
        # tello.get_frame_read().stop()
        # tello.streamoff()
        # exit(0)

