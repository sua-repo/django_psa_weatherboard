from django.http import JsonResponse
from django.shortcuts import render
import requests

from config import settings

# Create your views here.


# dev_2
# dev_5
def index(request):
    context = {
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
def get_weather(request):
    x = request.GET.get("x")
    y = request.GET.get("y")

    endpoint = settings.KMA_SHORT_ENDPOINT
    key = settings.KMA_SHORT_KEY

    from datetime import datetime, timedelta

    now = datetime.now()
    now -= timedelta(minutes=now.minute % 30 + 10)
    base_date = now.strftime("%Y%m%d")
    base_time = now.strftime("%H%M")

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
        response = requests.get(endpoint, params=params)
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
