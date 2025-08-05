// static/js/index.js

import { convertToGrid } from "./utils/convertToGrid.js";
import { getWeatherForecast } from "./utils/weather.js";

const now = new Date();
const daysOfWeek = ["일", "월", "화", "수", "목", "금", "토"];
const today = now.getDay();
const days = Array.from({ length: 6 }, (_, i) => daysOfWeek[(today + i + 1) % 7]);

let startIndex = 0;
const visibleCount = 6;
const container = document.getElementById("weather-cards");
const btnPrev = document.getElementById("btn-prev");
const btnNext = document.getElementById("btn-next");
let weatherData = [];

function renderCards() {
  container.innerHTML = "";
  const sliced = weatherData.slice(startIndex, startIndex + visibleCount);
  sliced.forEach(item => {
    const card = document.createElement("div");
    card.className = "text-center border rounded shadow-sm p-4 bg-light";
    card.style.minWidth = "120px";
    card.style.height = "140px";
    card.innerHTML = `
      <div style="font-size: 32px;">${item.icon}</div>
      <div style="font-size: 18px;">${item.temp}</div>
      <div style="font-size: 16px;">${item.hour}</div>
    `;
    container.appendChild(card);
  });
}

btnPrev.addEventListener("click", () => {
  if (startIndex > 0) {
    startIndex -= visibleCount;
    renderCards();
  }
});

btnNext.addEventListener("click", () => {
  if (startIndex + visibleCount < weatherData.length) {
    startIndex += visibleCount;
    renderCards();
  }
});

function renderDailySummary(midForecast) {
  const container = document.getElementById("daily-summary");
  container.innerHTML = "";

  const today = new Date();
  const days = Array.from({ length: 6 }, (_, i) => {
    const date = new Date(today);
    date.setDate(today.getDate() + i + 1);
    const dayName = daysOfWeek[date.getDay()];
    return dayName;
  });


  days.forEach((day, i) => {
    const minKey = `taMin${i + 3}`;
    const maxKey = `taMax${i + 3}`;
    const min = midForecast[minKey] ?? "-";
    const max = midForecast[maxKey] ?? "-";

    const div = document.createElement("div");
    div.className = "border rounded p-3 text-center";
    div.style.width = "140px";
    div.innerHTML = `
      <div style="font-weight: bold;">${day}요일</div>
      <div style="font-size: 24px;">🌤️</div>
      <div>최고 ${max}°C</div>
      <div>최저 ${min}°C</div>
    `;
    container.appendChild(div);
  });
}

function extractHourNumber(hourString) {
  const match = hourString.match(/^(\d{1,2})시$/);
  if (!match) return null;
  return parseInt(match[1], 10);
}

function handleWeatherResult(result) {

  const shortData = result.short;
  const midData = result.mid;

  if (!midData) {
    console.warn("❗중기예보 데이터가 없습니다.");
    return;
  }

  // 시간별 처리
  const now = new Date();
  const currentHour = now.getHours();

  const future = shortData.filter(item => {
    const hourNum = extractHourNumber(item.hour);
    return hourNum !== null && hourNum >= currentHour;
  });

  const past = shortData.filter(item => {
    const hourNum = extractHourNumber(item.hour);
    return hourNum !== null && hourNum < currentHour;
  });

  weatherData = [...future, ...past];
  renderCards();
  renderDailySummary(midData);
}

function initAutocomplete() {
  const input = document.getElementById("location-search");
  input.addEventListener("click", () => {
    input.removeAttribute("readonly");
    input.focus();
    const keyboardEvent = new KeyboardEvent("keydown", { key: " " });
    input.dispatchEvent(keyboardEvent);
  });

  const autocomplete = new google.maps.places.Autocomplete(input, {
    fields: ["geometry", "name"],
    componentRestrictions: { country: "kr" }
  });

  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    if (!place || !place.geometry) {
      alert("장소를 찾을 수 없습니다.");
      return;
    }

    const lat = place.geometry.location.lat();
    const lon = place.geometry.location.lng();
    const name = place.name;

    document.querySelector("h4").textContent = `${name} 날씨`;

    const { x, y } = convertToGrid(lat, lon);
    getWeatherForecast(x, y, handleWeatherResult);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  navigator.geolocation.getCurrentPosition(
    function(position) {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      fetch(`/get-address?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
          if (data.results && data.results.length > 0) {
            const dong = data.results[0].region.area3.name;
            document.querySelector("h4").textContent = `${dong} 날씨`;
          }
        });

      const { x, y } = convertToGrid(lat, lon);
      getWeatherForecast(x, y, handleWeatherResult);
    },
    function(error) {
      console.error("위치 정보를 가져올 수 없습니다.", error);
    }
  );
});

window.initAutocomplete = initAutocomplete;
