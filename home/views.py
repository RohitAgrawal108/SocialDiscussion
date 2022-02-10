from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/home.html')

def chat(request):
    context={"1":1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    'h':1,
    }
    return render(request, 'Chat/ChatTemplate.html',context)
