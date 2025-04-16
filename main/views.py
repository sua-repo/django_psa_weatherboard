from django.shortcuts import render

# Create your views here.


# dev_2
# dev_5
def index(request):
    hours = ["9", "10", "11", "12", "13", "14"]
    days = ["금", "토", "일", "월", "화", "수"]

    context = {
        "hours": hours,
        "days": days,
    }
    return render(request, "main/index.html", context)
