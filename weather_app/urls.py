from django.urls import path
from . import views

urlpatterns= [
    path("",views.index, name="index"),
    path('get_ai_response', views.get_ai_response, name='get_ai_response'),
]