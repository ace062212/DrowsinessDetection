# 🚗 라즈베리파이 기반 졸음운전 방지 시스템
**소프트웨어 인재육성 캠프 은상 수상작**  
**실제 산업 현장에서 사용할 수 있을까? 라는 고민에서 시작된 프로젝트**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![RaspberryPi](https://img.shields.io/badge/Raspberry%20Pi-5-C51A4A?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.7.0-green?style=for-the-badge&logo=opencv&logoColor=white)
![Hardware](https://img.shields.io/badge/Hardware-Embedded-orange?style=for-the-badge&logo=raspberrypi&logoColor=white)
![Award](https://img.shields.io/badge/Award-은상수상-silver?style=for-the-badge&logo=trophy&logoColor=white)

---

## 🏆 프로젝트 성과

### 🥈 **소프트웨어 인재육성 캠프 은상 수상 (2024)**
- **주관**: 소프트웨어 인재육성 캠프
- **수상 분야**: IoT/임베디드 시스템 부문
- **수상 이유**: 실용성과 기술적 완성도를 인정받아 은상 수상
- **의미**: 라즈베리파이 기반 실용적 시스템의 우수성 공식 인정

---

## 🎯 프로젝트 동기

### 🤔 "정말 실용적인 시스템을 만들 수 있을까?"

**개발 배경:**
- 일반 PC가 아닌 **실제 산업 현장에서 사용할 수 있는 시스템** 개발 욕구
- 졸음운전으로 인한 교통사고 문제의 심각성 인식
- **"이론이 아닌 현실에서 작동하는 기술"**을 만들고 싶었던 도전

**개발 기간**: 2024년 9월  
**핵심 질문**: *"버스회사에서 정말 이런 시스템을 원할까?"*

---

## 💡 실용성을 위한 철저한 시장 조사

### 📞 **고속버스 회사 직접 문의**
**"실제로 현장에서 필요한 기능이 무엇인지 알고 싶었어요"**

**조사 내용:**
- 실제 고속버스 회사 여러 곳에 전화 문의
- 기존에 사용 중인 졸음운전 방지 시스템 현황 파악  
- 현장에서 느끼는 기존 시스템의 한계점 청취
- 운전기사들이 원하는 기능과 불편사항 조사

**조사 결과:**
- 대부분 간단한 경고음 시스템만 사용 중
- **오탐지가 많아서** 운전기사들이 시스템을 꺼버리는 경우 빈발
- **실시간 모니터링**과 **정확한 감지**에 대한 니즈 확인

### 🗺️ **졸음운전 위험 구간 분석**
**"어느 구간에서 가장 위험할까? 데이터로 확인해보자"**

**분석 과정:**
- [고속도로 노선별 교통사고 현황 데이터](https://drive.google.com/drive/folders/1Z_oWJ6AM-Q1QZdBMZnO8jVkCdGuHndzZ?usp=sharing) 활용
- **R을 활용한 교통사고 데이터 시각화**
- 졸음운전 사고가 빈발하는 경로 및 시간대 분석
- Google Maps API를 통한 위험구간 지도 시각화

---

## 🔧 라즈베리파이, 그리고 임베디드의 세계

### 💻 **PC에서 라즈베리파이로의 전환**
**"컴퓨터는 컴퓨터인데, 뭔가 다르더라..."**

**라즈베리파이 경험:**
- **제한된 성능** 속에서 실시간 영상 처리 최적화 경험
- **GPIO 제어**를 통한 하드웨어 직접 제어의 매력
- **실제 제품화**를 위한 소형화, 저전력의 중요성 체감

**하드웨어 구성:**
- **Raspberry Pi 5**: 메인 컴퓨팅 유닛
- **Camera Module 3**: 고해상도 실시간 영상 입력
- **부저 모듈**: 즉각적인 경고음 출력
- **GPIO 연결**: 하드웨어 제어 인터페이스

### 🏭 **산업 현장을 위한 설계**
**"실제 버스에 설치한다면?"**

**실용성 고려사항:**
1. **30km/h 이상에서만 동작**: 시내 정차 시 불필요한 경고 방지
2. **다중 경고 시스템**: 
   - 부저를 통한 즉각적 청각 경고
   - 화면 표시를 통한 시각적 경고  
   - 텔레그램을 통한 관제센터 원격 알림
3. **데이터 기록**: MySQL 연동으로 운행 기록 관리

---

## 🛠 핵심 기술 구현

### 👁️ **정확한 졸음 감지 알고리즘**
```python
# 눈 감김 감지
def detect_eyes(self, frame):
    eyes_open, _ = self.eye_detector.detect_eyes(frame)
    if not eyes_open:
        if time.time() - self.blink_start_time >= BLINK_TEXT_TIME:
            self.trigger_buzzer(1.0)
            send_telegram_message("졸음 감지! 즉시 조치 필요!")
            upload_to_database(0, 1)
```

**감지 방식:**
- **OpenCV + Mediapipe**: 얼굴 랜드마크 기반 정밀 감지
- **눈 감김 시간 측정**: 단순 깜빡임과 졸음 구분
- **하품 횟수 카운트**: 3회 연속 하품 시 경고

### 🔔 **스마트한 경고 시스템**
```python
# 속도 기반 활성화
if self.speed >= 30:
    if not self.eye_detection_active:
        self.picam2.start()
        self.eye_detection_active = True
        self.trigger_notification_buzzer()
```

**특징:**
- **속도 연동**: 30km/h 이상에서만 활성화로 오탐지 최소화
- **단계적 경고**: 1차 부저 → 2차 화면 표시 → 3차 원격 알림
- **실시간 모니터링**: 관제센터에서 실시간 상황 파악 가능

---

## 📊 교통사고 데이터 분석

### 📈 **R을 활용한 위험구간 분석**

**분석 파일별 기능:**

1. **route_analysis_1.R**: 기본 노선 데이터 처리
   ```r
   # 노선별 위치 데이터 지오코딩
   data <- load_accident_data("path/to/data.csv")
   routes <- calculate_routes(data)
   visualize_routes(routes)
   ```

2. **route_analysis_2.R**: 고속도로 Shapefile 처리
   ```r
   # 고속도로 공간 데이터 분석
   highway_data <- load_shapefile("path/to/shapefile.shp")
   filtered_data <- filter_highways(highway_data)
   plot_highways(filtered_data)
   ```

3. **route_analysis_3.R**: 교통사고 현황 시각화
   ```r
   # 사고 다발 구간 분석
   accident_data <- sort_accident_data(data)
   visualize_accident_data(map, accident_data, "fatalities")
   analyze_intersections(route_data, accident_data)
   ```

### 🗺️ **시각화 결과**
- **사고 건수 히트맵**: 위험구간 한눈에 파악
- **사망자/부상자 분포도**: 심각도별 구간 분류
- **노선 교차점 분석**: 복잡 구간 위험도 평가

---

## 🏗️ 시스템 아키텍처

### 📋 **전체 시스템 구조**
```
라즈베리파이 기반 졸음운전 방지 시스템
├── 하드웨어 레이어
│   ├── Raspberry Pi 5 (메인 컴퓨팅)
│   ├── Camera Module 3 (영상 입력)
│   └── 부저 모듈 (경고음 출력)
├── 소프트웨어 레이어  
│   ├── 실시간 영상 처리 (OpenCV)
│   ├── 졸음 감지 알고리즘 (Mediapipe)
│   ├── 경고 시스템 (GPIO 제어)
│   └── 데이터 관리 (MySQL)
└── 통신 레이어
    ├── 텔레그램 알림
    └── 데이터베이스 연동
```

### 🔧 **주요 모듈**

**Detection 모듈:**
- `eye_detector.py`: 눈 감김 상태 실시간 감지
- `mouth_detector.py`: 하품 감지 및 횟수 카운트

**Utils 모듈:**
- `database.py`: MySQL 데이터베이스 연동
- `notification.py`: 텔레그램 메시지 전송
- `display.py`: 실시간 상태 표시

---

## 📊 실제 검증 및 성과

### ✅ **현장 적용 가능성 검증**
**"정말 버스에서 쓸 수 있을까?"**

**테스트 결과:**
- **오탐지율 대폭 감소**: 30km/h 이상에서만 동작으로 시내 운행 중 오탐지 방지
- **실시간 성능**: 라즈베리파이 5에서 30fps 안정적 처리
- **전력 효율성**: 저전력으로 장시간 운행 중 사용 가능

**실용성 확인:**
- 실제 고속버스 노선 시뮬레이션 테스트
- 다양한 조명 조건에서 안정적 감지
- 운전기사 피로도와 감지 정확도 상관관계 분석

### 📈 **데이터 기반 안전성 개선**
- **위험구간 사전 경고**: 교통사고 데이터 분석 결과 기반
- **개인별 피로도 패턴**: 운전기사별 졸음 패턴 데이터 축적
- **예방적 관리**: 사고 발생 전 사전 조치 가능

---

## 💭 이 프로젝트를 통해 배운 것

### 🔧 **임베디드 시스템 개발 경험**
**"PC가 아닌 실제 하드웨어에서 동작하는 시스템"**

- **성능 제약 극복**: 제한된 자원에서 최적화하는 경험
- **하드웨어 제어**: GPIO를 통한 직접적인 하드웨어 조작
- **실시간 처리**: 영상 처리와 하드웨어 제어의 동기화

### 📋 **시장 조사의 중요성**
**"기술만으로는 충분하지 않다"**

- **현장의 소리**: 실제 사용자(운전기사)의 니즈 파악
- **기존 시스템 한계**: 왜 기존 제품들이 외면받는지 이해
- **실용성 우선**: 기술적 완성도보다 실제 활용도 중심 설계

### 🗺️ **데이터 분석과 시각화**
**"숫자 뒤에 숨은 이야기 찾기"**

- **R을 활용한 지리정보 시각화**: 교통사고 패턴 분석
- **공공데이터 활용**: 실제 정부 데이터를 활용한 인사이트 도출
- **현실 문제 해결**: 데이터 분석을 통한 실질적 개선안 제시

### 🌟 **제품 지향적 사고**
**"Demo가 아닌 Product 만들기"**

- **사용자 중심**: 기술적 가능성보다 사용자 편의성 우선
- **확장성 고려**: 실제 양산과 배포를 고려한 설계
- **지속가능성**: 유지보수와 업그레이드 가능한 구조

---

## 🔮 향후 발전 방향

### 🚀 **상용화 가능성**
- **버스 회사와의 파일럿 테스트**: 실제 노선에서 성능 검증
- **IoT 통합**: 차량 관제 시스템과의 연동
- **AI 학습 고도화**: 개인별 졸음 패턴 학습을 통한 정확도 향상

### 📊 **데이터 플랫폼 확장**
- **실시간 위험구간 정보**: 교통 상황 기반 동적 경고
- **예측 모델**: 날씨, 시간, 구간별 졸음 위험도 예측
- **통합 안전 솔루션**: 졸음운전 외 종합적 운행 안전 관리

---

## 📁 프로젝트 구조 및 실행

### 📂 **디렉토리 구조**
```
DrowsinessDetection/
├── src/
│   ├── main.py                    # 메인 실행 파일
│   ├── detection/
│   │   ├── eye_detector.py        # 눈 감김 감지
│   │   └── mouth_detector.py      # 하품 감지
│   ├── utils/
│   │   ├── database.py            # 데이터베이스 연동
│   │   ├── notification.py        # 텔레그램 알림
│   │   └── display.py             # 화면 표시
│   └── config/
│       └── settings.py            # 설정 파일
├── analysis/
│   ├── route_analysis_1.R         # 기본 노선 분석
│   ├── route_analysis_2.R         # Shapefile 처리
│   └── route_analysis_3.R         # 교통사고 분석
├── data/
│   ├── haarcascade_eye.xml        # 눈 검출 모델
│   └── haarcascade_frontalface_default.xml # 얼굴 검출 모델
└── requirements.txt               # 필요한 라이브러리
```

### 🚀 **설치 및 실행**
```bash
# 필수 라이브러리 설치
pip install -r requirements.txt

# 시스템 실행 (라즈베리파이에서)
python src/main.py

# 교통사고 데이터 분석 (R 환경에서)
Rscript analysis/route_analysis_1.R
```

### ⚠️ **주의사항**
- 라즈베리파이 5 이상 권장
- Google Maps API 키 필요 (교통사고 분석용)
- 텔레그램 봇 토큰 설정 필요

---

## 📊 프로젝트 자료 및 결과물

### 📚 **관련 자료**
- 📊 [발표자료](https://drive.google.com/file/d/1VvYZi_TLRJagFjTqcLyYLVFQfkftC0LB/view?usp=sharing): 전체 프로젝트 개요 및 결과
- 🎥 [시스템 구동 영상](https://drive.google.com/file/d/1kKJkofs_6sVcjkxZ52kIn9LiBUN8N8G9/view?usp=sharing): 실제 동작 모습
- 📊 [교통사고 데이터](https://drive.google.com/drive/folders/1Z_oWJ6AM-Q1QZdBMZnO8jVkCdGuHndzZ?usp=sharing): 분석에 사용된 원본 데이터

### 🛠 **개발 환경**
- **Hardware**: Raspberry Pi 5, Camera Module 3
- **OS**: Raspberry Pi OS
- **Language**: Python 3.9+, R 4.x
- **Database**: MySQL
- **Libraries**: OpenCV, Mediapipe, RPi.GPIO, Picamera2

---

## 📞 Contact (공동 작업자)

- **박동균**
- **Email**: ace062212@gmail.com
- **GitHub**: [ace062212](https://github.com/ace062212)

- **김재현**  
- **Email**: nicegame9510@gmail.com
- **GitHub**: [kimjaekim](https://github.com/kimjaekim)
---

*"라즈베리파이로 첫 임베디드 시스템을 개발하며, 기술이 현실에서 어떻게 작동하는지 배운 프로젝트"*

**🏆 소프트웨어 인재육성 캠프 은상 수상작 (2024)**  
**🔧 실제 산업 현장 적용을 고민한 IoT 시스템 개발 경험**
