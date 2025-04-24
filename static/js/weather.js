// 미완성
export async function getWeatherForecast(x, y, shortEndpoint, shortKey, midEndpoint, midKey) {
    const now = new Date();
    const baseDate = now.toISOString().slice(0, 10).replace(/-/g, "");
  
    // 초단기예보 기준시간 계산 (10분 여유)
    const shortNow = new Date(now);
    shortNow.setMinutes(shortNow.getMinutes() - (shortNow.getMinutes() % 30) - 10);
    const shortBaseTime = `${String(shortNow.getHours()).padStart(2, "0")}${String(shortNow.getMinutes()).padStart(2, "0")}`;
  
    // 단기예보 기준시간 계산 (30분 여유)
    const midNow = new Date(now);
    midNow.setHours(midNow.getHours() - (midNow.getMinutes() < 30 ? 1 : 0));
    midNow.setMinutes(0);
    const midBaseTime = `${String(midNow.getHours()).padStart(2, "0")}00`;
  
    const shortParams = new URLSearchParams({
      serviceKey: shortKey,
      pageNo: "1",
      numOfRows: "1000",
      dataType: "JSON",
      base_date: baseDate,
      base_time: shortBaseTime,
      nx: x,
      ny: y,
    });
  
    const midParams = new URLSearchParams({
      serviceKey: midKey,
      pageNo: "1",
      numOfRows: "1000",
      dataType: "JSON",
      base_date: baseDate,
      base_time: midBaseTime,
      nx: x,
      ny: y,
    });
  
    try {
      const [shortRes, midRes] = await Promise.all([
        fetch(`${shortEndpoint}?${shortParams}`),
        fetch(`${midEndpoint}?${midParams}`),
      ]);
  
      const shortData = await shortRes.json();
      const midData = await midRes.json();
  
      console.log("초단기예보:", shortData);
      console.log("단기예보:", midData);
  
      // TODO: 두 데이터 조합하여 현재시간 +1~+6, +9, +12 시간 날씨 구성하기
  
    } catch (err) {
      console.error("날씨 정보 가져오기 실패", err);
    }
  }
  