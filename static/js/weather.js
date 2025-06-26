// static/js/weather.js

// dev_20 
export async function getWeatherForecast(x, y, shortUrl, shortKey, midUrl, midKey, onSuccess) {
  try {
    const response = await fetch(`/get-weather/?x=${x}&y=${y}`);
    const data = await response.json();

    if (data.weather) {
      // 콜백 함수가 주어졌다면 결과를 전달
      if (typeof onSuccess === "function") {
        onSuccess(data.weather);
      }
    } 
    else {
      console.warn("날씨 데이터가 없습니다.");
    }
  } 
  
  catch (error) {
    console.error("날씨 데이터를 불러오는 데 실패했습니다:", error);
  }
}