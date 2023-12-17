import io
import cv2
from PIL import Image, ImageFilter
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import board
import busio
 

# pin 에 연결된 LED 에 value(0/1) 값을 출력하여 LED 를 켜거나 끄는 함수
def led_on_off(pin, value):
    GPIO.output(pin, value)

def measure_distance():
	GPIO.output(trig, 1) # trig 핀에 1(High) 출력
	GPIO.output(trig, 0) # trig 핀에 0(Low) 출력. 1->0 초음파 발사 지시

	while(GPIO.input(echo) == 0): # echo 핀 값이 0 ->1 로 바뀔 때까지 루프
		pass

	# echo 핀 값이 1이면 초음파가 발사되었음
	pulse_start = time.time() # 초음파 발사 시간 기록
	while(GPIO.input(echo) == 1): # echo 핀 값이 1->0으로 바뀔 때까지 루프
		pass
	
	# echo 핀 값이 0이 되면 초음파 수신
	pulse_end = time.time() # 초음파가 되돌아 온 시간 기록
	pulse_duration = pulse_end - pulse_start # 시간 계산
	return pulse_duration*340*100/2 # 거리 계산하여 리턴(단위 cm)

def getTemperature() : # 센서로부터 온도 값 수신 함수
    global sensor
    return float(sensor.temperature) # HTU21D로부터 온도 값 읽어오기

def getHumidity() : # 센서로부터 습도 값 수신 함수
    global sensor
    return float(sensor.relative_humidity) # HTU21D로부터 습도 값 읽어오기

def inithw(): # 최초 시작
    global sensor, led1, led2, led3, trig, echo, camera # 사용할 객체들
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = HTU21D(i2c) # HTU21D 장치를 제어 객체
    led1 = 6 # GPIO6 핀에 LED1 연결
    led2 = 5 # GPIO5 핀에 LED2 연결
    led3 = 13 # GPIO13 핀에 LED3 연결
    trig = 20 # GPIO20 
    echo = 16 # GPIO16

    GPIO.setmode(GPIO.BCM) # BCM 모드
    GPIO.setup(trig, GPIO.OUT) # GPIO20 핀을 출력으로 지정
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(led1, GPIO.OUT) # GPIO6 핀을 출력으로 지정
    GPIO.setup(led2, GPIO.OUT) # GPIO5 핀을 출력으로 지정
    GPIO.setup(led3, GPIO.OUT) # GPIO13 핀을 출력으로 지정

    # 카메라 객체를 생성
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 프레임을 임시 저장할 버퍼 개수를 1 로 설정
    buffer_size = 1
    camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
 

def runhw():
    global sensor, led1, led2, led3, trig ,echo

    distance = measure_distance() # 거리 측정
    time.sleep(0.5) # 0.5 초 간격으로 거리 측정
    
    if(distance<=10): # 물체와의 거리가 10cm 이내 일 때
        led_on_off(led1,1) # led1 on
        led_on_off(led2,1) # led2 on
        led_on_off(led3,1) # led3 on
    elif(distance<=20): # 물체와의 거리가 20cm 이내 일 때
        led_on_off(led1,1) # led1 on
        led_on_off(led2,1) # led2 off
        led_on_off(led3,0) # led2 off
    elif(distance<=30): # 물체와의 거리가 30cm 이내 일 때
        led_on_off(led1,1) # led1 on
        led_on_off(led2,0) # led2 off
        led_on_off(led3,0) # led2 off
    else: # 물체와의 거리가 30cm 보다 멀 때
        led_on_off(led1,0) # led1 off
        led_on_off(led2,0) # led2 off
        led_on_off(led3,0) # led3 off