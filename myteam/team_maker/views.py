from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'team_maker/index.html')
