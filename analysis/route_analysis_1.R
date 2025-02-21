# analysis/route_analysis_1.R

# 필요한 라이브러리 설치 및 로드
required_packages <- c("ggmap", "jsonlite", "stplanr", "sf", "ggplot2", "tmap", 
                      "googlePolylines", "httr", "dplyr", "mapdeck")

# 패키지 설치 확인 및 설치
for(pkg in required_packages) {
  if(!require(pkg, character.only = TRUE)) {
    install.packages(pkg)
    library(pkg, character.only = TRUE)
  }
}

# Google Maps API 키 설정
register_google(key='YOUR_API_KEY')

# 1. 데이터 로드 함수
load_accident_data <- function(file_path) {
  data <- read.csv(file_path, header = TRUE, fileEncoding = "CP949")
  return(data)
}

# 2. 지오코딩 함수
get_coordinates <- function(address) {
  result <- tryCatch({
    geocode(address, output = "latlon", source = "google")
  }, error = function(e) {
    return(NULL)
  })
  
  if (is.null(result) || is.na(result$lat) || is.na(result$lon)) {
    return(c(NA, NA))
  } else {
    return(c(result$lat, result$lon))
  }
}

# 3. 좌표 추가 함수
get_location_coordinates <- function(df, address_col) {
  coordinates <- t(sapply(df[[address_col]], get_coordinates))
  if (ncol(coordinates) < 2) {
    stop("좌표 데이터가 올바르게 생성되지 않았습니다.")
  }
  df[[paste0(address_col, "_위도")]] <- coordinates[, 1]
  df[[paste0(address_col, "_경도")]] <- coordinates[, 2]
  return(df)
}

# 4. 경로 시각화 함수
visualize_routes <- function(data, map_center = "south korea", zoom = 7) {
  map <- get_googlemap(center = map_center,
                      maptype = "roadmap",
                      zoom = zoom,
                      size = c(640, 640))
  
  ggmap(map) +
    geom_path(data = data, aes(x = X, y = Y, color = 출발지, group = L1), 
              size = 1) +
    labs(title = "출발지와 목적지 간의 경로",
         x = "경도",
         y = "위도")
}

# 메인 실행 코드
main <- function() {
  # 1. 데이터 로드
  accident_data <- load_accident_data("path/to/your/data.csv")
  
  # 2. 테스트 데이터 생성
  highway_test <- accident_data %>% head(1)
  
  # 3. 좌표 추가
  highway_test <- get_location_coordinates(highway_test, "시점")
  highway_test <- get_location_coordinates(highway_test, "종점")
  
  # 4. 경로 계산 및 시각화
  routes_list <- calculate_routes(highway_test)
  all_routes_df <- do.call(rbind, routes_list)
  
  # 5. 결과 시각화
  plot <- visualize_routes(all_routes_df)
  print(plot)
  
  # 6. 결과 저장
  write.csv(all_routes_df, "data/analysis/route_data.csv", row.names = FALSE)
}

# 스크립트 실행
if (!interactive()) {
  main()
}