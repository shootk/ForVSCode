from django.shortcuts import render
from django.http import HttpResponse
from .models import Message
# Create your views here.


def index(request):
    d = {
        'messages': Message.objects.all(),
    }
    return render(request, 'crud/index.html', d)


def add(request):
    return render(request, 'crud/edit.html', {})


def edit(request, editing_id):
    return render(request, 'crud/edit.html', {})


def delete(request):
    return HttpResponse('Delete')
