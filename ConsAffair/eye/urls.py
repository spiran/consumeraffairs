from django.urls import path
from . import views

app_name = 'eye'

urlpatterns = [
    path('collector', views.collector, name='collector'),
    path('event', views.getSession, name='event'),
    path('category-events', views.catEvents, name='category-events'),
    path('range-events', views.timeRangeEvents, name='range-events'),
    path('invalid-time', views.invalidTimestamp, name='invalid-time'),
]