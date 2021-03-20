from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    context = {
        "title":"Film Finder"
    }
    return render(request, "search.html", context)