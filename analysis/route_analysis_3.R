# analysis/route_analysis_3.R

# 필요한 라이브러리 설치 및 로드
required_packages <- c("sf", "dplyr", "ggmap", "ggplot2", "viridis")

for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

# Google Maps API 키 설정
register_google(key='YOUR_API_KEY')

# 1. 데이터 정렬 함수
sort_accident_data <- function(data) {
  sorted <- data %>%
    arrange(desc(accidents))
  return(sorted)
}

# 2. 좌표계 변환 함수
transform_coordinates <- function(data) {
  transformed <- st_transform(data, crs = 4326)
  return(transformed)
}

# 3. 사고 데이터 시각화 함수
visualize_accident_data <- function(map, data, metric = "accidents") {
  plot <- ggmap(map) +
    geom_sf(data = data, aes(color = !!sym(metric)), size = 1, inherit.aes = FALSE) +
    scale_color_continuous(
      trans = 'log',
      low = "gray",
      high = "red",
      name = paste0(toupper(substr(metric, 1, 1)), substr(metric, 2, nchar(metric)), " (Log Scale)")
    ) +
    labs(
      title = "Highways and Accident Data",
      color = paste0(toupper(substr(metric, 1, 1)), substr(metric, 2, nchar(metric)), " (Log Scale)")
    ) +
    theme_minimal()
  
  return(plot)
}

# 4. 주요 도로 필터링 함수
filter_major_roads <- function(data) {
  road_names <- c("경부", "영동", "서해안", "중앙", "중부", "중부내륙", 
                 "호남", "서울양양", "제2경인", "남해")
  
  filtered <- data %>%
    filter(ROAD_NAME %in% road_names)
  
  return(filtered)
}

# 5. 복합 시각화 함수
visualize_combined_data <- function(map, route_data, accident_data) {
  plot <- ggmap(map) +
    geom_path(data = route_data, 
              aes(x = X, y = Y, group = L1), 
              size = 1, 
              color = "blue") +
    geom_sf(data = accident_data, 
            aes(color = fatalities), 
            size = 1, 
            inherit.aes = FALSE) +
    scale_color_gradient(low = "gray", high = "red") +
    labs(
      title = "Combined Route and Accident Data",
      color = "Accidents",
      x = "경도",
      y = "위도"
    ) +
    theme_minimal()
  
  return(plot)
}

# 6. 교차점 분석 함수
analyze_intersections <- function(route_data, accident_data) {
  # 경로 데이터를 sf 객체로 변환
  route_sf <- st_as_sf(route_data, coords = c("X", "Y"), crs = 4326, remove = FALSE)
  
  # 교차점 계산
  intersections <- st_intersection(route_sf, accident_data)
  intersections_length <- st_length(intersections)
  
  return(list(
    intersections = intersections,
    lengths = intersections_length
  ))
}

# 메인 실행 코드
main <- function() {
  # 1. Shapefile 데이터 로드
  shapefile_data <- st_read("path/to/your/shapefile.shp", 
                           options = "ENCODING=EUC-KR")
  
  # 2. 데이터 정렬 및 변환
  sorted_data <- sort_accident_data(shapefile_data)
  transformed_data <- transform_coordinates(sorted_data)
  
  # 3. 주요 도로 필터링
  filtered_data <- filter_major_roads(transformed_data)
  
  # 4. 지도 준비
  map <- get_googlemap(center = "south korea",
                      maptype = "roadmap",
                      zoom = 7,
                      size = c(640, 640))
  
  # 5. 시각화
  accident_plot <- visualize_accident_data(map, filtered_data)
  print(accident_plot)
  
  # 6. 충남고속 데이터 로드 및 복합 시각화
  chungnam_data <- read.csv("path/to/your/chungnam_data.csv", header = TRUE)
  combined_plot <- visualize_combined_data(map, chungnam_data, filtered_data)
  print(combined_plot)
  
  # 7. 교차점 분석
  intersection_results <- analyze_intersections(chungnam_data, filtered_data)
  print(intersection_results)
}

# 스크립트 실행
if (!interactive()) {
  main()
}