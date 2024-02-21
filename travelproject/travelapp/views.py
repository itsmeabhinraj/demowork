from django.shortcuts import render
from .models import pplaces
# Create your views here.
def demo(request):
    obj=pplaces.objects.all()
    return render(request,"index.html",{'result':obj})

def demo1(request):
    return render(request,"result.html")


def page1(request):
    return render(request,'contact.html')
def page2(request):
    return render(request,'destinations.html')
def page3(request):
    return render(request,'index.html')
def page4(request):
    return render(request,'elements.html')
def page5(request):
    return render(request,'news.html')