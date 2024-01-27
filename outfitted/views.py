"""
This file is used to handle requests and return responses. Each view function takes a request object and returns a response object.
"""

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def test(request):
    return HttpResponse("Hello, World!")