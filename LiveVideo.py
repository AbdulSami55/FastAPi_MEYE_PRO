from datetime import datetime
from datetime import datetime
import os

import cv2
import Model.CheckTime as mchecktime
import ApiFunctions.CheckTime as apichecktime
from LiveVideoDetails import LiveVideoDetails
import Model.TeacherSlots as mteacherslots
import ApiFunctions.TeacherSlots as apiteacherslots
import Model.CheckTimeDetails as mchecktimedetails
import ApiFunctions.CheckTimeDetails as apichecktimedetails
import Model.ActivityDetails as mactivitydetails
import ApiFunctions.ActivityDetails as apiactivitydetails

class LiveStreaming():
    def update(self,st,et,model,teacherName,slotId,ip):
        # cap = cv2.VideoCapture(ip)
        # fullVideoCodec = cv2.VideoWriter_fourcc(*'mp4v')
        # Fullvideo = cv2.VideoWriter(f'Recordings/FullLectureVideos/{slotId},full_recording.mp4', fullVideoCodec, 30, (1920, 1080))
        # while True:
        #     if datetime.now().time()>st.time() and datetime.now().time()<et.time():
        #         _,frame = cap.read()
        #         Fullvideo.write(frame)
        #     else:
        #         Fullvideo.release()
        object = LiveVideoDetails(f'D:/New folder/videos/sirnoman 1.mp4',model,teacherName,st,et,slotId)
        response =object.update()
        print(response)
        directory = f"{slotId},Sit"  
        directorystand = f"{slotId},Stand"  
        parent_dir = "Recordings/RecordingDetails/"
        path = os.path.join(parent_dir, directory)
        path_stand = os.path.join(parent_dir, directorystand)
        os.mkdir(path)
        os.mkdir(path_stand)

        self.extract_frames('D:/New folder/videos/sirnoman 1.mp4', response['tempactivitySitDetails'],f'{parent_dir}{directory}/',response['activitySitDetails'])
        self.extract_frames('D:/New folder/videos/sirnoman 1.mp4', response['tempactivityStandDetails'],f'{parent_dir}{directorystand}/',response['activityStandDetails'])
                #break
                # checktime_object =  apichecktime.CheckTimeApi(checktime=mchecktime)
                # ctime = mchecktime.CheckTime(id=0,teacherSlotID=slotId,totaltimein=response['totalTimeIn'],totaltimeout=response['totalTimeOut'],
                #                             date=str(datetime.now().date()),sit=response['sitTime'],stand=response['standTime'])
                # checktime_object.add_checktime(checktime=ctime)

                # checktime =checktime_object.checksingletime_details(teacherSlotID=slotId)
                # checktimedata = checktime
                # teacherslot_object = apiteacherslots.TeacherSlots(teacherslots=mteacherslots)
                
                # teacherSlot = mteacherslots.TeacherSlot
                # teacherSlot.id=slotId
                # teacherSlot.timetableId=0
                # teacherSlot.status=response['status']
                # teacherSlot.slot = 0
            
                # teacherslot_object.update_teacherslots_details(teacherslots=teacherSlot)

                # for (timein,timeout) in zip(response['timeInDetails'],response['timeOutDetails']):                
                #     checktimedetails_object =  apichecktimedetails.CheckTimeDetailsApi(checktimedetails=mchecktimedetails)
                #     ctimedetails = mchecktimedetails.CheckTimeDetails(id=0,checkTimeID=checktimedata.id,timein=timein,timeout=timeout)
                #     datetime.now()
                #     checktimedetails_object.add_checktimedetails(checktimedetails=ctimedetails) 
                    
                
                # for data in response['activitySitDetails']:
                #     activity_object =  apiactivitydetails.ActivityDetailsApi()
                #     activity = mactivitydetails.ActivityDetails(id=0,checkTimeID=checktimedata.id,timein=data[0],timeout=data[1],status=data[2])
                #     datetime.now()
                #     activity_object.add_activity_details(activitydetails=activity) 

                # for data in response['activityStandDetails']:
                #     activity_object =  apiactivitydetails.ActivityDetailsApi()
                #     activity = mactivitydetails.ActivityDetails(id=0,checkTimeID=checktimedata.id,timein=data[0],timeout=data[1],status=data[2])
                #     datetime.now()
                #     activity_object.add_activity_details(activitydetails=activity)
                # break
    def extract_frames(self,video_path, time_intervals, output_path,current_time_interval):
        print('...enter...')
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
        print(video_path)

        for interval,current_interval in zip(time_intervals,current_time_interval):
            start_time, end_time = interval
            print(start_time,end_time)
            # Convert time to frame index
            start_frame = int(start_time * fps)
            end_frame = int(end_time * fps)

            video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            temp_start_time = str(current_interval[0]).split(" ")[1].split(".")[0]
            temp_end_time = str(current_interval[1]).split(" ")[1].split(".")[0]
            print(f'output_path={output_path}{temp_start_time.split(":")[0]} {temp_start_time.split(":")[1]} {temp_start_time.split(":")[2]},{temp_end_time.split(":")[0]} {temp_end_time.split(":")[1]} {temp_end_time.split(":")[2]}.mp4')
            video_writer = cv2.VideoWriter(f'{output_path}{temp_start_time.split(":")[0]} {temp_start_time.split(":")[1]} {temp_start_time.split(":")[2]},{temp_end_time.split(":")[0]} {temp_end_time.split(":")[1]} {temp_end_time.split(":")[2]}.mp4', fourcc, fps, (frame_width, frame_height))
            while start_frame <= end_frame:
                ret, frame = video.read()
                if not ret:
                    break

                # Process the frame (e.g., perform operations, write to video)
                video_writer.write(frame)

                start_frame += 1
            video_writer.release()

        video.release()
        

              
  