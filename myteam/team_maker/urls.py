from django.urls import path
from . import views

app_name = "team_maker"
urlpatterns = [
    path('team_maker/', views.index, name='index'),
]