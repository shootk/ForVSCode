from django.shortcuts import render
from django.http.response import HttpResponse
from datetime import datetime
from . import forms, models
from django.shortcuts import redirect

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


def hello_get_query(request):
    d = {
        'your_name': request.GET.get('your_name', default='xxx')
    }
    return render(request, 'get_query.html', d)


def hello_forms(request):
    form = forms.HelloForm(request.GET or None)
    if form.is_valid():
        message = 'データ検証に成功しました'
    else:
        message = 'データ検証に失敗しました'

    d = {'form': form,
         'message': message, }
    return render(request, 'forms.html', d)


def hello_forms2(request):
    d = {
        'form': forms.SampleForm(),
    }
    return render(request, 'forms_samples.html', d)


def hello_models(request):
    form = forms.HelloForm(request.POST or None)
    if form.is_valid():
        models.Hello.objects.create(**form.cleaned_data)
        return redirect('hello:hello_models')
    d = {
        'form': form,
        'hello_qs': models.Hello.objects.all().order_by('-id')
    }
    return render(request, 'models.html', d)
