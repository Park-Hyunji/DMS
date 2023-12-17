import io
import time
import paho.mqtt.client as mqtt
import circuit
from PIL import Image, ImageFilter
import base64
import cv2

def publish_image(client, image, topic):
    _, buffer = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    client.publish(topic, payload=encoded_image, qos=0, retain=False)


def on_connect(client, userdata, flag, rc):
    pass

def capture():
    ret, frame = circuit.camera.read()
    resized_frame = cv2.resize(frame, (640, 480))
    publish_image(client, resized_frame, "dogimage")    

circuit.inithw() # 최초 시작

ip = "localhost" # 브로커 IP 주소 입력

client = mqtt.Client()
client.on_connect = on_connect

client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

prevdistance=0 # 거리 초기화

while True:
    circuit.runhw()
    distance = circuit.measure_distance()
            
    prevdistance = distance # 이전 prevdistance를 distance로 갱신 

    tem = circuit.getTemperature() # tem에 circuit.py에서 측정한 온도 값 저장
    hum = circuit.getHumidity() # hum에 circuit.py에서 측정한 습도 값 저장

    # 결과 출력
    client.publish("dogstatus",f"온도:{tem:10.2f}℃ 습도:{hum:10.2f}% 거리:{distance:10.2f}cm",qos=0)
    
