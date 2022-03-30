from flask import make_response
from flask import request
from flask import Flask
import os
import json
from asyncio import constants
from flask import Flask, request, jsonify
app = Flask(__name__)


# Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])
def MainFunction():

    # รับ intent จาก Dailogflow
    rawMessage = request.get_json(silent=True, force=True)

    # เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    bot_respone = generating_answer(rawMessage)

    # ตอบกลับไปที่ Dailogflow
    print(bot_respone)
    r = make_response(bot_respone)
    # การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป
    r.headers['Content-Type'] = 'application/json'

    return r


def generating_answer(message):

    # Print intent ที่รับมาจาก Dailogflow
    # print(json.dumps(message, indent=4 ,ensure_ascii=False))

    # เก็บค่า ชื่อของ intent group ที่รับมาจาก Dailogflow
    intentGroup = message["queryResult"]["intent"]["displayName"]
    print("intnent group: ", intentGroup)

    # ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intentGroup == 'grade - custom':
        answer = grade_calculator(message)
    elif intentGroup == 'บวก':
        answer = "พร้อมบวกแล้วน้าาา"
    elif intentGroup == 'gpsTest':
        return json.dumps({
            "address": "2194 ถนน เจริญกรุง แขวง วัดพระยาไกร เขตบางคอแหลม กรุงเทพมหานคร 101200",
            "title": "เอเชียทีค เดอะ ริเวอร์ฟร้อนท์",
            "latitude": 13.704435,
            "type": "location",
            "longitude": 100.503212
        },ensure_ascii=False)
    elif intentGroup == 'imgTest':
        return json.dumps({"fulfillmentText": "ลองรูป"})
    else:
        answer = "พูดไรนิ"

    # สร้างการแสดงของ dict
    botResponse = {"fulfillmentText": answer}

    # แปลงจาก dict ให้เป็น JSON
    botResponse = json.dumps(botResponse)

    return botResponse


def grade_calculator(res):
    score = float(res["queryResult"]["outputContexts"]
                  [1]["parameters"]["score.original"])
    if score == 99:
        return "หูยเก่งจุง"
    return "อ่อนเกิ้น"


# กำหนด port ให้ flask
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
