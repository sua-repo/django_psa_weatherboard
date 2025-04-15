from django.shortcuts import render

# Create your views here.


# dev_3
def rsp(request):
    return render(request, "game/rsp.html")
