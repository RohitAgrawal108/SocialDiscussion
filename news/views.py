from django.shortcuts import render
import requests

API_KEY = 'fce045e4640c4b8c9876634793c5d0b6'
contry = 'in'

# Create your views here.

def index(request):

    url = f'https://newsapi.org/v2/top-headlines?country={contry}&apiKey={API_KEY}'
    responce = requests.get(url)
    data = responce.json()
    articales = data['articles']
    context = {
        'articles' : articales
    }


    return render(request, "news/index.html" ,context)