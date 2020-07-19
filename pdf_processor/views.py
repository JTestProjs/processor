from django.shortcuts import render
from django.http import HttpResponse
import json
import os

def processor(request): 
    pass

def index(request):
    return render(request, 'pdf_processor/template.html', {})