import json
import os
from flask import Flask
from flask import request
from flask import make_response

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST'])

def MainFunction():

    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)

    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป

    return r

def generating_answer(question_from_dailogflow_dict):

    #Print intent ที่รับมาจาก Dailogflow
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #เก็บค่า ชื่อของ intent group ที่รับมาจาก Dailogflow
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 
    print(intent_group_question_str)

    #ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str == 'grade - custom':
        answer_str = grade_calculator(question_from_dailogflow_dict)
    elif intent_group_question_str == 'บวก':
        answer_str = "พร้อมพวกแล้ว"
    else: 
        answer_str = "พูดไรนิ"

    #สร้างการแสดงของ dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def grade_calculator(res):
    score = float(res["queryResult"]["outputContexts"][1]["parameters"]["score.original"])
    if score == 99:
        return "หูยเก่งจุง"
    return "คะแนนเท่านี้แน่นะ "+str(score)


#กำหนด port ให้ flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)