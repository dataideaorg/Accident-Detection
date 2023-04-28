from django.shortcuts import render

#  Create your views here.

def home(request):
    return render(request,'accidentdetection/home.html')

def about(request):
    return render(request,'accidentdetection/about.html')

def contact(request):
    return render(request,'accidentdetection/contact.html')
