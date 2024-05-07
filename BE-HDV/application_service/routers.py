from datetime import datetime
import json
import os
import re
import pika
import requests
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import File, Body
from worker import public
import time

router = APIRouter(
    prefix="/api/application",
    tags=["api"],
)

@router.get("/")
def index():
    return {"message": "Hello World"}


@router.post("/checkin")
def checkin(zoom_id: str, file: bytes, time: str):
    return {"message": "Checkin Success"}

@router.post("/to_json/{meeting_id}", response_model=dict) #Todo:  handle checkin after
def excel_to_json(file: UploadFile = File(...), meeting_id: str = None):
    public(f"(application-service) Start getting participants for meeting_id: {meeting_id}...")
    start_time = time.time()

    print(meeting_id)
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    json_data = requests.post('http://localhost:8001/api/convert/excel_to_json', files={"file": (file.filename, open(file.filename, "rb"))})
    json_data = json_data.json()
    os.remove(file.filename)
    # os.remove('temp.xlsx')
    if not json_data:
        raise HTTPException(status_code=400, detail="Convert Failed")
    data_meeting = requests.get(f'http://localhost:5000/api/googlemeet/get_participants?meeting_id={meeting_id}')
    data_meeting_json = data_meeting.json()
    print(data_meeting_json)

    data_formated = []
    cnt = 1
    for data in json_data:
        json_item = {
            "id": cnt,
            "student_code": data['Mã sinh viên'],
            "student_name": data['Tên sinh viên'],
            "status": "",
            "time_in": "",
            "time_out": ""
        }
        cnt += 1
        data_formated.append(json_item)

    for data in data_meeting_json:
        str = data['signedin_user']['display_name'].split()
        msv = ''
        for i in str:
            if re.match(r'^B.*DCCN', i):
                # msv_set.add(i.decode('utf-8').strip('",'))
                msv = i.strip('",')
        for f in data_formated:
            if msv == f['student_code']:
                f['status'] = "1"
                f['time_in'] = data['start_time']
                f['time_out'] = data['end_time']

    # for data in data_formated:
    #     item = {
    #         "id_meet": meeting_id,
    #         "id_student": data['student_code'],
    #         "student_name": data['student_name'],
    #         "status": data['status'],
    #         "start_time": data['time_in'],
    #         "end_time": data['time_out'] if data['time_out'] else "Chua out"
    #     }
    #     print(json.dumps(item))
    #     try:
    #         response = requests.post('http://localhost:8003/api/attendance', data=json.dumps(item))
    #         if response.status_code == 200:
    #             print(response.text)
    #         else:
    #             print(response)
    #         print("hihi")
    #     except e:
    #         print(e)
    data_meeting = []
    for item in data_meeting_json:
        data_meeting.append({
            "account": item['signedin_user']['display_name'],
            "start_time": datetime.strptime(item['start_time'], "%a, %d %b %Y %H:%M:%S %Z").strftime("%H:%M:%S %d/%m/%Y"),
            "end_time": datetime.strptime(item['end_time'], "%a, %d %b %Y %H:%M:%S %Z").strftime("%H:%M:%S %d/%m/%Y") if item['end_time'] else None
        })
    print(data_meeting)


    end_time = time.time()
    public(f"(application-service) End getting participants for meeting_id: {meeting_id} - ({int(end_time - start_time)}ms)")
    public(f"Done")
    return {
        "meeting_id": meeting_id,
        "code": 200,
        "message": "Convert Success",
        "data": data_formated,
        "data_meet": data_meeting
    }
#Todo: handle export to excel
# @router.post("/to_excel")
# def json_to_excel(data: list = Body(...), file_name: str = None):
#     if not data:
#         raise HTTPException(status_code=400, detail="Data is required")
#     if not file_name:
#         file_name = 'output.xlsx'
#     if not convert.json_to_excel(data, file_name):
#         raise HTTPException(status_code=400, detail="Convert Failed")
#
#     return FileResponse(file_name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)
#
#

@router.post('/create_meet')
def create_meeting():
    response = requests.post('http://localhost:5000/api/googlemeet/create_meet')
    if response.status_code == 200:
        print("API call create meet was successful")
        return response.json()
    else:
        print("API call failed: status code: {response.status_code}")


@router.get('/messages')
def get_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    method_frame, header_frame, body = channel.basic_get('service')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        print(body.decode())
        return {
            'message': body.decode()
        }
    else:
        return {
            'message': ''
        }