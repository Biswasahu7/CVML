# **********************************
# Shell 4 front view model Details
# **********************************

# Shell 4 front view Camera Details
# IP - "192.168.12.15"
# User Name - admin
# Password - vert@123

# Shell 4 EBT Camera Details
# IP - "192.168.12.14"
# User Name - admin
# Password - vert@123
# Flapper

# Import necessary libraries...
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
import datetime
import time
import math
import cv2
import pyodbc
import numpy as np
import touch
import sys
from hikvisionapi import Client
from SQL_Data_Insert import insert_data


# MODEL LOGGER DETAILS...
l1=datetime.datetime.now()
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
# add a time rotating handler
handler = TimedRotatingFileHandler("/home/root1/CVML_2/Model_Logs/shell4/logs_{}.log".format(l1), when="m", interval=60)
logger.addHandler(handler)

# YOLO MODEL INITIALISE...
# Assigning  front view camera 4 model net and weight details...(9th_Aug)
# net1 = cv2.dnn.readNet('/home/root1/CVML_2/Yolo_Config/Shell_4_Frontview/9th_Aug/yolov3_training_final.weights',
#                       '/home/root1/CVML_2/Yolo_Config/Shell_4_Frontview/9th_Aug/yolov3_testing.cfg')
#
# # Assigning front view camera 4 model class details...
# classes1 = []
# with open("/home/root1/CVML_2/Yolo_Config/Shell_4_Frontview/9th_Aug/classes.txt", "r") as f:
#     classes1 = f.read().splitlines()


# 30th_Aug model details
net1 = cv2.dnn.readNet('/home/root1/CVML_2/Yolo_Config/Shell_4_Frontview/30th_Aug/yolov3_training_final.weights',
                       '/home/root1/CVML_2/Yolo_Config/Shell_4_Frontview/30th_Aug/yolov3_testing.cfg')

# Assigning front view camera 4 model class details...
classes1 = []
with open("/home/root1/CVML_2/Yolo_Config/Shell_4_Frontview/30th_Aug/classes.txt", "r") as f:
    classes1 = f.read().splitlines()

# ****************************************************************************************************************************

# Assigning  EBT camera 4 model net and weight details...
net2 = cv2.dnn.readNet('/home/root1/CVML_2/Yolo_Config/Shell_4_EBT/Aug_12/yolov3_training_final.weights',
                      '/home/root1/CVML_2/Yolo_Config/Shell_4_EBT/Aug_12/yolov3_testing.cfg')

# Assigning EBT camera 4 model class details...
classes2 = []
with open("/home/root1/CVML_2/Yolo_Config/Shell_4_EBT/Aug_12/classes.txt", "r") as f:
    classes2 = f.read().splitlines()


# centroid function
def pega_centro(l, r, t, b):
    x1 = int(t / 2)
    y1 = int(b / 2)
    cx = l + x1
    cy = r + y1
    return cx, cy

# Checking cycle end in SQL table
def is_cycle_end():

    # Connect SQL server to get the info
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'Server=172.21.25.164;'
        'Database=cvmlautomation2;'
        'UID=sa;'
        'PWD=admin@123;'
        'MARS_connection=yes')

    cursor = conn.cursor()
    ebj_end_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";

    # EXECUTE QUERY
    cursor.execute(ebj_end_query)
    myresult = cursor.fetchall()

    # This the condition where we will get signal from SQL to end the cycle...
    flag = 0
    for a in myresult:

        # print("Its - {}...should be Shell 4 Blowing/Arcing".format(a[0]))
        # if a[0] == "Shell 4 Blowing" or a[0] == "Shell 4 Arcing":
        # print("Its-{}...should be TRUE".format(a[1]))

        if a[1] == "TRUE":  # or a[1] == "MIDDLE":
            # logger.info("Shell 4 Flapper...Its-{}...should be OPEN/MIDDLE".format(a[1]))
            # ebj_removal_end = datetime.datetime.now().replace(microsecond=0)
            print("END")
            flag = 1
            break
    return flag


# This the is the main function to monitor shell 4 mddel
def shell_4():

    # Assign variable
    # P1
    start_process_monitoring = 0
    ebj_removal_start = 0
    ebj_removal_start_optional = 0
    ebj_removal_end = 0

    # P2
    ebt_mass_filling_start = 0
    ebt_mass_filling_end = 0

    # P3
    shell_levelling_start = 0
    shell_levelling_end = 0
    shell_end=0

    # P4
    top_lance_positioning_list=[]
    bucket_plus_count=0
    bucket_plus = 0
    top_count=0
    start_pouring = 0
    top_pouring = 0
    hm_positioning_start = 0
    hm_positioning_end = 0
    hm_pouring_start = 0
    hm_pouring_end = 0
    top_lance_positioning_start = 0
    top_lance_positioning_end = 0
    bucket_area=[]
    bucket_count=0
    pouring_check=0

    launder_car_insertion_list=[]
    launder_count=0
    launder_pouring = 0
    top_lance_positioning_start = 0
    top_lance_positioning_end = 0
    launder_insertion_start = 0
    launder_insertion_end = 0
    hm_positioning_list=[]
    hm_positioning_start = 0
    hm_positioning_end = 0
    hm_pouring_start = 0
    hm_pouring_end = 0
    end_hm_pouring = 0

    # NON CYCLIC

    person_count=0
    person_time=[]
    slug_removal = 0
    slug_count=0
    slug_removal_start=0
    slug_removal_end=0
    no_slug_car=0
    scrap_charging = 0
    scrap_count=0
    no_scrap_bucket=0
    scrap_charging_start=0
    scrap_charging_end=0
    gunning = 0
    gunning_start=0
    gunning_end=0
    gunning_person_count=0
    no_gunning=0
    fettling = 0
    fettling_start=0
    fettling_end=0
    fettling_bucket_count=0
    no_fettling_bucket=0


    # COMMON VARIABLES
    bucket_plus_list = []
    blowing_true=0
    connected_front=0
    check_end_cycle=0
    t1=time.time()
    t2=time.time()
    cycle = 0
    timestamps = []
    cycles = {}
    tim = time.time()
    end_cycle = 0
    ebt_camera = 0
    front_camera = 0
    top_lance_distance = 0
    launder_car_distance=0
    recent_proc_time = time.time()
    cur_tim = time.time()
    none_frame = 0
    pro_time = []
    per_count = 0
    per_cent = []
    none_frame_ebt = 0
    none_frame_front=0
    sec = 0.0
    framerate = 1.0
    end_ebt=0
    end_front=0

    # VIDEOWRITER VARIABLE
    vout_ebt = None
    fps_ebt = 1
    vout_front = None
    fps_front = 1

    # while True:

    try:

        # CONNECT TO EBT shell 4 CAMERA

        ip_ebt = "192.168.12.14"
        cap_ebt = cv2.VideoCapture()
        cap_ebt.open("rtsp://admin:vert@123@{}/Streaming/channels/1/?tcp".format(ip_ebt))
        distance = []

        # EBT CAMERA
        while end_cycle == 0:
            try:
                # Before starting this process we need to connect SQL DB to get the Shell 4 information to go head...
                st = datetime.datetime.now().replace(microsecond=0)
                print("Start connection EBT 4 Camera-{}".format(st))

                # logger.info("Start Connection to DB")

                # To start the process we need to run SQL to get trigger message...
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'Server=172.21.25.164;'
                    'Database=cvmlautomation2;'
                    'UID=sa;'
                    'PWD=admin@123;'
                    'MARS_connection=yes')

                cursor = conn.cursor()
                # print("Connection successfull to DB")
                logger.info("Connection successful to DB")

                # COLUMN NAMES
                c = ['Id', 'Name', 'Alias', 'Value', 'CreatedDateTime', 'ShellNo', 'ShortString1', 'ShortString2','DateTime1']

                # TO START PROCESS MONITORING FOR SQL DATA
                # logger.info("checking when to start process monitoring")
                while start_process_monitoring != 1:
                    # logger.info("checking when to start process monitoring")

                    process_start_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";

                    # EXECUTE QUERY
                    cursor.execute(process_start_query)
                    myresult = cursor.fetchall()

                    # First condition need to check SQL value...
                    for a in myresult:
                        # logger.info("Its {}".format(a[0]))

                        if a[0] == "Shell 4 Tapping":
                            # # print(a[1])
                            if int(time.time())%3 == 0:
                                time.sleep(1)
                                logger.info("Shell 4 Tapping Its {}-{}".format(a[1],datetime.datetime.now()))

                            if a[1] == "TRUE":
                                logger.info("Shell 4 tapping...Its {}".format(a[1]))
                                start_process_monitoring = 1
                                pt = datetime.datetime.now().replace(microsecond=0)
                                print("Process Start-{}".format(pt))
                                logger.info("Process started \n")
                                break

                # PROCESS 1 - EBJ_removal
                # logger.info("EBJ removal process check")

                # # EBJ START WE NEED TO CONNECT db TO GET THE INFO...
                # while ebj_removal_start == 0:
                #     # logger.info("EBJ removal process check")
                #
                #     ebj_start_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";
                #
                #     # EXECUTE QUERY
                #     cursor.execute(ebj_start_query)
                #     myresult = cursor.fetchall()
                #
                #     # Second condition to continue this process
                #     for a in myresult:
                #         # logger.info("Its {}".format(a[0]))
                #         if a[0] == "Shell 4 Ramp":
                #             if int(time.time())%3==0:
                #                 time.sleep(1)
                #                 logger.info("Shell 4 Ramp Its-{}".format(a[1]))
                #             # print("Its-{}...should be MIDDLE".format(a[1]))
                #
                #             if a[1] == "MIDDLE":
                #                 logger.info("Shell 4 ramp Its-{}".format(a[1]))
                #                 ebj_removal_start = datetime.datetime.now().replace(microsecond=0)
                #                 logger.info("EBJ removal start-{} \n".format(ebj_removal_start))
                #                 print("EBJ removal start-{} \n".format(ebj_removal_start))
                #                 break

                # EBJ END
                # logger.info("EBJ end check")

                # while ebj_removal_end == 0:
                #     ebj_end_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";
                #
                #     # EXECUTE QUERY
                #     cursor.execute(ebj_end_query)
                #     myresult = cursor.fetchall()
                #
                #     # Third condition to continue this process...
                #     for a in myresult:
                #         # logger.info("Its - {}...should be Shell 4 Flapper".format(a[0]))
                #
                #         if a[0] == "Shell 4 Flapper":
                #
                #             if int(time.time())%3 == 0:
                #                 time.sleep(1)
                #                 logger.info("Shell 4 Flapper Its-{}".format(a[1]))
                #             # print("Its-{}...should be OPEN/MIDDLE".format(a[1]))
                #
                #             if a[1] == "CLOSE":
                #                 # time.sleep(2)
                #                 logger.info("Shell 4 Flapper...Its-{}".format(a[1]))
                #                 ebj_removal_end = datetime.datetime.now().replace(microsecond=0)
                #                 logger.info("EBJ removal end-{} \n".format(ebj_removal_end))
                #                 print("EBJ removal end-{} \n".format(ebj_removal_end))
                #                 break

                while ebj_removal_end == 0:

                    # CHECK EBJ START from SQL.
                    if ebj_removal_start == 0:
                        ebj_start_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";
                        # EXECUTE QUERY
                        cursor.execute(ebj_start_query)
                        myresult = cursor.fetchall()
                        # logger.info("checking ebj_removal_start")
                        # Second condition to continue this process...
                        for a in myresult:
                            # logger.info("Its {}".format(a[0]))
                            if a[0] == "Shell 4 Ramp":
                                if int(time.time()) % 3 == 0:
                                    time.sleep(1)
                                    logger.info("Shell 4 Ramp Its-{}".format(a[1]))
                                # print("Its-{}...should be MIDDLE".format(a[1]))

                                if a[1] == "MIDDLE":
                                    logger.info("Shell 4 ramp Its-{}".format(a[1]))
                                    ebj_removal_start = datetime.datetime.now().replace(microsecond=0)
                                    logger.info("EBJ removal start-{} \n".format(ebj_removal_start))
                                    print("EBJ removal start-{} \n".format(ebj_removal_start))
                                    break

                    # CHECK EBJ START OPTIONAL
                    if ebj_removal_start_optional == 0:

                        ebj_start_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";
                        # EXECUTE QUERY
                        cursor.execute(ebj_start_query)
                        myresult = cursor.fetchall()

                        # Second condition to continue this process
                        for a in myresult:
                            # logger.info("Its {}".format(a[0]))
                            if a[0] == "Shell 4 Tapping":
                                if int(time.time()) % 3 == 0:
                                    time.sleep(1)
                                    logger.info("Shell 4 Tapping Its-{}".format(a[1]))
                                # print("Its-{}...should be MIDDLE".format(a[1]))

                                if a[1] == "FALSE":
                                    logger.info("Shell 4 Tapping Its-{}".format(a[1]))
                                    ebj_removal_start_optional = datetime.datetime.now().replace(microsecond=0)
                                    logger.info("EBJ removal start optional -{} \n".format(ebj_removal_start_optional))
                                    print("EBJ removal start optional -{} \n".format(ebj_removal_start_optional))
                                    break

                    # CHECK EBJ END
                    ebj_end_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";
                    # EXECUTE QUERY
                    cursor.execute(ebj_end_query)
                    myresult = cursor.fetchall()

                    # Third condition to continue this process...
                    for a in myresult:
                        if a[0] == "Shell 4 Flapper":
                            if int(time.time()) % 3 == 0:
                                time.sleep(1)
                                logger.info("Shell 4 Flapper Its-{}".format(a[1]))
                            # print("Its-{}...should be OPEN/MIDDLE".format(a[1]))

                            if a[1] == "CLOSE":
                                # time.sleep(2)
                                logger.info("Shell 4 Flapper...Its-{}".format(a[1]))
                                ebj_removal_end = datetime.datetime.now().replace(microsecond=0)
                                logger.info("EBJ removal end-{} \n".format(ebj_removal_end))
                                print("EBJ removal end-{} \n".format(ebj_removal_end))
                                break

                if ebj_removal_start == 0:
                    if ebj_removal_start_optional != 0:
                        ebj_removal_start = ebj_removal_start_optional
                        logger.info("captured ebj_removal_start from ebj_removal_start_optional - {}".format(ebj_removal_start))
                    else:
                        logger.info("subtract 5 sec from ebj_removal_end to get ebj_removal_start")
                        ebj_removal_start=ebj_removal_end-datetime.timedelta(seconds=5)
                        logger.info("captured ebj_removal_start-{}".format(ebj_removal_start))

                # PROCESS 2 - EBT MASS FILLING
                if ebj_removal_end != 0 and ebt_mass_filling_start == 0:
                    ebt_mass_filling_start = ebj_removal_end
                    # time.sleep(3)
                    # ebt_mass_filling_end = datetime.datetime.now()
                    logger.info("ebt_mass_filling_start-{} & ebj_removal_end-{}".format(ebt_mass_filling_start,ebj_removal_end))
                    print("ebt_mass_filling_start-{} & ebj_removal_end-{}".format(ebt_mass_filling_start,ebj_removal_end))

                # if ebt_mass_filling_start!=0 and shell_levelling_end==0:

                # while ebt_mass_filling_end == 0:
                if shell_levelling_end == 0:

                    # print("Waiting for 10 sec")
                    # time.sleep(10)
                    # ebt_mass_filling_end = datetime.datetime.now().replace(microsecond=0)

                    try:

                        # Here we are running EBT 4 model to detect person from shell4 EBT camera...

                        # Capture image from live EBT 4 camera
                        _, img = cap_ebt.read()

                        # if img is None:
                        #     break

                        # SKIP FRAMES
                        sec += framerate
                        if sec % 4 != 0:
                            continue

                        # If continuous 5 non frames then reconnect EBT 4 camera...
                        if end_ebt == 1:
                            print("Continuous 5 non frames reconnecting to EBT4 camera.")
                            logger.info("Continuous 5 non frames reconnecting to EBT4 camera.")

                            ip_ebt = "192.168.12.14"
                            cap_ebt = cv2.VideoCapture()
                            cap_ebt.open("rtsp://admin:vert@123@{}/Streaming/channels/1/?tcp".format(ip_ebt))
                            end_ebt = 0
                            none_frame_ebt = 0
                            continue

                        # If Image is blank it will increase frame count
                        if img is None:
                            none_frame_ebt += 1
                            print("None frame - {}".format(none_frame_ebt))
                            logger.info("None frame - {}".format(none_frame_ebt))
                        else:
                            none_frame_ebt = 0

                        # SAVE RESULT & TERMINATE CODE - IF CONSECUTIVE NONE_FRAMES
                        # THAT MEANS...ITS END OF VIDEO
                        if none_frame_ebt == 5:
                            # print("Consecutive {} None frames...save result and terminate the process".format(none_frame_ebt))
                            end_ebt = 1
                            # print("END is -{}".format(end_ebt))

                        if img is None:
                            continue

                        # TO SKIP FRAMES
                        # sec = sec + framerate
                        # if sec%1 != 0:
                        #     continue

                        # RESIZING image FRAME to display...
                        scale_percent = 35
                        width = int(img.shape[1] * scale_percent / 100)
                        height = int(img.shape[0] * scale_percent / 100)
                        # Resize original image to display according to our requirement...
                        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                        height, width, _ = img.shape
                        size = (width, height)

                        # VIDEOWRITER
                        video_file_ebt = "/media/root1/data/ebt_video/Shell_4_EBT_video_{}.avi".format(datetime.datetime.now())
                        if vout_ebt == None:
                            vout_ebt = cv2.VideoWriter(video_file_ebt, cv2.VideoWriter_fourcc(*'DIVX'), fps_ebt,size)
                            logger.info("Shell 4 Ebt Camera videowriter defined")
                            print("Shell 4 Ebt Camera videowriter defined")

                        # DETECTION CHECKING
                        (W, H) = (None, None)
                        if W is None or H is None:
                            (H, W) = img.shape[:2]
                        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                        net2.setInput(blob)
                        ln = net2.getUnconnectedOutLayersNames()
                        layerOutputs = net2.forward(ln)
                        boxes = []
                        confidences = []
                        classIDs = []
                        # idxs = []

                        for output in layerOutputs:

                            for detection in output:

                                scores = detection[5:]
                                classID = np.argmax(scores)
                                confidence = scores[classID]

                                if confidence >= 0.3:

                                    box = detection[0:4] * np.array([W, H, W, H])
                                    (centerX, centerY, width, height) = box.astype("int")
                                    x_a = int(centerX - (width / 2))
                                    y_a = int(centerY - (height / 2))

                                    boxes.append([x_a, y_a, int(width), int(height)])
                                    confidences.append(float(confidence))
                                    classIDs.append(classID)

                        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

                        # Co-ordinate for distance measurement
                        # POINT FOR EBT END (PERSON DISTANCE CALCUTATION)
                        p1, p2 = 600, 425
                        cv2.circle(img, (p1, p2), 5, (100, 100, 200), 7)

                        # print("Shell 4 EBT idxs-{}".format(len(idxs)))
                        if len(idxs) > 0:

                            # print("something detected")

                            for i in idxs.flatten():
                                (x, y) = (boxes[i][0], boxes[i][1])
                                (w, h) = (boxes[i][2], boxes[i][3])
                                cv2.rectangle(img, (x, y), (x + w, y + h), 0, 2)
                                class_name = classes2[classIDs[i]]
                                cv2.putText(img, class_name, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 127, 0), 1)

                                # If any person detected by model then we need to perform below steps...
                                if "person" == class_name:
                                    print("Person detect form EBT camera4")
                                    person_time.append(datetime.datetime.now().replace(microsecond=0))
                                    logger.info("Person detected from EBT camera4 \n person_time-{}".format(person_time))

                                    # person_count+=1
                                    # if person_count>=5:
                                    #     ebt_mass_filling_end = datetime.datetime.now().replace(microsecond=0)
                                    #     print("ebt_mass_filling_end-{} \n".format(ebt_mass_filling_end))
                                    #     logger.info("ebt_mass_filling_end-{} \n".format(ebt_mass_filling_end))
                                    #     break

                                    # logger.info("Person detected form EBT camera")
                                    # # LOGIC FOR CHECKING PERSON POSITION
                                    # # ALSO CHECK PERSON UP/DOWN MOVEMENT
                                    #
                                    # # CAPTURE ebt_mass_filling_end TIMESTAMP
                                    # c1 = x + w / 2
                                    # c2 = y + h / 2
                                    # distance.append(math.sqrt(((p1 - c1) ** 2) + ((p2 - c2) ** 2)))
                                    #
                                    # if len(distance) == 3:
                                    #     down = 0
                                    #     print("person distance -{}".format(distance))
                                    #     logger.info("person distance -{}".format(distance))
                                    #     # for d in distance:
                                    #     if distance[0] > distance[1] > distance[2] and distance[-1] < 70:
                                    #         # down += 1
                                    #         ebt_mass_filling_end = datetime.datetime.now().replace(microsecond=0)
                                    #         print("ebt_mass_filling_end-{} \n".format(ebt_mass_filling_end))
                                    #         logger.info("ebt_mass_filling_end-{} \n".format(ebt_mass_filling_end))
                                    #         break
                                    #     # if down == 3:
                                    #     #     # print(distance)
                                    #     #     # print("END")
                                    #     #     ebt_mass_filling_end = datetime.datetime.now().replace(microsecond=0)
                                    #     #     print("ebt_mass_filling_end-{} \n".format(ebt_mass_filling_end))
                                    #     #     break
                                    #     distance.clear()

                        # VIDEO SAVE
                        vout_ebt.write(img)

                        # cv2.imshow("Shell 4 EBT", img)
                        # cv2.waitKey(1)

                    except Exception as ebt_cam_e:
                        logger.info("Shell 4 EBT CAM EXCEPTION-{}".format(ebt_cam_e))
                        print("Shell 4 EBT CAM EXCEPTION-{}".format(ebt_cam_e))

                # # PROCESS 3 - Shell_levelling
                # if ebt_mass_filling_end != 0 and shell_levelling_start == 0:
                #     shell_levelling_start = ebt_mass_filling_end
                #     logger.info("shell_levelling_start-{} \n".format(shell_levelling_start))
                #     print("shell_levelling_start-{} \n".format(shell_levelling_start))

                # logger.info("checking for shell_levelling_end")
                # logger.info("shell_levelling_end-{}".format(shell_levelling_end))

                # if shell_levelling_end == 0: #and ebt_mass_filling_end!=0:
                if shell_end==0:
                    shell_levelling_end_query = "SELECT Name,Value FROM CVMLAutomation2.dbo.GeneralConfiguation WHERE ShellNo=4";
                    print("checking shell end")
                    # EXECUTE QUERY
                    cursor.execute(shell_levelling_end_query)
                    myresult = cursor.fetchall()

                    # Checking SQL condition to process forward...
                    for a in myresult:
                        # logger.info("Its-{}...should be Shell 4 Tilt".format(a[0]))

                        if a[0] == "Shell 4 Tilt":
                            if int(time.time())%3 == 0:
                                time.sleep(1)
                                logger.info("Shell 4 Tilt Its- {}".format(float(a[1])))

                            # if int(math.ceil(float(a[1]))) in range(-7, 7):
                            # if int(math.ceil(float(a[1]))) >= 1.5:
                            if float(a[1]) >= -1.0:
                                logger.info("Shell 4 Tilt Its- {}".format(float(a[1])))
                                # CHECK IF ANY POURING START DETECTED
                                if top_pouring==1:
                                    logger.info("top pouring altready started before shell levelling end\n")
                                    # BEFORE SHELL LLEVELLING END IF HM_POSITIONING ENDED & HM POURING STARTED...
                                    if hm_positioning_end!=0:
                                        logger.info("hm_positioning_end/hm_pouring_start was already captured\n")
                                        logger.info("taking -5 sec from hm_positioning_end as shell_levelling_end")
                                        shell_levelling_end=(hm_positioning_end-datetime.timedelta(seconds=5)).replace(microsecond=0)
                                    else:
                                        shell_levelling_end = datetime.datetime.now().replace(microsecond=0)
                                        logger.info("normally captured shell_levelling_end")

                                elif launder_pouring==1:
                                    logger.info("launder pouring altready started before shell levelling end\n")
                                    # BEFORE SHELL LLEVELLING END IF HM_POSITIONING ENDED & HM POURING STARTED...
                                    if top_lance_positioning_end!=0:
                                        logger.info("top lance positioning end was already captured\n")
                                        logger.info("taking -5 sec from top_lance_positioning_end as shell_levelling_end")
                                        shell_levelling_end=(top_lance_positioning_end-datetime.timedelta(seconds=5)).replace(microsecond=0)
                                    else:
                                        shell_levelling_end = datetime.datetime.now().replace(microsecond=0)
                                        logger.info("normally captured shell_levelling_end")

                                else:
                                    logger.info("No pouring started yet")
                                    shell_levelling_end=datetime.datetime.now().replace(microsecond=0)
                                    logger.info("shell_levelling_end-{}".format(shell_levelling_end))

                                logger.info("shell_levelling_end-{} \n".format(shell_levelling_end))
                                print("shell_levelling_end-{} \n".format(shell_levelling_end))
                                shell_end=1
                                break

                # IF SHELL END...CHECK IF EBT WAS ENDED OR NOT...
                if shell_end == 1 and ebt_mass_filling_end == 0:

                    if shell_levelling_end != 0:

                        if len(person_time) == 0:
                            # ebt_mass_filling_end = shell_levelling_end-datetime.timedelta(seconds=2)
                            # shell_levelling_start = ebt_mass_filling_end
                            # GET DIFFERENCE BETWEEN EBT_START & SHELL_END
                            time_difference = int(abs(shell_levelling_end-ebt_mass_filling_start).total_seconds())
                            logger.info("Time difference between ebt_mass_filling_start & shell_levelling -end is - {}".format(time_difference))

                            if time_difference>1:
                                time_add = time_difference/2.0
                                ebt_mass_filling_end = (ebt_mass_filling_start+datetime.timedelta(seconds=time_add)).replace(microsecond=0)
                                shell_levelling_start = ebt_mass_filling_end
                                logger.info("Added {} in ebt_mass_filling_start to get ebt_mass_filling_end & shell_levelling_start".format(time_add))

                            else:
                                shell_levelling_end = (shell_levelling_end+datetime.timedelta(seconds=2)).replace(microsecond=0)
                                time_difference = int(abs(shell_levelling_end - ebt_mass_filling_start).total_seconds())
                                logger.info("added 2 sec to shell_levelling_end time\n and now time difference between ebt_mass_filling_start & shell_levelling -end is - {}".format(time_difference))
                                time_add = time_difference / 2.0
                                ebt_mass_filling_end = (ebt_mass_filling_start + datetime.timedelta(seconds=time_add)).replace(microsecond=0)
                                shell_levelling_start = ebt_mass_filling_end
                                logger.info("added {} in ebt_mass_filling_start to get ebt_mass_filling_end & shell_levelling_start".format(time_add))


                        elif len(person_time)>1:
                            ind=int(len(person_time)*2/3)
                            ebt_mass_filling_end = person_time[ind]
                            shell_levelling_start = ebt_mass_filling_end
                            logger.info("Captured ebt_mass_filling_end & shell_levelling_start")
                            print("Captured ebt_mass_filling_end & shell_levelling_start")
                        else:
                            ebt_mass_filling_end = person_time[-1]
                            shell_levelling_start = ebt_mass_filling_end
                            logger.info("Captured ebt_mass_filling_end & shell_levelling_start")
                            print("Captured ebt_mass_filling_end & shell_levelling_start")

            # except Exception as ebt_e:
            #     print("Shell 4 EBT exception-{}".format(ebt_e))
            #     logger.info("Shell 4 EBT exception-{}".format(ebt_e))

                logger.info("Shell 4 EBT Camera is Done !")
                print("Shell 4 EBT Camera is Done !")

                # f_name=datetime.datetime.now()
                # touch.touch("/home/root1/CVML_2/Result_Txt/ebt_result_{}.txt".format(f_name))
                # with open("/home/root1/CVML_2/Result_Txt/result_{}.txt".format(f_name), "w") as f:
                #     f.write("EBJ - Start-{} & End-{}".format(ebj_removal_start,ebj_removal_end))
                #     f.write("\n")
                #     f.write("EBT MASS FILLING - Start-{} & End-{}".format(ebt_mass_filling_start,ebt_mass_filling_end))
                #     f.write("\n")
                #     f.write("SHELL LEVELLING - Start-{} & End-{}".format(shell_levelling_start,shell_levelling_end))
                #     f.write("\n")
                #
                # end_cycle=1
                # logger.info("Result Stored , end_cycle-{}...Hold 30 Sec".format(end_cycle))
                # time.sleep(30)
                # logger.info("Done !")


                # Connect shel 4 FRONT VIEW camera

                # VIDEO

                # TOP POURING
                # cap_front = cv2.VideoCapture("/media/root1/data/front_video/Shell_4_front_video_2021-08-17 19:51:53.535546.avi")
                # LAUNDER POURING
                # cap_front = cv2.VideoCapture("/media/root1/data/front_video/Shell_4_front_video_2021-08-18 08:26:14.833034.avi")

                # HTTP
                ip_front = "192.168.12.15"
                while connected_front != 1:
                    try:
                        logger.info("Trying to connect front camera...")
                        cam = Client('http://{}'.format(ip_front), 'admin', 'vert@123')
                        logger.info("Connected !")
                        connected_front = 1

                    except Exception as e1:
                        logger.info("Its Exception while connecting - {}".format(e1))
                        logger.info("Retrying...")
                        continue

                # RTSP

                # ip_front = "192.168.12.15"
                # cap_front = cv2.VideoCapture()
                # cap_front.open("rtsp://admin:vert@123@{}/Streaming/channels/1/?tcp".format(ip_front))
                # logger.info("camera connected shell 4 frontview")
                # print("Camera connected...Shell 4 front view")


                recent_proc_time=time.time()

                # while end_cycle != 1:

                    # try:
                # # Reading image from live camera
                vid = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
                bytes = b''
                with open('screen1.jpg', 'wb') as f:
                    for chunk in vid.iter_content(chunk_size=1024):
                        bytes += chunk
                        a = bytes.find(b'\xff\xd8')
                        b = bytes.find(b'\xff\xd9')
                        if a != -1 and b != -1:
                            jpg = bytes[a:b + 2]
                            bytes = bytes[b + 2:]
                            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                            # Reconnect camera when 5 non frames arrives
                            if end_front == 1:
                                # logger.info("Reconnect shell 4 front view camera")
                                # print("Reconnect Shell 4 front view camera")
                                # ip_front = "192.168.12.15"
                                # cap_front = cv2.VideoCapture()
                                # cap_front.open("rtsp://admin:vert@123@{}/Streaming/channels/1/?tcp".format(ip_front))
                                # none_frame_front = 0
                                # end_front = 0
                                logger.info("continue none frames...end_fron-{}".format(end_front))
                                break
                                # continue

                            if img is None:
                                none_frame_front += 1
                                logger.info("None frame - {}".format(none_frame_front))
                                print("shell 4 front camera None frame - {}".format(none_frame_front))
                            else:
                                none_frame_front = 0

                            # SAVE RESULT & TERMINATE CODE - IF CONSECUTIVE NONE_FRAMES
                            # THAT MEANS...ITS END OF VIDEO
                            if none_frame_front == 5:
                                logger.info("shell 4 front camera Consecutive {} None frames".format(none_frame_front))
                                print("shell 4 front camera Consecutive {} None frames".format(none_frame_front))
                                end_front = 1
                                # logger.info("END is -{}".format(end_front))
                                # print("END is -{}".format(end_front))

                            if img is None:
                                continue

                            # TO SKIP FRAMES
                            # sec = sec + framerate
                            # if sec % 5 != 0:
                            #     continue

                            logger.info("Alive-{}".format(datetime.datetime.now()))

                            # RESIZING image FRAME to display...
                            scale_percent = 35
                            width = int(img.shape[1] * scale_percent / 100)
                            height = int(img.shape[0] * scale_percent / 100)

                            # Resize original image to display according to our requirement...
                            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                            height, width, _ = img.shape
                            size = (width, height)

                            # VIDEOWRITER
                            # video_file_front = "/home/root1/CVML_2/Model_Logs/shell4/testing/front_video_{}.avi".format(datetime.datetime.now())
                            video_file_front = "/media/root1/data/front_video/Shell_4_front_video_{}.avi".format(datetime.datetime.now())
                            if vout_front == None:

                                logger.info("Shell 4 Front Camera videowriter defined")
                                print("Shell 4 Front Camera videowriter defined")
                                vout_front = cv2.VideoWriter(video_file_front, cv2.VideoWriter_fourcc(*'DIVX'), fps_front, size)


                            # # POINT FOR TOP LANCE distance...
                            p1, p2 = 600, 170
                            cv2.circle(img, (p1, p2), 5, (50, 100, 200), 5)

                            # POINT FOR LAUNDER INSERTION distance...
                            q1, q2 = 575, 375
                            cv2.circle(img, (q1, q2), 5, (200, 150, 200), 5)



                            # DETECTION CHECKING
                            (W, H) = (None, None)
                            if W is None or H is None:
                                (H, W) = img.shape[:2]

                            blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                            net1.setInput(blob)
                            ln = net1.getUnconnectedOutLayersNames()
                            layerOutputs = net1.forward(ln)

                            boxes = []
                            confidences = []
                            classIDs = []
                            # idxs = []

                            for output in layerOutputs:

                                for detection in output:

                                    scores = detection[5:]
                                    classID = np.argmax(scores)
                                    confidence = scores[classID]

                                    if confidence >= 0.3:
                                        box = detection[0:4] * np.array([W, H, W, H])
                                        (centerX, centerY, width, height) = box.astype("int")
                                        x_a = int(centerX - (width / 2))
                                        y_a = int(centerY - (height / 2))

                                        boxes.append([x_a, y_a, int(width), int(height)])
                                        confidences.append(float(confidence))
                                        classIDs.append(classID)

                            idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

                            # To end cycle in rare case
                            # After top pouring started...process didnt execute further...end the cycle

                            # t2=time.time()
                            # if top_pouring == 1:
                            #     if hm_pouring_start==0: # and  hm_positioning_start==0:
                            #         if t2-t1>=900:
                            #             logger.info("After top pouring started...process didnt execute further...end the cycle")
                            #             t = datetime.datetime.now()
                            #             print("After top pouring started...process didnt execute further...end the cycle-{}".format(t))
                            #             end_cycle=1
                            #             logger.info("end_cycle-{}".format(end_cycle))
                            #
                            # # After launder pouring started...process didnt execute further...end the cycle"
                            # if launder_pouring == 1:
                            #     if launder_insertion_start==0:
                            #         if t2-t1>=900:
                            #             logger.info("After launder pouring started...process didnt execute further...end the cycle")
                            #             # print("After launder pouring started...process didnt execute further...end the cycle")
                            #             end_cycle=1
                            #             logger.info("end_cycle-{}".format(end_cycle))

                            # Check for hm_pouring_enonly if either top or launder pouring flag is 1
                            if top_pouring == 1 or launder_pouring == 1:
                                # logger.info("checking for end_hm_pouring")

                                if len(idxs) > 0:

                                    # FOR TOP & LAUNDER POURING
                                    # HM POURING END ... WHEN BUCKET IS OUT OF SIGHT

                                    # TO CHECK END OF HM_POURING FOR TOP POURING
                                    if top_pouring == 1 and hm_pouring_end == 0 and hm_pouring_start != 0:
                                        logger.info("For Top Pouring checking hm_pouring_end")
                                        class_names = []

                                        for i in idxs.flatten():
                                            # # print("1-{}".format(type(idxs)))
                                            class_names.append(classes1[classIDs[i]])

                                        # If bucket not detected from camera for certain time mean hm pouring end...
                                        if "bucket" not in class_names and "bucket plus" not in class_names:
                                            end_hm_pouring += 1
                                        else:
                                            end_hm_pouring = 0

                                        # This the condition where we will get top lance positing time...
                                        if end_hm_pouring >= 20:

                                            hm_pouring_end = datetime.datetime.now().replace(microsecond=0)
                                            # if top_lance_positioning_start == 0:
                                            top_lance_positioning_start = hm_pouring_end
                                            print("For Top pouring...hm_pouring_end...top_lance_positioning_start {},{}".format(hm_pouring_end,top_lance_positioning_start))
                                            logger.info("For Top pouring...hm_pouring_end...top_lance_positioning_start")

                                            # logger.info(
                                            #     "hm_pouring_end-{}...top_lance_positioning_start (already)-{}".format(
                                            #         hm_pouring_end, top_lance_positioning_start))
                                            # print("hm_pouring_end-{}...top_lance_positioning_start (already)-{}".format(
                                            #     hm_pouring_end,
                                            #     top_lance_positioning_start))

                                    # TO CHECK END OF HM_POURING FOR LAUNDER POURING
                                    if launder_pouring == 1 and hm_pouring_end == 0 and hm_pouring_start != 0:
                                        logger.info("For Launder Pouring checking hm_pouring_end")
                                        # print("Inside Launder Pouring...Checking hm_pouring_end...if bucket is out of sight...hm_positioning_end-{}".format(hm_positioning_end))
                                        class_names = []
                                        # # print("2-{}".format(type(idxs)))

                                        for i in idxs.flatten():
                                            (x, y) = (boxes[i][0], boxes[i][1])
                                            (w, h) = (boxes[i][2], boxes[i][3])
                                            cv2.rectangle(img, (x, y), (x + w, y + h), 0, 2)
                                            class_name = classes1[classIDs[i]]
                                            class_names.append(classes1[classIDs[i]])
                                            cv2.putText(img, class_name, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 127, 0), 1)

                                        # If bucket not detected from camera for certain time mean hm_pouring_end...
                                        if "bucket" not in class_names:
                                            # # print("end hm_pouring-{}".format(end_hm_pouring))
                                            end_hm_pouring += 1
                                            logger.info("No Bucket...end_hm_pouring-{}".format(end_hm_pouring))
                                        else:
                                            end_hm_pouring = 0

                                        # This condition we will get HM pouring end for launder pouring...
                                        if end_hm_pouring >= 20 and hm_positioning_end != 0:
                                            hm_pouring_end = datetime.datetime.now().replace(microsecond=0)
                                            end_cycle = 1

                                            pro_time.append(str(hm_pouring_end))
                                            # # print("hm_pouring_end-{}".format(hm_pouring_end))
                                            print("For Launder pouring...hm_pouring_end...also cycle 6end")
                                            logger.info("hm_pouring_end-{}".format(hm_pouring_end))
                                            logger.info("For Launder pouring...hm_pouring_end...also cycle end")

                                            # STORE ALL TIMESTAMPS IN DICT
                                            # pro=[top_lance_positioning_start,top_lance_positioning_end,launder_insertion_start,launder_insertion_end,hm_positioning_start,hm_positioning_end,hm_pouring_start,hm_pouring_end]
                                            # pro_name=["top_lance_positioning_start","top_lance_positioning_end","launder_insertion_start","launder_insertion_end","hm_positioning_start","hm_positioning_end","hm_pouring_start","hm_pouring_end"]
                                            # t={}
                                            # # # print(len(pro_name),len(pro_time))
                                            # for i in range(len(pro_time)):
                                            #     t[pro_name[i]]=pro_time[i]
                                            # # print("Cycle Timestamp - {}".format(t))

                                elif len(idxs) == 0:

                                    # Model has not detection anything but we are checking HM pouring end condition...
                                    if launder_pouring == 1 and hm_pouring_end == 0 and hm_pouring_start != 0:
                                        logger.info("No detection...checking hm_pouring_end-{}".format(end_hm_pouring))
                                        end_hm_pouring += 1

                                        if end_hm_pouring >= 20 and hm_pouring_end==0:
                                            hm_pouring_end = datetime.datetime.now().replace(microsecond=0)
                                            logger.info("No detection...hm_pouring_end-{}".format(hm_pouring_end))
                                            print("END Cycle")
                                            end_cycle = 1
                                            logger.info("end_cycle-{}".format(end_cycle))

                                    if top_pouring == 1 and hm_pouring_end == 0 and hm_pouring_start != 0:
                                        end_hm_pouring += 1
                                        logger.info("No detection...checking end_hm_pouring-{}".format(end_hm_pouring))

                                        if end_hm_pouring >= 20 and hm_pouring_end==0:
                                            hm_pouring_end = datetime.datetime.now().replace(microsecond=0)

                                            # if top_lance_positioning_start == 0:
                                            top_lance_positioning_start = hm_pouring_end

                                            print("For Top pouring...hm_pouring_end...top_lance_positioning_start")
                                            logger.info("For Top pouring...hm_pouring_end...top_lance_positioning_start")

                                            # logger.info("hm_pouring_end-{}...top_lance_positioning_start (already)-{}".format(hm_pouring_end, top_lance_positioning_start))
                                            # print("hm_pouring_end-{}...top_lance_positioning_start (already)-{}".format(hm_pouring_end, top_lance_positioning_start))

                            # A
                            # NON-CYCLIC PROCESS (SCRAP CHARGING) END CHECK
                            if scrap_charging == 1 and scrap_charging_start != 0 and scrap_charging_end == 0:
                                temp = []

                                # If model has detect some thing
                                if len(idxs) == 0:
                                    no_scrap_bucket += 1

                                elif len(idxs) > 0:
                                    for i in idxs.flatten():
                                        class_name = classes1[classIDs[i]]
                                        temp.append(class_name)

                                    # If scrap bucket not in the detection model
                                    if "scrap bucket" not in temp:
                                        no_scrap_bucket += 1
                                    else:
                                        no_scrap_bucket = 0

                            # If scrap bucket is not in the temp list means we will get scrap charging end time...
                            if no_scrap_bucket == 10 and scrap_charging_end == 0:
                                scrap_charging_end = datetime.datetime.now().replace(microsecond=0)
                                print("scrap_charging_end-{}".format(scrap_charging_end))
                                logger.info("scrap_charging_end-{}".format(scrap_charging_end))

                            # B
                            # NON-CYCLIC PROCESS (SLUG REMOVAL) END CHECK
                            if slug_removal == 1 and slug_removal_start != 0 and slug_removal_end == 0:
                                temp = []

                                if len(idxs) == 0:
                                    no_slug_car += 1

                                elif len(idxs) > 0:
                                    for i in idxs.flatten():
                                        class_name = classes1[classIDs[i]]
                                        temp.append(class_name)

                                    # If slug car not in the detection model...
                                    if "slug car" not in temp:
                                        no_slug_car += 1
                                    else:
                                        no_slug_car = 0

                            # If slug car is not there in temp list means we will get slug removal end time...
                            if no_slug_car == 10 and slug_removal_end == 0 and slug_removal_start != 0:
                                slug_removal_end = datetime.datetime.now().replace(microsecond=0)
                                print("slug_removal_end-{}".format(slug_removal_end))
                                logger.info("slug_removal_end-{}".format(slug_removal_end))

                            # C
                            # NON-CYCLIC PROCESS (SLUG REMOVAL) END CHECK
                            if fettling == 1 and fettling_start != 0 and fettling_end == 0:
                                temp = []
                                # If model has detect some thing
                                if len(idxs) == 0:
                                    no_fettling_bucket += 1
                                elif len(idxs) > 0:
                                    for i in idxs.flatten():
                                        class_name = classes1[classIDs[i]]
                                        temp.append(class_name)

                                    # If scrap bucket not in the detection model
                                    if "fettling bucket" not in temp:
                                        no_fettling_bucket += 1
                                    else:
                                        no_fettling_bucket = 0

                            # If fettling bucket is not in the temp list means we will get fettling end time...
                            if no_fettling_bucket == 10 and fettling_end == 0:
                                fettling_end = datetime.datetime.now().replace(microsecond=0)
                                print("fettling_end-{}".format(fettling_end))
                                logger.info("fettling_end-{}".format(fettling_end))

                            # D
                            # NON-CYCLIC PROCESS (GUNNING) END CHECK
                            if gunning == 1 and gunning_start != 0 and gunning_end == 0:
                                temp = []
                                # If model has detect some thing
                                if len(idxs) == 0:
                                    no_gunning += 1
                                elif len(idxs) > 0:
                                    for i in idxs.flatten():
                                        class_name = classes1[classIDs[i]]
                                        temp.append(class_name)

                                    # If scrap bucket not in the detection model
                                    if "person" not in temp:
                                        no_gunning += 1
                                    else:
                                        no_gunning = 0

                            # If scrap bucket is not in the temp list means we will get scrap charging end time...
                            if no_gunning == 10 and gunning_end == 0:
                                gunning_end = datetime.datetime.now().replace(microsecond=0)
                                print("gunning_end-{}".format(gunning_end))
                                logger.info("gunning_end-{}".format(gunning_end))

                            if len(idxs) == 0:
                                scrap_count = 0
                                slug_count = 0
                                # launder_count = 0
                                top_count = 0
                            if len(idxs)>0:
                                end_hm_pouring=0
                                logger.info("end_hm_pouring-{}".format(end_hm_pouring))

                            if launder_pouring == 1:
                                logger.info("inside launder pouring")
                                logger.info("check blowing/arcing")
                                check_end_cycle = is_cycle_end()

                                if check_end_cycle == 1:
                                    if top_lance_positioning_end == 0:
                                        if len(top_lance_positioning_list) > 0:
                                            top_lance_positioning_end = top_lance_positioning_list[-1]
                                            logger.info("Blowing/Arcing TRUE but top_lance_end is 0...captured now-{}".format(top_lance_positioning_end))
                                        elif len(launder_car_insertion_list) > 0:
                                            top_lance_positioning_end = launder_car_insertion_list[0]
                                            logger.info("Blowing/Arcing TRUE but top_lance_end is 0...captured now-{}".format(top_lance_positioning_end))

                                    if launder_insertion_start == 0 and top_lance_positioning_end != 0:
                                        launder_insertion_start = top_lance_positioning_end
                                        logger.info("Blowing/Arcing TRUE but launder_insertion_start is 0...captured now-{}".format(launder_insertion_start))

                                    if launder_insertion_end == 0:
                                        if len(launder_car_insertion_list) > 0:
                                            launder_insertion_end = launder_car_insertion_list[-1]
                                            logger.info("Blowing/Arcing TRUE but launder_insertion_end is 0...captured now-{}".format(launder_insertion_end))

                                        elif len(hm_positioning_list) > 0:
                                            launder_insertion_end = hm_positioning_list[0]
                                            logger.info("Blowing/Arcing TRUE but launder_insertion_end is 0...captured now-{}".format(launder_insertion_end))

                                    if hm_positioning_start == 0 and launder_insertion_end != 0:
                                        hm_positioning_start = launder_insertion_end
                                        logger.info("Blowing/Arcing TRUE but hm_positioning_start is 0...captured now-{}".format(hm_positioning_start))

                                    if hm_positioning_end == 0:
                                        if len(hm_positioning_list) > 0:
                                            hm_positioning_end = hm_positioning_list[-1]
                                            logger.info("Blowing/Arcing TRUE but hm_positioning_end is 0...captured now-{}".format(hm_positioning_end))

                                    if hm_pouring_start == 0 and hm_positioning_end != 0:
                                        hm_pouring_start = hm_positioning_end
                                        logger.info("Blowing/Arcing TRUE but hm_pouring_start is 0...captured now-{}".format(hm_pouring_start))

                                    if hm_pouring_end == 0:
                                        if len(bucket_plus_list) > 0:
                                            hm_pouring_end = bucket_plus_list[-1]
                                            logger.info("Blowing/Arcing TRUE but hm_pouring_end is 0...captured now-{}".format(hm_pouring_end))

                                        else:
                                            hm_pouring_end = datetime.datetime.now().replace(microsecond=0)
                                            logger.info("Blowing/Arcing TRUE but hm_pouring_end is 0...captured now-{}".format(hm_pouring_end))

                                    end_cycle = 1
                                    logger.info("Its blowing/arcing TRUE...end the cycle")
                                    blowing_true = datetime.datetime.now().replace(microsecond=0)
                                    break


                            if top_pouring == 1:
                                logger.info("inside top pouring")
                                logger.info("check blowing/arcing")
                                check_end_cycle = is_cycle_end()

                                if check_end_cycle == 1:
                                    if hm_positioning_end == 0 and hm_pouring_start == 0:
                                        if len(hm_positioning_list) > 0:
                                            hm_positioning_end = hm_positioning_list[-1]
                                            hm_pouring_start = hm_positioning_end
                                    if hm_pouring_end == 0 and len(top_lance_positioning_list) > 0:
                                        hm_pouring_end = top_lance_positioning_list[0]

                                    if top_lance_positioning_end == 0:
                                        if len(top_lance_positioning_list) > 0:
                                            top_lance_positioning_end = top_lance_positioning_list[-1]
                                        else:
                                            top_lance_positioning_end = datetime.datetime.now().replace(microsecond=0)

                                        logger.info("Blowing/arcing TRUE...top lance positioning was 0...captured now-{}".format(top_lance_positioning_end))

                                    if slug_removal_start != 0 and slug_removal_end == 0:
                                        slug_removal_end = datetime.datetime.now().replace(microsecond=0)
                                        logger.info("captured slug removal end")

                                    end_cycle = 1
                                    logger.info("Its blowing/arcing TRUE...end the cycle")
                                    blowing_true = datetime.datetime.now().replace(microsecond=0)
                                    break

                            # THIS IS FOR GUNNING (D/NON CYCLIC PROCESS)
                            # CHECKING START OF GUNNING BASED ON WHETHER TWO PERSONS ARE DETECTED OR NOT
                            # THIS IS OUTSIDE FOR LOOP (for i in idxs.flatten) CZ WE WANT TO CHECK THIS ONLY ONCE FOR EACH FRAME
                            # D - GUNNING
                            if len(idxs)>=2:
                                temp=[]
                                for j in idxs.flatten():
                                    temp.append(classes1[classIDs[j]])
                                if temp.count("person")>=2 and gunning==0:
                                    # fettling_bucket_count += 1
                                    # if fettling_bucket_count > 2:
                                    gunning = 1
                                    gunning_start = datetime.datetime.now().replace(microsecond=0)
                                    logger.info("gunning_start-{}".format(gunning_start))

                            # IF ANY OBJECT IS DETECTED
                            if len(idxs) > 0:
                                # # print("3-{}".format(type(idxs)))
                                # logger.info("something detected by model")

                                for i in idxs.flatten():

                                    # # print("3-{}".format(type(idxs)))
                                    (x, y) = (boxes[i][0], boxes[i][1])
                                    (w, h) = (boxes[i][2], boxes[i][3])
                                    cv2.rectangle(img, (x, y), (x + w, y + h), 0, 2)
                                    class_name = classes1[classIDs[i]]
                                    cv2.putText(img, class_name, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 127, 0), 1)

                                    # A - SCRAP CHARGING process...
                                    if class_name == "scrap bucket":

                                        if scrap_charging != 1:
                                            scrap_count += 1

                                            if scrap_count >= 5:
                                                scrap_charging = 1

                                                # If our model has detect scrap bucket that means we will get scrap charging start time...
                                                if shell_levelling_end != 0:
                                                    scrap_charging_start = shell_levelling_end
                                                    logger.info("scrap charging_start-{}...shell levelling end-{}".format(scrap_charging_start, shell_levelling_end))
                                                    print("scrap charging_start-{}...shell levelling end-{}".format(scrap_charging_start, shell_levelling_end))
                                                # else:
                                                #     scrap_charging_start=datetime.datetime.now().replace(microsecond=0)

                                    # B - SLUG REMOVAL Process...
                                    if class_name == "slug car":
                                        print("slug")

                                        if slug_removal != 1:
                                            slug_count += 1

                                            if slug_count >= 2:
                                                slug_removal = 1

                                                # If our model has detect slug car that means we will get slug removal start time...
                                                # if shell_levelling_end != 0:
                                                slug_removal_start = datetime.datetime.now().replace(microsecond=0)

                                                # slug_removal_start=shell_levelling_end
                                                logger.info("slug removal_start-{}".format(slug_removal_start))
                                                print("slug removal_start-{}".format(slug_removal_start))

                                                # slug_removal_start=shell_levelling_end
                                                # logger.info("slug removal_start-{} ...shell_levelling_end-{}".format(slug_removal_start, shell_levelling_end))
                                                # print("slug removal_start-{} ...shell_levelling_end-{}".format(slug_removal_start, shell_levelling_end))


                                            # else:
                                                #     slug_removal_start = datetime.datetime.now().replace(microsecond=0)
                                                #     logger.info("shell levelling end was 0...slug removal_start-{} ...shell_levelling_end-{}".format(slug_removal_start,shell_levelling_end))
                                                #     print("shell levelling end was 0...slug removal_start-{} ...shell_levelling_end-{}".format(slug_removal_start,shell_levelling_end))

                                    # C - FETTLING
                                    if class_name=="fettling bucket":
                                        fettling_bucket_count+=1
                                        if fettling_bucket_count>2:
                                            fettling=1
                                            fettling_start=datetime.datetime.now().replace(microsecond=0)
                                            logger.info("fettling_start-{}".format(fettling_start))



                                    if class_name == 'bucket':
                                        bucket_count += 1
                                        hm_positioning_list.append(datetime.datetime.now().replace(microsecond=0))
                                        logger.info("bucket count-{}".format(bucket_count))
                                    if class_name == "top lance":
                                        top_lance_positioning_list.append(datetime.datetime.now().replace(microsecond=0))
                                    if class_name == "launder car":
                                        launder_car_insertion_list.append(datetime.datetime.now().replace(microsecond=0))
                                    if class_name == "bucket plus":
                                        bucket_plus_count += 1
                                        bucket_plus_list.append(datetime.datetime.now().replace(microsecond=0))
                                        logger.info("bucket plus count -{}".format(bucket_plus_count))


                                    # 4 Top Pouring Process...
                                    # First condition for top pouring is model has to detect bucket...
                                    if class_name == "bucket" or class_name == "bucket plus":
                                        # bucket_count += 1
                                        # logger.info("bucket_count-{}".format(bucket_count))
                                        top_count += 1
                                        if top_count >= 3:
                                            if launder_pouring != 1 and top_pouring != 1:
                                                top_pouring = 1
                                                # Taking this time to calculate
                                                t1 = time.time()
                                                print("It will be top pouring")
                                                logger.info("It will be top pouring")

                                    # 4 Launder Pouring process...
                                    cur_tim = time.time()

                                    # If model has detect launder car or top lance that means it's launder pouring...
                                    if class_name == 'launder car' or class_name == "top lance":
                                        launder_count += 1
                                        if launder_count >= 5:
                                            if top_pouring != 1 and launder_pouring != 1:  # and cur_tim - recent_proc_time < 100.0 :
                                                launder_pouring = 1
                                                t1 = time.time()
                                                print("It will be launder pouring")
                                                logger.info("It will be launder pouring")


                                    # CHECK IF ANY BUCKET_PLUS DETECTED TILL 50 FRAMES FROM BUCKET ARRIVAL
                                    if bucket_count<20 and bucket_plus==0:
                                        # logger.info("bucket count - {}".format(bucket_count))
                                        logger.info("checking bucket plus")
                                        if class_name=="bucket plus":
                                            bucket_plus=1
                                            logger.info("Its bucket_plus - {} \n will check pouring".format(bucket_plus))
                                    # TO CROSS CHECK launder / top POURING
                                    # if class_name == 'bucket':
                                    if bucket_plus==1 and pouring_check==0 and bucket_count>2:
                                        pouring_check=1
                                        logger.info("check pouring")
                                        # bucket_area.append(w * h)
                                        # print("Bucket Area - {}".format(bucket_area))
                                        # if launder_pouring == 1:
                                        #     logger.info("Its Launder Pouring\n")
                                        # elif top_pouring == 1:
                                        #     logger.info("Its Top Pouring\n")
                                        # # logger.info("Bucket Area - {}".format(bucket_area))
                                        # if len(bucket_area)>10 and pouring_check==0:
                                        #     average_bucket_area=np.mean(bucket_area)
                                        #     logger.info("Average Bucket Area - {}".format(average_bucket_area))
                                        #     pouring_check = 1
                                        #     if average_bucket_area< 100000.0:
                                        #         logger.info("average is < 100000 ")
                                        if launder_pouring==1:
                                            logger.info("launder pouring\n")
                                            logger.info("Model declared process as Launder Pouring...But Bucket is detected for Top Pouring\n")
                                            logger.info("lets reset launder pouring and switch to top pouring\n")
                                            top_pouring=1
                                            launder_pouring=0
                                            logger.info("top_pouring-{} & launder_pouring-{}".format(top_pouring,launder_pouring))

                                            logger.info("time values\n")
                                            logger.info("{} & {}\n {} & {}\n {} & {}\n {} & {}\n".format(top_lance_positioning_start, top_lance_positioning_end,launder_insertion_start, launder_insertion_end, hm_positioning_start,
                                                hm_positioning_end, hm_pouring_start, hm_pouring_end))

                                            logger.info("assigning time values\n")
                                            hm_positioning_start=shell_levelling_end
                                            logger.info("assigned hm_positioning_start = shell_levelling_end - {}".format(hm_pouring_start))
                                            top_lance_positioning_start=0
                                            top_lance_positioning_end=0
                                            launder_insertion_start=0
                                            launder_insertion_end=0
                                            hm_pouring_start=0
                                            hm_pouring_end=0
                                            hm_positioning_end=0
                                            logger.info("time values\n top lance, launder, hm_position & hm_pouring\n")
                                            logger.info("{} & {}\n {} & {}\n {} & {}\n {} & {}\n".format(top_lance_positioning_start, top_lance_positioning_end,launder_insertion_start, launder_insertion_end, hm_positioning_start,
                                                hm_positioning_end, hm_pouring_start, hm_pouring_end))

                                        elif top_pouring==1:
                                            logger.info("Its top pouring")

                                        logger.info("\ncheck pouring done ")

                                    elif bucket_count>20 and pouring_check==0:
                                        # logger.info("average is > 100000")
                                        pouring_check=1
                                        logger.info("pouring check")
                                        if top_pouring==1 and len(launder_car_insertion_list)>0:
                                            logger.info("top_pouring going on")
                                            logger.info("Model declared process as Top Pouring...But Bucket is detected for Launder Pouring\n")
                                            logger.info("lets reset top pouring and switch to launder pouring\n")
                                            top_pouring = 0
                                            launder_pouring = 1
                                            logger.info("top_pouring-{} & launder_pouring-{}".format(top_pouring,launder_pouring))

                                            logger.info("time values\n")
                                            logger.info("{} & {}\n {} & {}\n {} & {}\n {} & {}\n".format(top_lance_positioning_start, top_lance_positioning_end,launder_insertion_start, launder_insertion_end,
                                                hm_positioning_start,hm_positioning_end, hm_pouring_start, hm_pouring_end))

                                            logger.info("assigning time values\n")
                                            top_lance_positioning_start = shell_levelling_end
                                            logger.info("assigned top_lance_positioning_start = shell_levelling_end - {}".format(top_lance_positioning_start))

                                            if len(launder_car_insertion_list)>0:
                                                top_lance_positioning_end = launder_car_insertion_list[0]
                                                launder_insertion_start = top_lance_positioning_end
                                                logger.info("FROM LAUNDER LIST captured top lance positioning end & launder insertion start - {}".format(top_lance_positioning_end))

                                            if len(hm_positioning_list)>0:
                                                launder_insertion_end = hm_positioning_list[0]
                                                hm_positioning_start = launder_insertion_end
                                                logger.info("FROM HM POSITIONING LIST captured launder insertion end & hm positioning start - {}".format(launder_insertion_end))

                                            hm_positioning_end=0
                                            hm_pouring_start=0
                                            hm_pouring_end=0

                                            logger.info("time values\n top lance, launder, hm_position & hm_pouring\n")
                                            logger.info("{} & {}\n {} & {}\n {} & {}\n {} & {}\n".format(top_lance_positioning_start, top_lance_positioning_end,launder_insertion_start, launder_insertion_end,
                                                hm_positioning_start,hm_positioning_end, hm_pouring_start, hm_pouring_end))

                                        elif launder_pouring==1:
                                            logger.info("launder_pouring going on OR it is top pouring only")

                                        logger.info("\ncheck pouring done ")

                                    if top_pouring == 1:

                                        # logger.info("inside top pouring")
                                        # logger.info("check blowing/arcing")
                                        # check_end_cycle=is_cycle_end()
                                        #
                                        # if check_end_cycle == 1:
                                        #     if hm_positioning_end == 0 and hm_pouring_start == 0:
                                        #         if len(hm_positioning_list)>0:
                                        #             hm_positioning_end = hm_positioning_list[-1]
                                        #             hm_pouring_start = hm_positioning_end
                                        #     if hm_pouring_end == 0 and len(top_lance_positioning_list)>0:
                                        #         hm_pouring_end = top_lance_positioning_list[0]
                                        #
                                        #     if top_lance_positioning_end == 0:
                                        #         if len(top_lance_positioning_list)>0:
                                        #             top_lance_positioning_end = top_lance_positioning_list[-1]
                                        #         else:
                                        #             top_lance_positioning_end=datetime.datetime.now().replace(microsecond=0)
                                        #
                                        #         logger.info("Blowing/arcing TRUE...top lance positioning was 0...captured now-{}".format(top_lance_positioning_end))
                                        #
                                        #     if slug_removal_start!=0 and slug_removal_end == 0:
                                        #         slug_removal_end=datetime.datetime.now().replace(microsecond=0)
                                        #         logger.info("captured slug removal end")
                                        #
                                        #     end_cycle=1
                                        #     logger.info("Its blowing/arcing TRUE...end the cycle")
                                        #     blowing_true=datetime.datetime.now().replace(microsecond=0)
                                        #     break

                                        # 4.1 HM Positioning process...
                                        # if scrap_charging == 0 and slug_removal == 0 and shell_levelling_end != 0 and hm_positioning_start == 0:
                                        if shell_levelling_end != 0 and hm_positioning_start == 0:
                                            hm_positioning_start = shell_levelling_end
                                            # print("Top pouring...hm_positioning_start - {}...shell_levelling_end - {}".format(hm_positioning_start, shell_levelling_end))
                                            print("Top pouring...shell_levelling_end - {}...hm_positioning_start - {}".format(shell_levelling_end,hm_positioning_start))
                                            logger.info("Top pouring...hm_positioning_start - {}...shell_levelling_end - {}".format(hm_positioning_start, shell_levelling_end))

                                        # elif scrap_charging == 1 and scrap_charging_end != 0 and hm_positioning_start == 0:
                                        #     hm_positioning_start = scrap_charging_end
                                        #     # hm_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                        #     print("Top pouring...hm_positioning_start-{}...scrap_charging_end-{}".format(
                                        #         hm_positioning_start, scrap_charging_end))
                                        #     logger.info("Top pouring...hm_positioning_start-{}...scrap_charging_end-{}".format(
                                        #         hm_positioning_start, scrap_charging_end))
                                        #
                                        # elif slug_removal == 1 and slug_removal_end != 0 and hm_positioning_start == 0:
                                        #     hm_positioning_start = slug_removal_end
                                        #     # hm_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                        #     print("Top pouring...hm_positioning_start-{}...slug removal end-{}".format(
                                        #         hm_positioning_start, slug_removal_end))
                                        #     logger.info("Top pouring...hm_positioning_start-{}...slug removal end-{}".format(
                                        #         hm_positioning_start, slug_removal_end))

                                        # IF STILL hm_positioning_start IS NOT STARTED & BUCKET IS DETECTED

                                        # if class_name == "bucket" and hm_positioning_start == 0:
                                        #     hm_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                        #     logger.info("hm_positioning_start-{}".format(hm_positioning_start))
                                        #     print("hm_positioning_start-{}".format(hm_positioning_start))

                                        # check which non cyclic process is the recent one and take its end time as start time of hm_positioning

                                        # 4.2 HM Pouring
                                        # hm positing end condition for top pouring BUCKET BOTTOM PLUS
                                        if class_name == "bucket plus" and hm_positioning_end == 0:
                                            bucket_plus_count += 1

                                            if bucket_plus_count >= 10:
                                                hm_positioning_end = datetime.datetime.now().replace(microsecond=0)
                                                hm_pouring_start = hm_positioning_end
                                                print("Top Pouring...hm_positioning_end-{}...hm_pouring_start-{}".format(hm_positioning_end,hm_pouring_start))
                                                logger.info("Top Pouring...hm_positioning_end-{}...hm_pouring_start-{}".format(hm_positioning_end,hm_pouring_start))

                                        # When Bucket is out of sight...HM Pouring is end and top lance positioning start
                                        # Top Lance Positioning process...
                                        if class_name == "top lance" and hm_pouring_end != 0:

                                            # IN CASE IF, HM_POURING NOT ENDED BUT TOP LANCE DETECTED ...START TOP LANCE POSITIONING
                                            if top_lance_positioning_start == 0:
                                                top_lance_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                                logger.info("top lance detected...top_lance_positioning_start-{}".format(top_lance_positioning_start))
                                                print("top lance detected...top_lance_positioning_start-{}".format(top_lance_positioning_start))

                                            # if hm_pouring_end==0:
                                            #     hm_pouring_end=datetime.datetime.now().replace(microsecond=0)
                                            #     logger.info("hm_pouring_end-{}".format(hm_pouring_end))
                                            #     print("hm_pouring_end-{}".format(hm_pouring_end))

                                            c1 = int(x + (w / 2.0))
                                            c2 = int(y + (h / 2.0))
                                            cv2.circle(img, (c1, c2), 5, (255, 153, 255), 5)

                                            top_lance_distance = math.sqrt(((p1 - c1) ** 2) + ((p2 - c2) ** 2))

                                            logger.info("TOP_POURING \n points(p1,p2,c1,c2)\n {},{},{},{}\n ...top lance distance-{}".format(p1,p2,c1,c2,top_lance_distance))
                                            print("TOP_POURING ...top lance distance-{}".format(top_lance_distance))

                                            # If model has detect top lance and checking the distance if condition is matching means we will get top lance positing end time...
                                            # if int(top_lance_distance) in range(0, 125) and top_lance_positioning_end == 0:
                                            if int(top_lance_distance) in range(0, 140) and top_lance_positioning_end == 0 and top_lance_positioning_start!=0:
                                                top_lance_positioning_end = datetime.datetime.now().replace(microsecond=0)

                                                # STILL IF HM_POURING END IS 0...
                                                if hm_pouring_end==0:
                                                    hm_pouring_end=top_lance_positioning_start

                                                print("Top lance end-{}".format(top_lance_positioning_end))
                                                end_cycle = 1
                                                print("Top Pouring...top_lance_positioning_end...also cycle end")
                                                logger.info("Top Pouring...top_lance_positioning_end-{}...also cycle end".format(top_lance_positioning_end))

                                    # Launder pouring process...
                                    elif launder_pouring == 1:

                                        # logger.info("inside launder pouring")
                                        # logger.info("check blowing/arcing")
                                        # check_end_cycle = is_cycle_end()
                                        #
                                        # if check_end_cycle == 1:
                                        #     if top_lance_positioning_end == 0:
                                        #         if len(top_lance_positioning_list)>0:
                                        #             top_lance_positioning_end = top_lance_positioning_list[-1]
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but top_lance_end is 0...captured now-{}".format(
                                        #                     top_lance_positioning_end))
                                        #         elif len(launder_car_insertion_list)>0:
                                        #             top_lance_positioning_end = launder_car_insertion_list[0]
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but top_lance_end is 0...captured now-{}".format(
                                        #                     top_lance_positioning_end))
                                        #
                                        #
                                        #     if launder_insertion_start == 0 and top_lance_positioning_end !=0:
                                        #         launder_insertion_start = top_lance_positioning_end
                                        #         logger.info(
                                        #             "Blowing/Arcing TRUE but launder_insertion_start is 0...captured now-{}".format(
                                        #                 launder_insertion_start))
                                        #
                                        #     if launder_insertion_end == 0:
                                        #         if len(launder_car_insertion_list)>0:
                                        #             launder_insertion_end = launder_car_insertion_list[-1]
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but launder_insertion_end is 0...captured now-{}".format(
                                        #                     launder_insertion_end))
                                        #
                                        #         elif len(hm_positioning_list)>0:
                                        #             launder_insertion_end = hm_positioning_list[0]
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but launder_insertion_end is 0...captured now-{}".format(
                                        #                     launder_insertion_end))
                                        #
                                        #     if hm_positioning_start == 0 and launder_insertion_end != 0:
                                        #         hm_positioning_start = launder_insertion_end
                                        #         logger.info("Blowing/Arcing TRUE but hm_positioning_start is 0...captured now-{}".format(hm_positioning_start))
                                        #
                                        #     if hm_positioning_end ==0:
                                        #         if len(hm_positioning_list)>0:
                                        #             hm_positioning_end = hm_positioning_list[-1]
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but hm_positioning_end is 0...captured now-{}".format(
                                        #                     hm_positioning_end))
                                        #
                                        #     if hm_pouring_start == 0 and hm_positioning_end != 0:
                                        #         hm_pouring_start = hm_positioning_end
                                        #         logger.info(
                                        #             "Blowing/Arcing TRUE but hm_pouring_start is 0...captured now-{}".format(
                                        #                 hm_pouring_start))
                                        #
                                        #
                                        #     if hm_pouring_end == 0:
                                        #         if len(bucket_plus_list)>0:
                                        #             hm_pouring_end = bucket_plus_list[-1]
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but hm_pouring_end is 0...captured now-{}".format(
                                        #                     hm_pouring_end))
                                        #
                                        #         else:
                                        #             hm_pouring_end=datetime.datetime.now().replace(microsecond=0)
                                        #             logger.info(
                                        #                 "Blowing/Arcing TRUE but hm_pouring_end is 0...captured now-{}".format(
                                        #                     hm_pouring_end))
                                        #
                                        #
                                        #     end_cycle = 1
                                        #     logger.info("Its blowing/arcing TRUE...end the cycle")
                                        #     blowing_true = datetime.datetime.now().replace(microsecond=0)
                                        #     break

                                        # 4.1 Top Lance Positioning
                                        # if scrap_charging == 0 and slug_removal == 0 and shell_levelling_end != 0 and top_lance_positioning_start == 0:
                                        if shell_levelling_end != 0 and top_lance_positioning_start == 0:
                                            top_lance_positioning_start = shell_levelling_end
                                            print("Launder pouring...top_lance_positioning_start-{}...shell_levelling_end-{}".format(top_lance_positioning_start, shell_levelling_end))
                                            logger.info("Launder pouring...top_lance_positioning_start-{}...shell_levelling_end-{}".format(top_lance_positioning_start, shell_levelling_end))

                                        # elif scrap_charging == 1 and scrap_charging_end != 0 and top_lance_positioning_start == 0:
                                        #     top_lance_positioning_start = scrap_charging_end
                                        #     # top_lance_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                        #     print("Launder pouring...top_lance_positioning_start-{}...scrap_charging_end-{}".format(top_lance_positioning_start, scrap_charging_end))
                                        #     logger.info("Launder pouring...top_lance_positioning_start-{}...scrap_charging_end-{}".format(top_lance_positioning_start, scrap_charging_end))
                                        #
                                        # elif slug_removal == 1 and slug_removal_end != 0 and top_lance_positioning_start == 0:
                                        #     top_lance_positioning_start = slug_removal_end
                                        #     # top_lance_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                        #     print("Launder pouring...top_lance_positioning_start-{}...slug_removal_end-{}".format(top_lance_positioning_start, slug_removal_end))
                                        #     logger.info("Launder pouring...top_lance_positioning_start-{}...slug_removal_end-{}".format(top_lance_positioning_start, slug_removal_end))

                                        # check which non cyclic process is the recent one and take its end time as start time of top_lance_positioning

                                        if class_name == 'top lance':

                                            top_lance_positioning_list.append(datetime.datetime.now().replace(microsecond=0))
                                            logger.info("top_lance_positioning_list-{}".format(top_lance_positioning_list))
                                            print("top_lance_positioning_list-{}".format(top_lance_positioning_list))


                                            # if top_lance_positioning_start == 0:
                                            #     top_lance_positioning_start = datetime.datetime.now().replace(microsecond=0)
                                            #     logger.info("top_lance_positioning_start-{}".format(top_lance_positioning_start))
                                            #     print("top_lance_positioning_start-{}".format(top_lance_positioning_start))

                                            c1 = int(x + (w / 2.0))
                                            c2 = int(y + (h / 2.0))
                                            # c1=int(x+w)
                                            # c2=int(y+(h/2))
                                            cv2.circle(img, (c1, c2), 5, (255, 153, 255), 5)
                                            top_lance_distance = math.sqrt(((p1 - c1) ** 2) + ((p2 - c2) ** 2))

                                            print("LAUNDER_POURING ...top lance distance-{}".format(top_lance_distance))
                                            logger.info("LAUNDER_POURING \n points(p1,p2,c1,c2)\n {},{},{},{}\n ...top lance distance-{}".format(p1,p2,c1,c2,top_lance_distance))

                                            # If model has detect top lance and checking the distance if condition is matching means we will get top lance positing end time...

                                            if int(top_lance_distance) in range(0, 140) and top_lance_positioning_end == 0:

                                                top_lance_positioning_end = datetime.datetime.now().replace(microsecond=0)
                                                launder_insertion_start = top_lance_positioning_end
                                                print("top lance positioning end & launder insertion start-{}".format(top_lance_positioning_end,launder_insertion_start))

                                                # Top lance positing end means we will get launder insert start time...
                                                # if launder_insertion_start == 0:
                                                #     launder_insertion_start = top_lance_positioning_end

                                                pro_time.append(str(top_lance_positioning_end))
                                                pro_time.append(str(launder_insertion_start))
                                                # # print(pro_time)
                                                # print("Top_lance_position_end-{} & launder_insertion_start-{}".format(top_lance_positioning_end,launder_insertion_start))
                                                logger.info("Top_lance_position_end-{} & launder_insertion_start-{}".format(
                                                    top_lance_positioning_end, launder_insertion_start))

                                        # # 4.2 Launder Insertion
                                        if class_name == "launder car": # and launder_insertion_start == 0:
                                            launder_car_insertion_list.append(datetime.datetime.now().replace(microsecond=0))
                                            logger.info("launder_car_insertion_list-{}".format(launder_car_insertion_list))
                                            print("launder_car_insertion_list-{}".format(launder_car_insertion_list))

                                        if class_name == "launder car": # and launder_insertion_start != 0:
                                            c1 = int(x + (w / 2.0))
                                            c2 = int(y + (h / 2.0))
                                            cv2.circle(img, (c1, c2), 5, (170, 170, 170), 5)
                                            # launder_car_distance = math.sqrt(((q1 - c1) ** 2) + ((q2 - c2) ** 2))
                                            launder_car_distance = math.sqrt(((q1 - c1) ** 2) + ((q2 - c2) ** 2))
                                            print("launder_car_distance-{}".format(launder_car_distance))
                                            logger.info("LAUNDER_POURING\n points(q1,q2,c1,c2)\n{},{},{},{}\nlaunder_car_distance-{}".format(q1,q2,c1,c2,launder_car_distance))

                                            # This the condition where we will get launder insert end time
                                            if int(launder_car_distance) in range(0, 280) and launder_insertion_end == 0:
                                                launder_insertion_end = datetime.datetime.now().replace(microsecond=0)

                                                # Launder insert end menas we will get hm positing start time...
                                                # if hm_positioning_start == 0:
                                                hm_positioning_start = launder_insertion_end
                                                logger.info("hm_positioning_start-{}".format(hm_positioning_start))
                                                print("hm_positioning_start-{}".format(hm_positioning_start))

                                                pro_time.append(str(launder_insertion_end))
                                                pro_time.append(str(hm_positioning_start))
                                                print("launder_insertion_end-{} and hm_positioning_start-{}".format(launder_insertion_end,hm_positioning_start))
                                                logger.info("launder_insertion_end-{} and hm_positioning_start-{}".format(launder_insertion_end,hm_positioning_start))

                                        if class_name == "bucket": # and hm_positioning_start == 0:
                                            hm_positioning_list.append(datetime.datetime.now().replace(microsecond=0))
                                            logger.info("hm_positioning_list-{}".format(hm_positioning_list))
                                            print("hm_positioning_list-{}".format(hm_positioning_list))

                                        # 4.3 HM Positioning
                                        if len(idxs) >= 2: # and hm_positioning_start != 0:
                                            temp = []

                                            for j in idxs.flatten():
                                                temp.append(classes1[classIDs[j]])

                                            # If model has detect both hook and bucket...
                                            if "hook" in temp and "bucket" in temp and hm_positioning_end == 0:
                                                hm_positioning_end = datetime.datetime.now().replace(microsecond=0)
                                                hm_pouring_start = hm_positioning_end

                                                print("hm_positioning_end-{} & hm_pouring_start-{}".format(hm_positioning_end,hm_pouring_start))
                                                logger.info("hm_positioning_end-{} & hm_pouring_start-{}".format(hm_positioning_end,hm_pouring_start))

                                                # HERE WE WILL CHECK ALL PREVIOSU PROCESS IF ANY "0"
                                                if top_lance_positioning_end == 0:
                                                    if len(top_lance_positioning_list)>0:
                                                        top_lance_positioning_end = top_lance_positioning_list[-1]
                                                        launder_insertion_start = top_lance_positioning_end
                                                        logger.info("FROM TOP LANCE POSITIONING LIST top lance positioning end & launder insertion start - {} & {}".format(top_lance_positioning_end,launder_insertion_start))
                                                    elif len(launder_car_insertion_list)>0:
                                                        top_lance_positioning_end=launder_car_insertion_list[0]
                                                        launder_insertion_start=top_lance_positioning_end
                                                        logger.info("FROM LAUNDER LIST top lance positioning end & launder insertion start - {} & {}".format(top_lance_positioning_end,launder_insertion_start))


                                                if launder_insertion_end == 0:
                                                    if len(launder_car_insertion_list)>0:
                                                        launder_insertion_end = launder_car_insertion_list[-1]
                                                        hm_positioning_start = launder_insertion_end
                                                        logger.info("FROM LAUNDER INSERTION LIST launder insertion end & hm positioning start - {} & {}".format(launder_insertion_end,hm_positioning_start))
                                                    elif len(hm_positioning_list)>0:
                                                        launder_insertion_end=hm_positioning_list[0]
                                                        hm_positioning_start=launder_insertion_end
                                                        logger.info("FROM HM POSITIONING LIST launder insertion end & hm positioning start - {} & {}".format(launder_insertion_end, hm_positioning_start))


                                                # if launder_insertion_start != 0 and launder_insertion_end == 0:
                                                #     launder_insertion_end = hm_positioning_start
                                                #     print("launder_insertion_end-{}".format(launder_insertion_end))
                                                #     logger.info("launder_insertion_end-{}".format(launder_insertion_end))

                                                # # YOLO code for checking both these detected objects
                                                # hook = []
                                                # bucket = []
                                                # # # print("5...{}".format(type(idxs)))
                                                # for j in idxs.flatten():
                                                #     # print("5-{}".format(type(idxs)))
                                                #     (x, y) = (boxes[j][0], boxes[j][1])
                                                #     (w, h) = (boxes[j][2], boxes[j][3])
                                                #     cv2.rectangle(img, (x, y), (x + w, y + h), 0, 2)
                                                #     class_name = classes1[classIDs[j]]m

                                                #     if class_name == "bucket":
                                                #         # # print("bucket-{}".format([x,y,w,h]))
                                                #         bucket.append(x)
                                                #         bucket.append(y)
                                                #         bucket.append(w)
                                                #         bucket.append(h)
                                                #     if class_name == "Hook":
                                                #         # # print("Hook-{}".format([x,y,w,h]))
                                                #         hook.append(x)
                                                #         hook.append(y)
                                                #         hook.append(w)
                                                #         hook.append(h)
                                                # # Check Intersection between hook and bucket bounding box
                                                # if hook[1] + hook[3] in range(bucket[1], bucket[1] + bucket[3]) and hook[1] < bucket[1] and hm_positioning_end == 0:
                                                #     # print("Condition Satisfied-{}-{}".format(bucket,hook))
                                                #     # If hook and bucket condition is matching means hm positoing end and we will get hm puring start time...
                                                #     hm_positioning_end = datetime.datetime.now().replace(microsecond=0)
                                                #     # Hm positing end menas we willget hm pouring start time...
                                                #     hm_pouring_start = hm_positioning_end
                                                #     pro_time.append(str(hm_positioning_end))
                                                #     pro_time.append(str(hm_pouring_start))
                                                #     print("hm_positioning_end-{} & hm_pouring_start-{}".format(hm_positioning_end,hm_pouring_start))
                                                #     logger.info("hm_positioning_end-{} & hm_pouring_start-{}".format(hm_positioning_end,hm_pouring_start))

                            # VIDEO SAVE
                            vout_front.write(img)

                            # DISPLAY IMAGE
                            # cv2.imshow("Shell 4 FRONT", img)
                            # cv2.waitKey(1)

                    if end_front == 1:
                        connected_front = 0

                        while connected_front != 1:
                            try:
                                logger.info("Trying to Reconnect front camera...")
                                cam = Client('http://{}'.format(ip_front), 'admin', 'vert@123')
                                logger.info("Connected !")
                                connected_front = 1

                            except Exception as e1:
                                logger.info("Its Exception while Reconnecting - {}".format(e1))
                                logger.info("Retrying...")
                                continue

                        # CONTINUE WHILE LOOP (end_cycle LOOP)
                        continue

            except Exception as front_e:
                # logger.info("Shell 4 Front view Exception - {}".format(front_e))
                # print("Shell 4 Front view Exception - {}".format(front_e))
                logger.info("main code exception-{}".format(front_e))
                print("main code exception-{}".format(front_e))

        logger.info("Shell 4 end_cycle-{} ...out from while end_cycle loop".format(end_cycle))

        # RESET EVERYTHING FROM START TO END ONCE CYCLE IS COMPLETE...
        # ALSO UPDATE TIME STAMPS IN TXT FILE for reference...

        if end_cycle == 1:

            # LOGIC FOR CHECKING IF ANY START/END  IS "0"
            if launder_pouring == 1:

                # ASSIGN THE ACTUAL SHELL LEVELLING END TIME NOW TO THE TOP_LANCE_POSITIONING_START
                if shell_levelling_end!=0:
                    top_lance_positioning_start=shell_levelling_end

                if top_lance_positioning_end == 0 and launder_insertion_start != 0:
                    top_lance_positioning_end = launder_insertion_start

                if launder_insertion_end == 0 and hm_positioning_start != 0:
                    launder_insertion_end = hm_positioning_start

                zero_timings = {}

                # CHECK IF STILL ANY OF THE PROCESS START/END TIME IS "0"
                if top_lance_positioning_start == 0:
                    zero_timings["top_lance_positioning_start"]=top_lance_positioning_start
                if top_lance_positioning_end == 0:
                    zero_timings["top_lance_positioning_start"] = top_lance_positioning_end
                if launder_insertion_start == 0:
                    zero_timings["launder_insertion_start"] = launder_insertion_start
                if launder_insertion_end == 0:
                    zero_timings["launder_insertion_end"] = launder_insertion_end
                if hm_positioning_start == 0:
                    zero_timings["hm_positioning_start"] = hm_positioning_start
                if hm_positioning_end == 0:
                    zero_timings["hm_positioning_end"] = hm_positioning_end
                if hm_pouring_start == 0:
                    zero_timings["hm_pouring_start"] = hm_pouring_start
                if hm_pouring_end == 0:
                    zero_timings["hm_pouring_end"] = hm_pouring_end

            if top_pouring == 1:

                # ASSIGN THE ACTUAL SHELL LEVELLING END TIME NOW TO THE HM_POSITIONING_START
                if shell_levelling_end != 0:
                    hm_positioning_start = shell_levelling_end

                if hm_pouring_end == 0 and top_lance_positioning_start != 0:
                    hm_pouring_end = top_lance_positioning_start

                zero_timings = {}

                # CHECK IF STILL ANY OF THE PROCESS START/END TIME IS "0"
                if top_lance_positioning_start == 0:
                    zero_timings["top_lance_positioning_start"] = top_lance_positioning_start
                if top_lance_positioning_end == 0:
                    zero_timings["top_lance_positioning_start"] = top_lance_positioning_end
                if hm_positioning_start == 0:
                    zero_timings["hm_positioning_start"] = hm_positioning_start
                if hm_positioning_end == 0:
                    zero_timings["hm_positioning_end"] = hm_positioning_end
                if hm_pouring_start == 0:
                    zero_timings["hm_pouring_start"] = hm_pouring_start
                if hm_pouring_end == 0:
                    zero_timings["hm_pouring_end"] = hm_pouring_end

            print("****** SHELL 4 END CYCLE...WILL INSERT DATA INTO SQL *******")

            # Store Timestamps in txt file
            f_name = datetime.datetime.now().replace(microsecond=0)
            result_file = "Result_{}".format(f_name)
            touch.touch("/home/root1/CVML_2/Result_Txt_shell4/{}.txt".format(result_file))

            with open("/home/root1/CVML_2/Result_Txt_shell4/{}.txt".format(result_file),"w") as f:

                if top_pouring == 1:
                    logger.info("Writing top pouring Details to txt file")

                    f.write("EBJ removal - Start-{} & End-{}".format(ebj_removal_start, ebj_removal_end))
                    f.write("\n")
                    f.write("EBT Mass Filling - Start-{} & End-{}".format(ebt_mass_filling_start, ebt_mass_filling_end))
                    f.write("\n")
                    f.write("shell_levelling - Start-{} & End-{}".format(shell_levelling_start, shell_levelling_end))
                    f.write("\n")
                    f.write("IT's Shell 4 TOP POURING \n")
                    f.write("Hm_positioning - Start-{} & End-{}".format(hm_positioning_start,hm_positioning_end))
                    f.write("\n")
                    f.write("Hm_pouring - Start-{} & End-{}".format(hm_pouring_start,hm_pouring_end))
                    f.write("\n")
                    f.write("Top_lance_positioning - Start-{} & End-{}".format(top_lance_positioning_start,top_lance_positioning_end))
                    f.write("\n")
                    f.write("#"*50)
                    f.write("\n")
                    f.write("Non-Cyclic Process")
                    f.write("\n")
                    f.write("SlugDoor_Cleaning - Start-{} & End-{}".format(slug_removal_start, slug_removal_end))
                    f.write("\n")
                    f.write("Scrap_charging - Start-{} & End-{}".format(scrap_charging_start, scrap_charging_end))
                    f.write("\n")
                    f.write("Fettling - Start-{} & End-{}".format(fettling_start, fettling_end))
                    f.write("\n")
                    f.write("Gunning - Start-{} & End-{}".format(gunning_start, gunning_end))
                    f.write("\n")
                    f.write("Blowing/Arcing TRUE - {}".format(blowing_true))
                    f.write("\n")

                    logger.info("writing Done")

                elif launder_pouring == 1:

                    logger.info("Writing launder pouring Details to txt file")

                    f.write("EBJ removal - Start-{} & End-{}".format(ebj_removal_start, ebj_removal_end))
                    f.write("\n")
                    f.write("EBT Mass Filling - Start-{} & End-{}".format(ebt_mass_filling_start, ebt_mass_filling_end))
                    f.write("\n")
                    f.write("shell_levelling - Start-{} & End-{}".format(shell_levelling_start, shell_levelling_end))
                    f.write("\n")
                    f.write("IT's shell 4 LAUNDER POURING \n")
                    f.write("Top_lance_positioning - Start-{} & End-{}".format(top_lance_positioning_start,top_lance_positioning_end))
                    f.write("\n")
                    f.write("Launder_insertion - Start-{} & End-{}".format(launder_insertion_start,launder_insertion_end))
                    f.write("\n")
                    f.write("Hm_positioning - Start-{} & End-{}".format(hm_positioning_start, hm_positioning_end))
                    f.write("\n")
                    f.write("Hm_pouring - Start-{} & End-{}".format(hm_pouring_start, hm_pouring_end))
                    f.write("\n")
                    f.write("#" * 50)
                    f.write("\n")
                    f.write("Non-Cyclic Process")
                    f.write("\n")
                    f.write("SlugDoor_Cleaning - Start-{} & End-{}".format(slug_removal_start, slug_removal_end))
                    f.write("\n")
                    f.write("Scrap_charging - Start-{} & End-{}".format(scrap_charging_start, scrap_charging_end))
                    f.write("\n")
                    f.write("Fettling - Start-{} & End-{}".format(fettling_start, fettling_end))
                    f.write("\n")
                    f.write("Gunning - Start-{} & End-{}".format(gunning_start, gunning_end))
                    f.write("\n")
                    f.write("Blowing/Arcing TRUE - {}".format(blowing_true))
                    f.write("\n")

                    logger.info("writing Done")


            # CALLING SQL INSERT FUNCTION

            # PROCESS NAMES TO BE PASSED AS KEY IN DICTIONARY ALONG WITH ITS TIME VALUES
            # names=["EBTBRICKJAM", "EBTMASSFilling", "EBTLevelling", "HMPositioning", "HMPouring", "LaunderInsertion", "TopLancePositioning"]
            names = [ "EBTBRICKJAM","EBTMASSFilling","EBTLevelling","ScrapCharging","SlagDoorCleaning","TopLancePositioning", "LaunderInsertion", "HMPositioning","HMPouring","Fettling","Gunning"]

            if launder_pouring == 1:
                print("It was shell 4 Launder pouring")

                process_dict = {names[0]: (ebj_removal_start, ebj_removal_end, 4),
                                names[1]: (ebt_mass_filling_start, ebt_mass_filling_end, 4),
                                names[2]: (shell_levelling_start, shell_levelling_end, 4),
                                names[5]: (top_lance_positioning_start, top_lance_positioning_end, 4),
                                names[6]: (launder_insertion_start, launder_insertion_end, 4),
                                names[7]: (hm_positioning_start, hm_positioning_end, 4),
                                names[8]: (hm_pouring_start, hm_pouring_end, 4)}

                if scrap_charging == 1:
                    process_dict[names[3]] = (scrap_charging_start, scrap_charging_end,4)

                if slug_removal == 1:
                    process_dict[names[4]] = (slug_removal_start,slug_removal_end,4)

                if fettling==1:
                    process_dict[names[9]] = (fettling_start, fettling_end, 4)

                if gunning==1:
                    process_dict[names[10]] = (gunning_start, gunning_end, 4)


            elif top_pouring == 1:
                print("It was shell 4 Top pouring")

                process_dict = {names[0]: (ebj_removal_start, ebj_removal_end, 4),
                                names[1]: (ebt_mass_filling_start, ebt_mass_filling_end, 4),
                                names[2]: (shell_levelling_start, shell_levelling_end, 4),
                                names[7]: (hm_positioning_start, hm_positioning_end, 4),
                                names[8]: (hm_pouring_start, hm_pouring_end, 4),
                                names[5]: (top_lance_positioning_start, top_lance_positioning_end, 4)}

                if scrap_charging == 1:
                    process_dict[names[3]] = (scrap_charging_start, scrap_charging_end,4)

                if slug_removal == 1:
                    process_dict[names[4]] = (slug_removal_start,slug_removal_end,4)

                if fettling == 1:
                    process_dict[names[9]] = (fettling_start, fettling_end, 4)

                if gunning == 1:
                    process_dict[names[10]] = (gunning_start, gunning_end, 4)

            # Calling SQL function to insert Data to SQl
            print("Calling SQL Data Insert Function")
            insert_data(process_dict,result_file,4)

            # RESETTIG ALL VARIABLES

            # print("Resetting all variables")
            # # P1
            # start_process_monitoring = 0
            # ebj_removal_start = 0
            # ebj_removal_end = 0
            #
            # # P2
            # ebt_mass_filling_start = 0
            # ebt_mass_filling_end = 0
            #
            # # P3
            # shell_levelling_start = 0
            # shell_levelling_end = 0
            #
            # # P4
            # top_lance_positioning_list = []
            # bucket_plus_count = 0
            # top_count = 0
            # start_pouring = 0
            # top_pouring = 0
            # hm_positioning_start = 0
            # hm_positioning_end = 0
            # hm_pouring_start = 0
            # hm_pouring_end = 0
            # top_lance_positioning_start = 0
            # top_lance_positioning_end = 0
            #
            # launder_car_insertion_list = []
            # launder_count = 0
            # launder_pouring = 0
            # top_lance_positioning_start = 0
            # top_lance_positioning_end = 0
            # launder_insertion_start = 0
            # launder_insertion_end = 0
            # hm_positioning_start = 0
            # hm_positioning_end = 0
            # hm_pouring_start = 0
            # hm_pouring_end = 0
            # end_hm_pouring = 0
            #
            # # NON CYCLIC
            # person_count = 0
            # person_time = []
            # slug_removal = 0
            # slug_count = 0
            # slug_removal_start = 0
            # slug_removal_end = 0
            # no_slug_car = 0
            # scrap_charging = 0
            # scrap_count = 0
            # no_scrap_bucket = 0
            # scrap_charging_start = 0
            # scrap_charging_end = 0
            # gunning = 0
            # gunning_start = 0
            # gunning_end = 0
            # fettling = 0
            # fettling_start = 0
            # fettling_end = 0
            #
            # # COMMON VARIABLES

            # check_end_cycle = 0
            # t1 = time.time()
            # t2 = time.time()
            # cycle = 0
            # timestamps = []
            # cycles = {}
            # tim = time.time()
            # end_cycle = 0
            # ebt_camera = 0
            # front_camera = 0
            # top_lance_distance = 0
            # launder_car_distance = 0
            # recent_proc_time = time.time()
            # cur_tim = time.time()
            # none_frame = 0
            # pro_time = []
            # per_count = 0
            # per_cent = []
            # none_frame_ebt = 0
            # none_frame_front = 0
            # sec = 0.0
            # framerate = 1.0
            # end_ebt = 0
            # end_front = 0
            #
            # # VIDEOWRITER VARIABLE
            # vout_ebt = None
            # fps_ebt = 5
            # vout_front = None
            # fps_front = 5

            # logger.info("Cycle End...Reset all variables")
            # print("Cycle End...Reset all variables")

            # HOLD FOR 30 sec
            logger.info("Hold for 30 sec to settle")
            print("Hold for 30 sec to settle")
            time.sleep(30)
            logger.info("Done")
            print("One Cycle Done")

            # break

    except Exception as e:

        print("Shell 4 Model Exception - {}".format(e))
        logger.info("Shell 4 Model Exception-{}".format(e))
        # exception_type, exception_object, exception_traceback = sys.exc_info()
        # filename = exception_traceback.tb_frame.f_code.co_filename
        # line_number = exception_traceback.tb_lineno
        # print("Shell 4 Model Exception type: ", exception_type)
        # print("File name: ", filename)
        # print("Line number: ", line_number)

if __name__ == "__main__":

    while True:
        logger.info("Calling shell_4 inside main")
        shell_4()
        logger.info("shell_4 terminated...will restart again")