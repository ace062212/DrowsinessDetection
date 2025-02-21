# analysis/route_analysis_2.R

# 필요한 라이브러리 설치 및 로드
required_packages <- c("sf", "dplyr", "ggmap", "stringr", "tidyr")

for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

# Google Maps API 키 설정
register_google(key='YOUR_API_KEY')

# 1. Shapefile 데이터 로드 함수
load_shapefile <- function(file_path) {
  shapefile_data <- st_read(file_path, options = "ENCODING=EUC-KR")
  return(shapefile_data)
}

# 2. 고속도로 데이터 필터링 함수
filter_highways <- function(data) {
  filtered <- data %>%
    filter(grepl("고속도로", ROAD_NAME)) %>%
    select(ROAD_NAME, geometry) %>%
    mutate(ROAD_NAME = str_replace_all(ROAD_NAME, "고속도로", ""))
  return(filtered)
}

# 3. 좌표계 변환 함수
transform_coordinates <- function(data) {
  transformed <- st_transform(data, crs = 4326)
  return(transformed)
}

# 4. 교통사고 데이터 로드 함수
load_accident_data <- function(file_path) {
  data <- read.csv(file_path, header = TRUE, fileEncoding = "CP949")
  return(data)
}

# 5. 데이터 병합 및 정제 함수
merge_and_clean_data <- function(highway_data, accident_data) {
  merged <- highway_data %>%
    left_join(accident_data, by = "ROAD_NAME")
  
  # NA 값 처리
  cleaned <- merged %>%
    select(where(~ !all(is.na(.)))) %>%
    na.omit()
  
  return(cleaned)
}

# 6. 지도 시각화 함수
visualize_highways <- function(data) {
  map <- get_map(location = "south korea", zoom = 7, maptype = "roadmap")
  
  plot <- ggmap(map) +
    geom_sf(data = data, 
            aes(geometry = geometry), 
            color = "blue", 
            size = 1, 
            inherit.aes = FALSE) +
    labs(title = "Highways in South Korea") +
    theme_minimal()
  
  return(plot)
}

# 7. GeoJSON 저장 및 로드 함수
save_load_geojson <- function(data, file_path = NULL, mode = "save") {
  if(mode == "save") {
    st_write(data, file_path, delete_layer = TRUE)
  } else {
    data <- st_read(file_path)
    return(data)
  }
}

# 메인 실행 코드
main <- function() {
  # 1. Shapefile 데이터 로드
  shapefile_data <- load_shapefile("path/to/your/shapefile.shp")
  
  # 2. 고속도로 데이터 필터링
  filtered_data <- filter_highways(shapefile_data)
  
  # 3. 좌표계 변환
  transformed_data <- transform_coordinates(filtered_data)
  
  # 4. 교통사고 데이터 로드
  accident_data <- load_accident_data("path/to/your/accident_data.csv")
  
  # 5. 데이터 병합 및 정제
  final_data <- merge_and_clean_data(transformed_data, accident_data)
  
  # 6. 결과 시각화
  plot <- visualize_highways(final_data)
  print(plot)
  
  # 7. 결과 저장 (선택사항)
  save_load_geojson(final_data, "data/analysis/highways.geojson", "save")
}

# 스크립트 실행
if (!interactive()) {
  main()
}