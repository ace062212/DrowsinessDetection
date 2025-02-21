# 🚗 라즈베리파이 기반 졸음운전 방지 시스템 및 노선 분석

## 프로젝트 개요
본 프로젝트는 버스 운전자의 졸음운전을 감지하고 예방하는 시스템을 개발하며, 고속도로 노선별 교통사고 데이터를 분석하여 안전한 운행 경로를 제시합니다.

## 기간 
- 2024. 09 
## 데이터 소스
프로젝트에서 사용된 데이터는 다음 링크에서 확인할 수 있습니다:
- [고속도로 노선별 교통사고 현황 데이터](https://drive.google.com/drive/folders/1Z_oWJ6AM-Q1QZdBMZnO8jVkCdGuHndzZ?usp=sharing)

## 프로젝트 구조

## 📋 프로젝트 개요
실시간 영상 처리와 딥러닝을 활용하여 운전자의 졸음 상태를 감지하고 경고하는 시스템입니다. 라즈베리파이 5와 카메라 모듈을 사용하여 운전자의 눈 감김과 하품을 실시간으로 감지하며, 위험 상황 발생 시 즉각적인 경고를 제공합니다.

## 📚 발표자료 링크
- 📊 [발표자료](https://drive.google.com/file/d/1VvYZi_TLRJagFjTqcLyYLVFQfkftC0LB/view?usp=sharing)
- 🎥 [시스템 구동 영상](https://drive.google.com/file/d/1kKJkofs_6sVcjkxZ52kIn9LiBUN8N8G9/view?usp=sharing)

## 🛠 주요 기능
1. **실시간 졸음 감지**
   - OpenCV와 Mediapipe를 활용한 눈 감김 감지
   - 하품 횟수 측정 및 분석
   - 30km/h 이상 주행 시 자동 활성화

2. **다중 경고 시스템**
   - 부저를 통한 청각적 경고
   - 화면 표시를 통한 시각적 경고
   - 텔레그램 메시지를 통한 원격 알림

3. **데이터 관리**
   - MySQL 데이터베이스 연동
   - 졸음 상태 기록 및 분석
   - 실시간 모니터링 데이터 저장

## 💻 개발 환경
- Hardware: Raspberry Pi 5
- OS: Raspberry Pi OS
- Language: Python 3.9+
- Camera: Raspberry Pi Camera Module 3
- Database: MySQL

### 사용 라이브러리
- OpenCV
- Mediapipe
- Pygame
- RPi.GPIO
- Picamera2
- SQLAlchemy
- Pandas
- PyMySQL

## 📊 시스템 구조
1. **하드웨어 구성**
   - Raspberry Pi 5
   - Camera Module 3
   - 부저 모듈
   - GPIO 연결

2. **소프트웨어 구성**
   - 실시간 영상 처리 모듈
   - 졸음 감지 알고리즘
   - 데이터베이스 관리 시스템
   - 알림 시스템

### 1. 기본 노선 데이터 처리 (route_analysis_1.R)
- 목적: 고속도로 노선별 기초 데이터 처리 및 시각화
- 주요 기능:
  - 노선별 위치 데이터 지오코딩
  - 출발지-도착지 경로 매핑
  - Google Maps API를 활용한 경로 시각화
- 사용 예시:

노선 데이터 로드 및 처리
data <- load_accident_data("path/to/data.csv")
routes <- calculate_routes(data)
visualize_routes(routes)


### 2. 고속도로 Shapefile 처리 (route_analysis_2.R)
- 목적: 고속도로 공간 데이터 처리 및 분석
- 주요 기능:
  - Shapefile 데이터 로드 및 필터링
  - 좌표계 변환 및 데이터 정제
  - 고속도로 노선도 시각화
- 사용 예시:

Shapefile 데이터 처리
highway_data <- load_shapefile("path/to/shapefile.shp")
filtered_data <- filter_highways(highway_data)
plot_highways(filtered_data)


### 3. 교통사고 데이터 분석 (route_analysis_3.R)
- 목적: 노선별 교통사고 현황 분석 및 위험구간 식별
- 주요 기능:
  - 교통사고 데이터 시각화
  - 사고 다발 구간 분석
  - 노선 교차점 분석
- 시각화 옵션:
  - 사고 건수 히트맵
  - 사망자 수 분포도
  - 부상자 수 분포도
- 사용 예시:
교통사고 데이터 분석
accident_data <- sort_accident_data(data)
visualize_accident_data(map, accident_data, "fatalities")
analyze_intersections(route_data, accident_data)

### 분석 코드 실행 환경
- R version: 4.x.x
- 필수 패키지:
  - sf
  - ggmap
  - dplyr
  - tidyr
  - viridis
  - stplanr

### 주의사항
- Google Maps API 키 필요
- 대용량 Shapefile 처리 시 충분한 메모리 필요

## 👥 개발자 정보
- GitHub: https://github.com/ace062212
- 이메일: ace062212@gmail.com


## 📜 라이센스
This project is licensed under the MIT License
