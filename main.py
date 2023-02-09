import asyncio
import datetime
from datetime import datetime, timedelta
from pathlib import Path
import threading
from typing import List
from fastapi import Depends, FastAPI, Header, Request, Response, WebSocket, WebSocketDisconnect,File, UploadFile
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse,StreamingResponse
import cv2
import Model.DVR as mdvr
import Model.User as muser
import ApiFunctions.DVR as apidvr
import ApiFunctions.User as apiuser
import ApiFunctions.Course as apicourse
import Model.Course as mcourse
import Model.TimeTable as mtimetable
import ApiFunctions.TimeTable as apitimetable
import Model.Camera as mcamera
import ApiFunctions.Camera as apicamera
import Model.Enroll as menroll
import ApiFunctions.Enroll as apienroll
import Model.Section as msection
import ApiFunctions.Section as apisection
import Model.Venue as mvenue
import ApiFunctions.Venue as apivenue
import Model.Teach as mteach
import ApiFunctions.Teach as apiteach
import Model.Study as mstudy
import ApiFunctions.Study as apistudy
import Model.Recordings as mrecordings
import ApiFunctions.Recordings as apirecordings
import Model.Reschedule as mreschedule
import ApiFunctions.Reshedule as apireschedule
import Model.Rules as mrules
import Model.TeacherSlots as mteacherslots
import nest_asyncio
from VideoRecording import RTSPVideoWriterObject
from sql import MySQL
from fastapi.responses import HTMLResponse
nest_asyncio.apply()

networkip = '192.168.43.192'
networkport = 8000
# 'rtsp://192.168.0.108:8080/h264_ulaw.sdp'
app = FastAPI()

# templates = Jinja2Templates(directory="templates")
# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("indexweb.html", {"request": request})


# CHUNK_SIZE = 1024*1024
# file_path = "Recordings/file,33,complete_recording.mp4"


# @app.get("/video")
# async def video_feed():
#    return FileResponse(file_path)

CHUNK_SIZE = 1024*1024




@app.get("/video")
async def video_endpoint(range: str = Header(None),path:str=None):
    video_path = Path(path)
    if range==None:
        range = "bytes=0-"
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    print(range)
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
#---------------------------Camera-----------------------------------------

    
def connect(websocket,count):
        asyncio.set_event_loop(asyncio.new_event_loop())
        async def  connect(websocket,count):
            await websocket.accept()
            camera = cv2.VideoCapture('rtsp://192.168.43.1:8000/h264_ulaw.sdp')
            # if count==1:
            #     camera = cv2.VideoCapture('rtsp://192.168.43.228:8080/h264_ulaw.sdp')
            #     count+=1
            # else:
            #     camera = cv2.VideoCapture('rtsp://192.168.43.118:8080/h264_ulaw.sdp')
            while True:
                success, frame = camera.read()
                if not success:
                    break
                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    await websocket.send_bytes(buffer.tobytes()) 
        asyncio.get_event_loop().run_until_complete(connect(websocket,count))
        
# async def  connect1(websocket,count):
#         await websocket.accept()
#         if count==1 or count==2:
#             camera = cv2.VideoCapture('rtsp://192.168.43.228:8080/h264_ulaw.sdp')
#             count+=1
#         else:
#             camera = cv2.VideoCapture('rtsp://192.168.43.118:8080/h264_ulaw.sdp')
#         while True:
#             success, frame = camera.read()
#             if not success:
#                 break
#             else:
#                 ret, buffer = cv2.imencode('.jpg', frame)
#                 await websocket.send_bytes(buffer.tobytes()) 

@app.websocket("/{count}/ws")
async def get_stream(websocket: WebSocket,count: int):
    try:
        connect(websocket,count)
        # Thread(target=asyncio.run,args=(connect1(websocket=websocket,count=count))).start()
    except WebSocketDisconnect:
        print("Client disconnected")   


#------------------------------------------------Video Recordings----------------------------------------------------------------

def iterfile(id,record):
    video_path=f'Recordings/file,{id},{record}_recording.avi'
    outputFrame = cv2.VideoCapture(video_path)
    while True:
        status,img= outputFrame.read()
        if status==False:
            break
        (flag, encodedImage) = cv2.imencode(".jpg", img)
        if not flag:
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

@app.get('/get-video-recordings/{id}/{record}')
def getvideo(id:str,record:str):
    return StreamingResponse(iterfile(id,record), media_type="multipart/x-mixed-replace;boundary=frame")


def cam(ip, s, e, f,stime,etime,day,teacher_slot,teacher_id):
    st = datetime.now()
    et = st + timedelta(minutes=2)
    stime= st
    etime =  et
    print(ip, s, e, f,stime,etime,day,teacher_slot)
    video_stream_widget = RTSPVideoWriterObject(ip, s, e, f,stime, etime,day,teacher_slot,teacher_id)
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass

        
@app.get('/stream')
def start_stream():
    lsttm =  timetable_object.getalltimetable()
    sql = MySQL()
    sql.__enter__()
    cursor = sql.conn.cursor()
    for timetable in lsttm:
        if timetable.id ==11:
            cursor.execute(f'''
                    SELECT * FROM CAMERA WHERE VenueID='{timetable.venueID}'
                        ''')
            for row in cursor.fetchall():
                cursor.execute(f'''
                    SELECT * FROM DVR WHERE ID='{row.DvrID}'
                        ''')
                dvrip=''
                for dvrrow in cursor.fetchall():
                    dvrip=dvrrow.IP
                cursor.execute(f'''
                        SELECT * FROM TEACH WHERE TimeTableID='{timetable.id}'
                            ''')
                lst=[]
                teacher_id=-1
                for row in cursor.fetchall():
                    lst.append(mteach.Teach(id=row.ID,timeTableID=row.TimeTableID,teacherID=row.TeacherID))
                    teacher_id = row.TeacherID
                for teach in lst:
                    cursor.execute(f'''
                            SELECT * FROM RULES WHERE TeachID='{teach.id}'
                                ''')
                    rules=None
                    for row in cursor.fetchall():
                        rules =  mrules.Rules(id=row.ID,teachID=row.TeachID,start_record=row.START_RECORD,end_record=row.END_RECORD,full_record=row.FULL_RECORD)
                    cursor.execute(f'''
                            SELECT * FROM TEACHERSLOTS WHERE TeachID='{teach.id}'
                                ''') 
                    teacher_slot=None
                    for row in cursor.fetchall():
                        if row.STATUS == 0:
                            teacher_slot = mteacherslots.TeacherSlot(id=row.ID,teachID=row.TeachID,slot=row.SLOT,status=row.STATUS)
                            break
                    
                    t1 = threading.Thread(target=cam, args=(f'rtsp://{dvrip}:8000/h264_ulaw.sdp', rules.start_record, rules.end_record, rules.full_record,timetable.starttime,timetable.endtime,timetable.day.value,teacher_slot,teacher_id))
                    t1.start()
    

#---------------------------DVR-----------------------------------------


@app.post('/api/add-dvr') 
def adddvr(dvr : mdvr.DVR):
    return dvr_object.add_dvr(dvr=dvr)

@app.get('/api/dvr-details') 
def dvrdetails():
    return dvr_object.dvr_details()
    
@app.put('/api/update-dvr-details') 
def updatedvrdetails(dvr : mdvr.DVR):
    return dvr_object.update_dvr_details(dvr=dvr)
    
    
@app.delete('/api/delete-dvr-details') 
def deletedvrdetails(dvr : mdvr.DVR):
    return dvr_object.delete_dvr_details(dvr=dvr)

#---------------------------------Camera---------------------------------

@app.post('/api/add-camera') 
def addcamera(camera : mcamera.Camera):
    return camera_object.add_camera(camera=camera)

@app.get('/api/camera-details/{dvrID}') 
def cameradetails(dvrID:int):
    return camera_object.camera_details(dvrID)
    
@app.put('/api/update-camera-details') 
def updatecameradetails(camera : mcamera.Camera):
    return camera_object.update_camera_details(camera=camera)
    
    
@app.delete('/api/delete-camera-details') 
def deletecameradetails(camera : mcamera.Camera):
    return camera_object.delete_camera_details(camera=camera)


#---------------------------User-----------------------------------------
@app.post('/api/add-user') 
def adduser(user : muser.User=Depends(),file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        foldername = user.role.value
        path=f"UserImages/{foldername}/{file.filename}"
        with open(path, 'wb') as f:
            f.write(contents)
        user.image = file.filename
        # image =  face_recognition.load_image_file(path)
        # image_encoding = face_recognition.face_encodings(image)[0]
        # return {"data":image_encoding.tolist()}
        return user_object.add_user(user=user)
    except Exception:
        print(Exception)
        return {"data": "There was an error uploading the file"}
    finally:
        file.file.close()
    

@app.get('/api/user-details') 
def userdetails():
    return user_object.user_details()
    
@app.get('/api/get-user-image/UserImages/{foldername}/{imagename}') 
def getuserimage(foldername:str,imagename:str):
    return FileResponse(f'UserImages/{foldername}/{imagename}')

    
@app.put('/api/update-user-details') 
def updateuserdetails(user : muser.User):
    return user_object.update_user_details(user=user)
    
    
@app.delete('/api/delete-user-details') 
def deleteuserdetails(user : muser.User):
    return user_object.delete_user_details(user=user)

#---------------------------------COURSE---------------------------------
@app.post('/api/add-course') 
def addcourse(course : mcourse.Course):
    return course_object.add_course(course=course)

@app.get('/api/course-details') 
def coursedetails():
    return course_object.course_details()
    
@app.put('/api/update-course-details') 
def updatecoursedetails(course : mcourse.Course):
    return course_object.update_course_details(course=course)
    
    
@app.delete('/api/delete-course-details') 
def deletecoursedetails(course : mcourse.Course):
    return course_object.delete_course_details(course=course)


#---------------------------------TimeTable---------------------------------

@app.post('/api/add-timetable') 
def addtimetable(timetable : mtimetable.TimeTable):
    return timetable_object.add_timetable(timetable=timetable)

@app.get('/api/timetable-details/{timetableid}') 
def timetabledetails(timetableid: int):
    return timetable_object.timetable_details(timetableid=timetableid)
    
@app.put('/api/update-timetable-details') 
def updatetimetabledetails(timetable : mtimetable.TimeTable):
    return timetable_object.update_timetable_details(timetable=timetable)
    
    
@app.delete('/api/delete-timetable-details') 
def deletetimetabledetails(timetable : mtimetable.TimeTable):
    return timetable_object.delete_timetable_details(timetable=timetable)

#---------------------------------Enroll---------------------------------

@app.post('/api/add-enroll') 
def addenroll(enroll : menroll.Enroll):
    return enroll_object.add_enroll(enroll=enroll)

@app.get('/api/enroll-details') 
def enrolldetails():
    return enroll_object.enroll_details()
    
@app.put('/api/update-enroll-details') 
def updateenrolldetails(enroll : menroll.Enroll):
    return enroll_object.update_enroll_details(enroll=enroll)
    
    
@app.delete('/api/delete-enroll-details') 
def deleteenrolldetails(enroll : menroll.Enroll):
    return enroll_object.delete_enroll_details(enroll=enroll)


#---------------------------------Venue---------------------------------
@app.post('/api/add-venue') 
def addvenue(venue : mvenue.Venue):
    return venue_object.add_venue(venue=venue)

@app.get('/api/venue-details') 
def venuedetails():
    return venue_object.venue_details()
    
@app.put('/api/update-venue-details') 
def updatevenuedetails(venue : mvenue.Venue):
    return venue_object.update_venue_details(venue=venue)
    
    
@app.delete('/api/delete-venue-details') 
def deletevenuedetails(venue : mvenue.Venue):
    return venue_object.delete_venue_details(venue=venue)

#---------------------------------Section---------------------------------
@app.post('/api/add-section') 
def addsection(section : msection.Section):
    return section_object.add_section(section=section)

@app.get('/api/section-details') 
def sectiondetails():
    return section_object.section_details()
    
@app.put('/api/update-section-details') 
def updatesectiondetails(section : msection.Section):
    return section_object.update_section_details(section=section)
    
    
@app.delete('/api/delete-section-details') 
def deletesectiondetails(section : msection.Section):
    return section_object.delete_section_details(section=section)

#---------------------------------Teach---------------------------------
@app.post('/api/add-teach') 
def addteach(teach : mteach.Teach):
    return teach_object.add_teach(teach=teach)

@app.get('/api/teach-details/{teacherid}') 
def teachdetails(teacherid:int):
    return teach_object.teach_details(teacherid=teacherid)
    
@app.put('/api/update-teach-details') 
def updateteachdetails(teach : mteach.Teach):
    return teach_object.update_teach_details(teach=teach)
    
   
@app.delete('/api/delete-teach-details') 
def deleteteachdetails(teach : mteach.Teach):
    return teach_object.delete_teach_details(teach=teach)


#---------------------------------Study---------------------------------

@app.post('/api/add-study') 
def addstudy(study : mstudy.Study):
    return study_object.add_study(study=study)

@app.get('/api/study-details') 
def studydetails():
    return study_object.study_details()
    
@app.put('/api/update-study-details') 
def updatestudydetails(study : mstudy.Study):
    return study_object.update_study_details(study=study)
    
    
@app.delete('/api/delete-study-details') 
def deletestudydetails(study : mstudy.Study):
    return study_object.delete_study_details(study=study)

#---------------------------------Recordings---------------------------------
@app.post('/api/add-recordings') 
def addrecordings(recordings : mrecordings.Recordings):
    return recordings_object.add_recordings(recordings=recordings)

@app.get('/api/recordings-details') 
def recordingsdetails():
    return recordings_object.recordings_details()

@app.get('/api/recordings-details-by-teacherid/{teacherid}') 
def recordingsdetailsbyteacherid(teacherid:int):
    return recordings_object.recordings_details_byteacherid(teacherid=teacherid)

  
@app.put('/api/update-recordings-details') 
def updaterecordingsdetails(recordings : mrecordings.Recordings):
    return recordings_object.update_recordings_details(recordings=recordings)
    
    
@app.delete('/api/delete-recordings-details') 
def deleterecordingsdetails(recordings : mrecordings.Recordings):
    return recordings_object.delete_recordings_details(recordings=recordings)

#---------------------------------ReSchedule---------------------------------
@app.post('/api/add-reschedule') 
def addreschedule(reschedule : mreschedule.Reschedule):
    return reschedule_object.add_reschedule(reschedule=reschedule)

@app.get('/api/reschedule-details') 
def rescheduledetails():
    return reschedule_object.reschedule_details()

@app.get('/api/get-timetable') 
def gettimetable():
    return reschedule_object.getTimetable()

class lststr(BaseModel):
    lstday : List[str]
    startdate:str
    enddate:str
@app.post('/api/get-timetable-bydates') 
def gettimetablebydates(data: lststr):
    return reschedule_object.gettimetablebydates(startdate=data.startdate,enddate=data.enddate,lstday=data.lstday)
    
@app.put('/api/update-reschedule') 
def updaterescheduledetails(reschedule : mreschedule.Reschedule):
    return reschedule_object.update_reschedule_details(reschedule=reschedule)
    
    
@app.delete('/api/delete-reschedule') 
def deleterescheduledetails(reschedule : mreschedule.Reschedule):
    return reschedule_object.delete_reschedule_details(reschedule=reschedule)


        
if __name__=='__main__':
    
    dvr_object =  apidvr.DVRApi(dvr=mdvr)
    camera_object =  apicamera.CameraApi(cam=mcamera)
    user_object = apiuser.UserApi(user=muser)
    course_object = apicourse.CourseApi(course=mcourse)
    timetable_object = apitimetable.TimeTableApi(timetable=mtimetable)
    enroll_object = apienroll.EnrollApi(enroll=menroll)
    venue_object = apivenue.VenueApi(venue=mvenue)
    section_object = apisection.SectionApi(section=msection)
    teach_object = apiteach.TeachApi(teach=mteach)
    study_object = apistudy.StudyApi(study=mstudy)
    recordings_object = apirecordings.RecordingsApi(recordings=mrecordings)
    reschedule_object = apireschedule.RescheduleApi(reschedule=mreschedule)
    uvicorn.run(app, host=networkip,port=networkport)
    
    
    
    
    
    
    
    
    
    
    
   