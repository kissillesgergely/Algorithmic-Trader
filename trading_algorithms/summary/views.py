from django.shortcuts import render
from .models import Trade

def summary(request):
    return render(request, 'summary/summary.html')
