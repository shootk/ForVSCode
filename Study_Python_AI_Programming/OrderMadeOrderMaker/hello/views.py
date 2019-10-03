from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def hello_world(request):
    # ハローワールドするためのビュー関数：webリクエストを受け取ってレスポンスを返す
    return HttpResponse('Hello World!')
