from . import views
from django.urls import path

urlpatterns = [
    path('',views.demo,name='demo'),
    path('result',views.demo1,name='demo1'),
    path('contact',views.page1,name='contact'),
    path('destinations',views.page2,name='destinations'),
    path('home1',views.page3,name='home1'),
    path('elements',views.page4,name='elements'),
    path('news',views.page5,name='news'),

]