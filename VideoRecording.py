import os
import threading
from datetime import datetime
from threading import Thread
import cv2
from datetime import datetime, timedelta
import Model.Recordings as mrecordings
import ApiFunctions.Recordings as apirecordings
import Model.User as muser
import ApiFunctions.User as apiuser
import Model.CheckTime as mchecktime
import ApiFunctions.CheckTime as apichecktime
import Model.CheckTimeDetails as mchecktimedetails
import ApiFunctions.CheckTimeDetails as apichecktimedetails
import face_recognition
import numpy as np
import Model.TeacherSlots as mteacherslots
import ApiFunctions.TeacherSlots as apiteacherslots
from collections import Counter


class RTSPVideoWriterObject(object):
    def __init__(self,ip, s, e, f,stime,etime,day,teacherName,timetableId,slotId,model):
        self.model = model
        self.capture = cv2.VideoCapture(ip)
        self.s = s
        self.e = e
        self.f= f
        self.st = stime
        self.et = etime
        self.day = day
        self.teacherName = teacherName
        self.timetableId = timetableId
        self.slotId = slotId
        self._key_lock = threading.Lock() 
        self.codec = cv2.VideoWriter_fourcc(*'h264')
        self.frame_width = 300
        self.frame_height = 150
        self.teachertimeinframes=0
        self.teachertimeoutframes=0
        self.totalteachertimeframes=0
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.sc=0
        self.image_encodings=None
        self.teacherin = False
        self.tempFrameCount=0
        self.tempFrame=None
        self.readImageCount=0
        self.status=False
        self.ip=ip
        self.activityLabel=[]
        
    def update(self):
        lsttimein=[]
        lsttimeout=[]
        lstActivityLabel=[]
        lstActivityTime=[]
        user_object =  apiuser.UserApi(user=muser)
        user=  user_object.single_user_details(teacherName=self.teacherName,role='Teacher')
        userdata = user['data']
        image =  face_recognition.load_image_file(f'UserImages/Teacher/{userdata.image}')
        self.image_encodings = face_recognition.face_encodings(image)[0]
        while True:
            #self.capture = cv2.VideoCapture(self.ip)
            if self.capture.isOpened():
                if datetime.now().time()>self.st.time() and datetime.now().time()<self.et.time():
                    (self.status, self.frame) = self.capture.read()  
                if self.status and self.sc==0 and datetime.now().time()>self.st.time() and datetime.now().time()<self.et.time():
                    self.thread1 = threading.Thread(target=self.check_time, args=())
                    self.thread1.daemon = True
                    self.thread1.start()
                    self.sc+=1
                if self.status and datetime.now().time()>self.st.time() and datetime.now().time()<self.et.time():
                    if self.tempFrameCount>10:
                        if self._key_lock.locked():
                            pass
                        else:
                            self.tempFrameCount=0
                            self.thread2 = threading.Thread(target=self.check_time_using_facial_recognition, args=())
                            self.thread2.daemon = True
                            self.thread2.start()
                        #self.check_time_using_facial_recognition(tempFrame=tempFrame)
                    else:
                        self.tempFrameCount+=1
                    if self.totalteachertimeframes>2:
                        if self.teachertimeinframes>0:
                            if self.teacherin==False:
                                self.teacherin=True
                                lsttimein.append(datetime.now())
                            counted = Counter(self.activityLabel)
                            most_common = counted.most_common(1)
                            if lstActivityLabel==[]:
                                lstActivityLabel.append(most_common[0][0])
                                lstActivityTime.append(datetime.now())
                            elif most_common[0][0]!=lstActivityLabel[-1]:
                                lstActivityLabel.append(most_common[0][0])
                                lstActivityTime.append(datetime.now())
                            
                            
                        elif self.teachertimeinframes==0 and self.teacherin==True:
                            lsttimeout.append(datetime.now())
                            self.teacherin= False
                        self.totalteachertimeframes=0
                        self.teachertimeinframes=0
                        self.teachertimeoutframes=0
                        print(len(self.activityLabel))
                        print(self.activityLabel)
                        self.activityLabel=[]
                    
                    
                        
                        
                    
                if self.sc==1 and datetime.now().time()>self.et.time():
                
                    if self.teacherin==True :
                        lsttimeout.append(datetime.now())
                        self.teacherin= False
                    self.activityLabel=[]
                    self.totalteachertimeframes=0
                    self.teachertimeinframes=0
                    self.teachertimeoutframes=0
                    totaltimein =0
                    totaltimeout =0
                    overalltimemin=0
                    totalsec=0
                    if lsttimein!=[]:  
                        if len(lsttimein)!=len(lsttimeout):
                            lsttimeout.append(datetime.now())
                    else:
                        lsttimeout=[]
                        lsttimein=[]
                    overalltime = datetime.now() - self.st
                    sec = overalltime.total_seconds()
                    overalltimemin += int(sec / 60)
                    
                    for (timein,timeout) in zip(lsttimein,lsttimeout):
                        time = timeout-timein
                        sec = time.total_seconds()
                        totalsec += sec
                    totalsec+=20
                    if (float(totalsec/60)-int(totalsec/60)) > 0.5:
                        totaltimein = int(totalsec/60) + 1
                    else:
                        totaltimein = int(totalsec/60)
                    totaltimeout = overalltimemin-totaltimein
                    checktime_object =  apichecktime.CheckTimeApi(checktime=mchecktime)
                    ctime = mchecktime.CheckTime(id=0,teacherSlotID=self.slotId,totaltimein=totaltimein,totaltimeout=totaltimeout,date=str(datetime.now().date()))
                    checktime_object.add_checktime(checktime=ctime)
                    checktime =checktime_object.checksingletime_details(teacherSlotID=self.slotId)
                    checktimedata = checktime
                    teacherslot_object = apiteacherslots.TeacherSlots(teacherslots=mteacherslots)
                    if totaltimein==0:
                        teacherSlot = mteacherslots.TeacherSlot
                        teacherSlot.id=self.slotId
                        teacherSlot.timetableId=self.timetableId
                        teacherSlot.status="Not Held"
                        teacherSlot.slot = 0
                        teacherslot_object.update_teacherslots_details(teacherslots=teacherSlot)
                    else:
                        if totaltimeout>=1:
                            teacherSlot = mteacherslots.TeacherSlot
                            teacherSlot.id=self.slotId
                            teacherSlot.timetableId=self.timetableId
                            teacherSlot.status="Late + Held"
                            teacherSlot.slot = 0
                            teacherslot_object.update_teacherslots_details(teacherslots=teacherSlot)
                        else:
                            teacherSlot = mteacherslots.TeacherSlot
                            teacherSlot.id=self.slotId
                            teacherSlot.timetableId=self.timetableId
                            teacherSlot.status="Held"
                            teacherSlot.slot = 0
                        
                            teacherslot_object.update_teacherslots_details(teacherslots=teacherSlot)
                    for (timein,timeout) in zip(lsttimein,lsttimeout):
                        # activityCount=0
                        # for tempActivityTime in lstActivityTime:
                        #     print(tempActivityTime)
                                    
                        checktimedetails_object =  apichecktimedetails.CheckTimeDetailsApi(checktimedetails=mchecktimedetails)
                        ctimedetails = mchecktimedetails.CheckTimeDetails(id=0,checkTimeID=checktimedata.id,timein=timein,timeout=timeout,sit=0,stand=0,mobile=0)
                        datetime.now()
                        checktimedetails_object.add_checktimedetails(checktimedetails=ctimedetails)   
                    self.sc=0
                    self.readImageCount=0
            
                    
   
                
        
    # def show_frame(self):
    #     if self.status:
    #         cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
    #         try:
    #             scale_percent = 10
    #             width = int(cv2image.shape[1] * scale_percent / 100)
    #             height = int(cv2image.shape[0] * scale_percent / 100)
    #             dim = (width, height)
    #             resized = cv2.resize(cv2image, dim, interpolation=cv2.INTER_AREA)
    #             img = Image.fromarray(resized)
    #         except:
    #             scale_percent = 60
    #             width = int(cv2image.shape[1] * scale_percent / 100)
    #             height = int(cv2image.shape[0] * scale_percent / 100)
    #             dim = (width, height)
    #             resized = cv2.resize(cv2image, dim, interpolation=cv2.INTER_AREA)
    #             img = Image.fromarray(resized)

    #         imgtk = ImageTk.PhotoImage(image=img)
            # if threading.current_thread().name == "1":
            #     lmain.imgtk = imgtk
            #     lmain.configure(image=imgtk)
            #     lmain.after(1, self.show_frame())
            # if threading.current_thread().name == "2":
            #     lmain1.imgtk = imgtk
            #     lmain1.configure(image=imgtk)
            #     lmain1.after(1, self.show_frame())

    def start_recording(self):
        fname = f'Recordings/file,{self.slotId},start_recording.mp4'
        rt = self.st + timedelta(seconds=60)
        print("start",self.st.time())
        print('record',rt.time())
        start_video = cv2.VideoWriter(fname, self.codec, 20, (self.frame_width, self.frame_height))
        
        while True:
            frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))
            start_video.write(frame)
            if datetime.now().time() > rt.time():
                # conn = MySQL()
                # conn.__enter__()
                # cursor = conn.conn.cursor()
                # cursor.execute(f'''
                #             SELECT * FROM TEACHERSLOTS WHERE ID='{self.slotid}'
                #                 ''')
                # for row in cursor.fetchall():
                #     if row.STATUS==0:
                #         cursor.execute(f'''
                #             UPDATE TEACHERSLOTS SET STATUS='{-1}' WHERE ID='{self.slotid}'
                #                 ''')
                start_video.release()
                print("done start")
                
                recording = mrecordings.Recordings(id=0,teacherSlotID=self.slotId,filename=fname,date=str(datetime.now().date()))
                rec_obj= apirecordings.RecordingsApi(recordings=mrecordings)
                rec_obj.add_recordings(recordings=recording)
                break

    def end_recording(self):
        fename = f'Recordings/file,{self.slotId},end_recording.mp4'
        count = 1
        rt = self.et - timedelta(seconds=60)
        print("end", self.et.time())
        print('record', rt.time())
        end_video = cv2.VideoWriter(fename, self.codec, 20, (self.frame_width, self.frame_height))
        while True:
            ct = datetime.now().time()
            while ct > rt.time() and ct<self.et.time():
                ct = datetime.now().time()
                frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))
                end_video.write(frame)
                count = 0
            if count == 0:
                end_video.release()
                print("done end")
                recording = mrecordings.Recordings(id=0,teacherSlotID=self.slotId,filename=fename,date=str(datetime.now().date()))
                rec_obj= apirecordings.RecordingsApi(recordings=mrecordings)
                rec_obj.add_recordings(recordings=recording)
                break

    def complete_recording(self):
        fcname = f'Recordings/file,{self.slotId},complete_recording.mp4'
        complete_video = cv2.VideoWriter(fcname, self.codec, 20, (self.frame_width, self.frame_height))
        while True:
            frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))
            complete_video.write(frame)
            if datetime.now().time() > self.et.time():
                complete_video.release()
                print("done complete")
                recording = mrecordings.Recordings(id=0,teacherSlotID=self.slotId,filename=fcname,date=str(datetime.now().date()))
                rec_obj= apirecordings.RecordingsApi(recordings=mrecordings)
                rec_obj.add_recordings(recordings=recording)
                break

    def check_time(self):
        if self.s == 1:
            sth = Thread(target=self.start_recording, args=())
            sth.start()
        if self.e == 1:
            eth = Thread(target=self.end_recording, args=())
            eth.start()
        if self.f== 1:
            cth = Thread(target=self.complete_recording, args=())
            cth.start()

        # if self.time.time() < ct:
        #     self.output_video.release()
        #     print("done")
        #     break
    def check_time_using_facial_recognition(self):
        if self._key_lock.locked():
            pass
        else:
            self._key_lock.acquire()
            temp_image_path = f'temp{self.timetableId}.JPG'
            cv2.imwrite(temp_image_path,self.frame)
            image = cv2.imread(temp_image_path)
            try:
                test_image = cv2.imread(temp_image_path)
                test_image = cv2.resize(test_image, (0, 0), fx=0.5, fy=0.5)
            except:
                test_image =  face_recognition.load_image_file(temp_image_path)
            #test_image =  face_recognition.load_image_file(temp_image_path)
            face_encodings = face_recognition.face_encodings(test_image)
            count=-1
            print(f'Face found={len(face_encodings)}')
            for face_encoding in face_encodings:
                #print(np.linalg.norm(np.expand_dims(self.image_encodings,axis=0) - face_encoding, axis=1))
                matches = face_recognition.compare_faces(np.expand_dims(self.image_encodings,axis=0),face_encoding)
                if True in matches:
                    #label = self.checkActivity(image)
                    label='Sit'
                    self.activityLabel.append(label)
                    self.teachertimeinframes+=1
                else:
                    self.teachertimeoutframes+=1
                count=0
            if count==-1:
                self.teachertimeoutframes+=1
                
            self.totalteachertimeframes+=1
            tempLabel=''
            if self.teachertimeinframes>0:
                tempLabel=self.activityLabel[self.teachertimeinframes-1]
            print(f'''
                Total Frames={self.totalteachertimeframes}
                Time In Frames={self.teachertimeinframes} Label = {tempLabel}
                Time Out Frames={self.teachertimeoutframes}
                ''')
            self._key_lock.release()
       
        
        
    def checkActivity(self,image):
        results = self.model.predict(image,stream=True, imgsz=640)
        label = self.get_label(results)
        return label
        
        
    def get_label(self,results):
        class_names=['Mobile','Sit','Stand']
        for r in results:
            label=''
            for c in r[0].boxes.cls:
                label = f'{class_names[int(c)]} '
                return label
    
       


