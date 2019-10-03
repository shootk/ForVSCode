from django.conf.urls import url
from . import views

urlpatterns = [
    # まずこのアプリケーションにURLディスパッチャを書いて、プロジェクトから呼び出す
    url(r'^$', views.hello_world, name='hello_world'),
]
