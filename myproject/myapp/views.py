from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def sample_view(request):
    return HttpResponse("Hello, this is a sample view!")
def add(request):
    a = request.GET.get("a",13)
    b = request.GET.get("b",13)
    result = a+b
    return HttpResponse(f"sum of a and b = {result} view")

