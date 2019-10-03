from django.shortcuts import render
from django.http.response import HttpResponse
from datetime import datetime

# Create your views here.


def hello_world(request):
    return HttpResponse('Hello World!')
# ハローワールドするためのビュー関数：webリクエストを受け取ってレスポンスを返す


def hello_template(request):
    d = {'hour': datetime.now().hour, 'message': 'Sample message', }
    return render(request, 'index.html', d)


def hello_if(request):
    d = {'is_visible': True, 'empty_str': '3', }
    return render(request, 'if.html', d)


def hello_for(request):
    d = {
        'objects': range(10),
    }
    return render(request, 'for.html', d)
