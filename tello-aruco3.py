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
            print("zeca0")
            error_step_0 = True
            tello.send_command_with_return('land')
            
    except:
        print('erro etapa 0')
        pass

def do_step_1():
    global tello, end_step_0, end_step_1, end_step_2, end_step_3
    try:
        if (end_step_0):
            
            cmd_return_11 = tello.send_command_with_return('forward 240')
            if (cmd_return_11 != 'ok'): #and type(cmd_return_11) is not None    
                print("zeca1")
                error_step_1 = True
                tello.send_command_with_return('land')
            elif (cmd_return_11 == 'ok'):
                
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

            cmd_return_21 = tello.send_command_with_return('forward 180')
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

            cmd_return_31 = tello.send_command_with_return('forward 120')
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


# Connect to Tello
tello = Tello()
tello.connect()

# Inicia o streaming de vídeo com resolução e FPS ajustados
tello.streamon()

# Set Speed
tello.set_speed(100)

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# Flag global para controlar quando parar a captura
stop_capture = False

# Função para capturar a imagem da câmara do Tello
def capture_images(tello):
    
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
                
                time.sleep(0.1)
                cv2.imshow("PPS16 Drone Delivery System", img)
                    
            # wait for ESC key to exit
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                cv2.destroyAllWindows()         
                break
            
        except:
            print("[Error] Tello não conectado ou ArUco não encontrado")
            pass
        
        '''        
        if frame is not None:
            # Exibe a imagem capturada
            cv2.imshow("Tello Camera", frame)
        # Espera 1 milissegundo para o próximo quadro
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressione 'q' para sair
            break
        '''

# Cria e inicia uma thread para capturar as imagens
capture_thread = threading.Thread(target=capture_images, args=(tello,))
capture_thread.daemon = True
capture_thread.start()
time.sleep(8)
while (True):
    
    try:
        #print("eu estou aqui2")
        #print("star", start_step_0, start_step_1, start_step_2, start_step_3)
        #print("end", end_step_0, end_step_1, end_step_2, end_step_3)
        #print("err", error_step_0, error_step_1, error_step_2, error_step_3)
        img_bgr2 = tello.get_frame_read().frame
        img2 = img_bgr2

        (corners, ids, rejected) = arucoDetector.detectMarkers(img2)
        if len(corners) > 0:
            
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                
                if (markerID == 1 or markerID == 2 or markerID == 3):
                    '''
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
                    '''

                    # send Navigation commands
                    # ------------------------------------------------------------------------------------------------------------                        
                    
                    print("zeca000", end_step_0)
                    
                    if (not start_step_0 and markerID == 1): # or (not end_step_0 and start_step_0 and markerID == 1)
                        print(" ################### STARTING STEP 0 ######################## ")
                        start_step_0 = True
                        do_step_0()
                        print("zeca00", error_step_0)
                        time.sleep(0.1)
                      
                    elif (end_step_0 and not start_step_1 and markerID == 1):
                        print(" ################### STARTING STEP 1 ######################## ")
                        start_step_1 = True
                        do_step_1()
                        print("zeca11", error_step_1)
                        time.sleep(0.5)
                    
                    elif (end_step_1 and not start_step_2 and markerID == 2):
                        print(" ################### STARTING STEP 2 ######################## ")
                        start_step_2 = True
                        do_step_2()

                        time.sleep(0.1)
                    
                    elif (end_step_2 and not start_step_3 and markerID == 3):
                        print(" ################### STARTING STEP 3 ######################## ")
                        start_step_3 = True
                        do_step_3()

                        time.sleep(0.1)                    

                    if error_step_0 or error_step_1 or error_step_2 or error_step_3:
                        cv2.destroyAllWindows()
                        break
                    
        # wait for ESC key to exit
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()         
            break
    except:
        print("[Error] Tello não conectado ou ArUco não encontrado")
        pass

print("::: End Program :::")
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