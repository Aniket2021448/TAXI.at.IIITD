from django.contrib import admin
from django.urls import path, include
from deadline5 import views

from . import views


urlpatterns = [
    
    path('', views.index, name = 'deadline5'),
    path('index.html', views.index, name = 'home'),
    path('query1.html', views.query1, name = 'query1'),
    path('query2.html', views.query2, name = 'query2'),
    path('aboutUs.html', views.about, name = 'about'),
    path('contactUs.html', views.contact, name = 'contact'),
    path('trigger1.html', views.trigger1, name = 'trigger1'),
    path('trigger2.html', views.trigger2, name = 'trigger2'),
    path('checkTrigger1.html', views.checkTrigger1, name = 'checkT1'),
    path('checkTrigger2.html', views.checkTrigger2, name ='checkT2'),
    path('passenger_signup.html/', views.passengerSignup, name ='Psignup'),

    path('passenger_login.html', views.passengerSignup, name = 'savePassenger'),
    # path('passengerUI.html', views.passengerUI, name = 'loggedPassenger'),

    path('passenger_login.html/', views.passengerLogin, name ="Plogin"),
    path('passenger_login.html/', views.passengerLogin, name = 'loggedPassenger'),
    
    path('driver_login.html', views.driverLogin, name ='Dlogin'),
    path('driverUI.html', views.driverLogin, name = 'saveDriver'),

    path('passengerUI.html', views.passengerUI, name="passenger_ui"),

    path('passengerUI.html',views.passengerUI, name="bookcab"),
    
    path('paymentPage.html',views.paymentInfoPage , name = 'bookedDetails'),
    path('cancelCab.html',views.cancelCab ,name = 'cancelCab'),
    path('payGateway.html', views.payNow, name = 'moveToPay'),
    path('payGateway.html', views.payNow, name = 'pay'),

    path('FeedbackByPass.html', views.feedback, name = 'giveFeedback'),
    path('OLAP1.html', views.OLAP1, name = 'OLAP1'),
    path('OLAP2.html', views.OLAP2, name = 'OLAP2'),
    path('OLAP3.html', views.OLAP3, name = 'OLAP3'),
    path('OLAP4.html', views.OLAP4, name = 'OLAP4'),
    
]