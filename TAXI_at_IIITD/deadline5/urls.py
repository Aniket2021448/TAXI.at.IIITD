from django.contrib import admin
from django.urls import path
from deadline5 import views

urlpatterns = [
    path ('', views.index, name = 'deadline5'),
    path('index.html', views.index, name = 'home'),
    path('query1.html', views.query1, name = 'query1'),
    path('query2.html', views.query2, name = 'query2'),
    path('aboutUs.html', views.about, name = 'about'),
    path('contactUs.html', views.contact, name = 'contact'),
    path('trigger1.html', views.trigger1, name = 'trigger1'),
    path('trigger2.html', views.trigger2, name = 'trigger2'),
    path('checkTrigger1.html', views.checkTrigger1, name = 'checkT1'),
    path('checkTrigger2.html', views.checkTrigger2, name ='checkT2')

]