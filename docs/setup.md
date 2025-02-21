# 설치 및 설정 가이드

## 하드웨어 요구사항
- Raspberry Pi 5
- Raspberry Pi Camera Module 3
- 부저 모듈
- GPIO 연결 케이블

## 소프트웨어 설치
1. 필요한 패키지 설치:
bash
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-picamera2

2. Python 패키지 설치:
bash
pip3 install -r requirements.txt

3. 카메라 활성화:
bash
sudo raspi-config
Interface Options -> Camera -> Enable


## 하드웨어 연결
1. 부저 모듈:
   - GPIO 18번 핀에 연결
   - GND는 라즈베리파이의 GND 핀에 연결

## 실행 방법
bash
cd src
python3 main.py

## 주의사항
- 텔레그램 봇 토큰과 채팅 ID는 settings.py에서 설정
- 카메라 모듈이 정상적으로 연결되어 있는지 확인
- GPIO 핀 번호 확인
