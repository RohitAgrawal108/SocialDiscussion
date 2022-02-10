from django.urls import path, include
from chat.views import ThreadView
from . import views

urlpatterns = [
    path('', views.template_view,name="template"),
    path('<str:username>/', ThreadView.as_view()),
]