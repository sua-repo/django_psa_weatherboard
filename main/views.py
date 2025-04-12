from django.shortcuts import render

# Create your views here.

# dev_2
def index(request):
    return render(request, 'main/index.html')

