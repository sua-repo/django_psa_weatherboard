from django.http import JsonResponse
from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from config import settings

from requests.adapters import HTTPAdapter
import ssl

# Create your views here.


# dev_2
# dev_5
def index(request):
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "naver_client_id": settings.NAVER_API_CLIENT_ID,
        "naver_client_secret": settings.NAVER_API_CLIENT_SECRET,
        "kma_short_endpoint": settings.KMA_SHORT_ENDPOINT,
        "kma_short_key": settings.KMA_SHORT_KEY,
        "kma_mid_endpoint": settings.KMA_MID_ENDPOINT,
        "kma_mid_key": settings.KMA_MID_KEY,
    }
    return render(request, "main/index.html", context)


# dev_5
def get_address(request):
    # request.GET
    # {
    #     'lat': '37.5',
    #     'lon': '127.1'
    # }
    #
    #  request.GET 결과인 딕셔너리처럼 생긴 객체에 원하는 키에 해당하는 값을 가져오는 메서드 사용 get("key")

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    url = f"https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

    params = {
        "coords": f"{lon},{lat}",  # f"{lon},{lat}"에 공백 없어야 함
        "orders": "legalcode",
        "output": "json",
    }

    headers = {
        "X-NCP-APIGW-API-KEY-ID": settings.NAVER_API_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": settings.NAVER_API_CLIENT_SECRET,
    }

    response = requests.get(
        url, headers=headers, params=params
    )  # request 아님 / Python 라이브러리
    data = response.json()
    return JsonResponse(data)


# dev_5
# dev_20
# TLS 설정을 낮춘 커스텀 어댑터 정의
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")  # 핵심: TLS 보안 수준 낮춤
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


def get_base_time(now):
    base = now - timedelta(minutes=40)  # 발표 완료 기준 보정

    hour = base.hour
    if hour < 2:
        hour = 23
        base -= timedelta(days=1)
    else:
        # 발표 시각 목록 중 가장 가까운 이전 시각
        hour = max(h for h in [2, 5, 8, 11, 14, 17, 20, 23] if h <= hour)

    base_date = base.strftime("%Y%m%d")
    base_time = f"{hour:02}00"

    return base_date, base_time


def get_weather(request):

    print("📡 요청 방식:", request.method)
    print("📦 요청 GET:", request.GET)

    x = request.GET.get("x")
    y = request.GET.get("y")

    endpoint = settings.KMA_SHORT_ENDPOINT
    key = settings.KMA_SHORT_KEY  # 디코딩된 원본 키

    now = datetime.now()
    base_date, base_time = get_base_time(now)

    params = {
        "serviceKey": key,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": x,
        "ny": y,
    }

    try:
        # 여기부터 TLS 강제 설정된 세션으로 요청
        session = requests.Session()
        session.mount("https://", TLSAdapter())  # TLS 보안 설정 덮어쓰기

        response = session.get(endpoint, params=params, timeout=(3, 10))

        print("🔑 최종 요청 URL:", response.url)
        print("🧾 응답 상태 코드:", response.status_code)
        print("📦 응답 본문 (텍스트):", response.text[:500])

        data = response.json()

        if data["response"]["header"]["resultCode"] != "00":
            return JsonResponse({"error": "기상청 데이터가 없습니다."}, status=404)

        body = data["response"].get("body")
        if not body:
            return JsonResponse({"error": "body가 비어 있습니다."}, status=404)

        items = body["items"]["item"]
        print("📍 날씨 아이템 개수:", len(items))

        if not items:
            return JsonResponse({"error": "예보 아이템이 없습니다."}, status=404)

        from collections import defaultdict

        grouped = defaultdict(dict)
        for item in items:
            if item["category"] in ["TMP", "SKY", "POP"]:
                grouped[item["fcstTime"]][item["category"]] = item["fcstValue"]

        now_hour = int(now.strftime("%H"))
        result = []

        for time, data in sorted(grouped.items()):
            hour = int(time[:2])

            # 시간 제한을 없애고 전체 다 가져오기
            temp = f"{data.get('TMP')}°C"
            sky = data.get("SKY", "1")
            pop = int(data.get("POP", 0))

            if pop >= 30:
                icon = "🌧️"
            else:
                icon = {"1": "☀️", "3": "🌤️", "4": "☁️"}.get(sky, "☀️")

            result.append({"hour": f"{hour}시", "temp": temp, "icon": icon})

        return JsonResponse({"weather": result})

    except Exception as e:
        print("❌ 예외 발생:", e)
        return JsonResponse({"error": str(e)}, status=500)
