from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from deepface import DeepFace
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/recognize', methods=['POST'])
def recognize():
    file = request.files['file']
    file.save('uploaded_image.jpg')
    
    try:
        obj = DeepFace.analyze(img_path="uploaded_image.jpg", actions=['age'], enforce_detection=False)[0]
        response = {
            'age': obj['age'],
        }
    except ValueError:
        response = {'error': 'Face could not be detected in the uploaded image.'}

    return jsonify(response)

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    origin = data['origin']
    destination = data['destination']
    
    # origin 값을 출력하는 로그 추가
    print(f"Origin: {origin}")
    print(f"Destination: {destination}")
    
    url = "https://apis-navi.kakaomobility.com/v1/directions"
    headers = {
        "Authorization": "KakaoAK 919687c36b28a4c8875e33e33bb8d0e6",  # API 키
        "Content-Type": "application/json"
    }
    payload = {
        "origin": origin,
        "destination": destination,
        "priority": "RECOMMEND",  # 경로 우선순위 설정
        "car_fuel": "GASOLINE",  # 차량 연료 종류
        "car_hipass": False,  # 하이패스 여부
        "alternatives": False  # 대체 경로 제공 여부
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "경로를 찾을 수 없습니다."}), 400

def send_email(smtp_info, subject, html_content, recipient_email):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_info['smtp_user_id']
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # HTML 본문 추가
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP_SSL(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
            server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])
            server.sendmail(msg['From'], msg['To'], msg.as_string())

        return True
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {e}")
        return False

@app.route('/send_fare_email', methods=['POST'])
def send_fare_email():
    data = request.json
    fare = data['fare']
    start_address = data['start_address']
    end_address = data['end_address']
    start_time = data['start_time']
    end_time = data['end_time']
    recipient_email = data['email']
    
    # 현재 날짜를 가져와서 월과 일을 추출
    current_date = datetime.now()
    month = current_date.month
    day = current_date.day
    
    # 메일 제목 생성
    subject = f"퀵보드 사용 영수증 - {month}월 {day}일"
    
    # HTML 템플릿 생성
    html_content = f"""
    <html>
    <body>
        <h2>총 사용 금액: {fare}원</h2>
        <p><strong>탑승 시간:</strong> {start_time}</p>
        <p><strong>하차 시간:</strong> {end_time}</p>
        <hr>
        <p><strong>출발지:</strong> {start_address}</p>
        <p><strong>도착지:</strong> {end_address}</p>
    </body>
    </html>
    """
    
    success = send_email(smtp_info, subject, html_content, recipient_email)
    
    if success:
        return jsonify({"message": "Email sent successfully"}), 200
    else:
        return jsonify({"message": "Failed to send email"}), 500

smtp_info = {
    "smtp_server": "smtp.naver.com",
    "smtp_user_id": "YOUR_EMAIL_ADDRESS@naver.com",  # 송신자 이메일
    "smtp_user_pw": "YOUR_EMAIL_ACCOUNT_PASSWORD",
    "smtp_port": 465
}


@app.route('/scooter')
def scooter():
    return render_template('scooter.html')

if __name__ == '__main__':
    app.run(debug=True)
