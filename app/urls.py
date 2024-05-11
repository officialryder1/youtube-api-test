from django.urls import path, re_path
from .views import home, search, single_item

urlpatterns = [
    path('', home, name="home"),
    path('search/<str:name>/',search, name='search'),
    re_path('video/(?P<slug>[\w-]+)/',single_item, name='searched_video')
]