import json
import ssl
from collections import defaultdict
from datetime import datetime, timedelta
from time import sleep

import requests
from django.http import JsonResponse
from django.shortcuts import render
from requests.adapters import HTTPAdapter

from config import settings

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


# 중기예보 발표 시각 기준 함수 (06시/18시 기준)
def get_mid_tmFc(now):
    base_time = now.replace(minute=0, second=0, microsecond=0)
    if now.hour < 6:
        base_time = base_time - timedelta(days=1)
        base_time = base_time.replace(hour=18)
    elif now.hour < 18:
        base_time = base_time.replace(hour=6)
    else:
        base_time = base_time.replace(hour=18)
    return base_time.strftime("%Y%m%d%H00")


def get_weather(request):
    print("📡 [get_weather] 요청 방식:", request.method)
    print("📦 [get_weather] 요청 파라미터:", request.GET)

    x = request.GET.get("x")
    y = request.GET.get("y")
    now = datetime.now()

    base_date, base_time = get_base_time(now)

    # -----------------------------
    # 1. 단기예보
    # -----------------------------
    short_result = []
    try:
        print("🔍 [단기예보] 요청 준비 중...")
        short_endpoint = settings.KMA_SHORT_ENDPOINT
        short_key = settings.KMA_SHORT_KEY

        short_params = {
            "serviceKey": short_key,
            "pageNo": 1,
            "numOfRows": 1000,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": x,
            "ny": y,
        }

        short_session = requests.Session()
        short_session.mount("https://", TLSAdapter())
        short_response = short_session.get(
            short_endpoint, params=short_params, timeout=(5, 15)
        )

        print("🌐 [단기예보] 요청 URL:", short_response.url)

        short_data = short_response.json()
        if short_data["response"]["header"]["resultCode"] != "00":
            print("⚠️ [단기예보] 결과 코드가 00이 아님")
            return JsonResponse({"error": "단기예보 데이터가 없습니다."}, status=404)

        short_items = short_data["response"]["body"]["items"]["item"]
        print("📍 [단기예보] 아이템 개수:", len(short_items))

        grouped = defaultdict(dict)
        for item in short_items:
            if item["category"] in ["TMP", "SKY", "POP"]:
                grouped[item["fcstTime"]][item["category"]] = item["fcstValue"]

        for time, data in sorted(grouped.items()):
            hour = int(time[:2])
            temp = f"{data.get('TMP')}°C"
            sky = data.get("SKY", "1")
            pop = int(data.get("POP", 0))

            icon = "🌧️" if pop >= 30 else {"1": "☀️", "3": "🌤️", "4": "☁️"}.get(sky, "☀️")
            short_result.append({"hour": f"{hour}시", "temp": temp, "icon": icon})

        print("✅ [단기예보] 처리 완료")

    except Exception as e:
        print("❌ [단기예보] 예외 발생:", e)
        return JsonResponse({"error": f"단기예보 오류: {str(e)}"}, status=500)

    # -----------------------------
    # 2. 중기예보
    # -----------------------------
    mid_result = {}
    try:
        print("🔍 [중기예보] 요청 준비 중...")
        region_id = "11H20201"
        mid_key = settings.KMA_MID_KEY
        mid_endpoint = settings.KMA_MID_ENDPOINT + "/getMidTa"
        tmFc = get_mid_tmFc(now)

        mid_params = {
            "serviceKey": mid_key,
            "pageNo": 1,
            "numOfRows": 1000,
            "dataType": "JSON",
            "regId": region_id,
            "tmFc": tmFc,
        }

        for attempt in range(3):
            try:
                mid_session = requests.Session()
                mid_session.mount("https://", TLSAdapter())
                mid_response = mid_session.get(
                    mid_endpoint, params=mid_params, timeout=(5, 15)
                )

                print("🌐 [중기예보] 요청 URL:", mid_response.url)

                if not mid_response.text.strip():
                    raise ValueError("중기예보 응답이 비어 있음")

                mid_data = mid_response.json()

                result_code = mid_data["response"]["header"]["resultCode"]
                result_msg = mid_data["response"]["header"].get("resultMsg", "")
                print("📋 [중기예보] 결과 코드:", result_code)
                print("📋 [중기예보] 결과 메시지:", result_msg)

                if result_code != "00":
                    print("⚠️ [중기예보] 결과 코드가 00이 아님")
                    mid_result = {}
                    break  # ❗ 반드시 break
                else:
                    mid_items = mid_data["response"]["body"]["items"]["item"]
                    if not mid_items:
                        raise ValueError("중기예보 항목이 비어 있음")
                    mid = mid_items[0]
                    mid_result = {
                        f"taMin{i}": mid.get(f"taMin{i}") for i in range(3, 9)
                    }
                    mid_result.update(
                        {f"taMax{i}": mid.get(f"taMax{i}") for i in range(3, 9)}
                    )

                    print("✅ [중기예보] 처리 완료")
                    break  # 성공했으니 반복 종료

            except (
                requests.exceptions.Timeout,
                requests.exceptions.RequestException,
            ) as e:
                print(f"⏳ [중기예보] {attempt+1}회차 요청 실패:", e)
                sleep(1)

        else:
            print("❌ [중기예보] 3회 시도 실패. 빈 값으로 반환")
            mid_result = {}

    except Exception as e:
        print("❌ [중기예보] 예외 발생:", e)
        mid_result = {}

    # -----------------------------
    # 3. 최종 응답
    # -----------------------------
    print("📤 [get_weather] 최종 응답 반환")
    return JsonResponse(
        {
            "weather": {
                "short": short_result,
                "mid": mid_result,
            }
        }
    )
