from django.shortcuts import render, HttpResponse
from django.db import connection, IntegrityError
from deadline5.models import query2Model
from django.http import JsonResponse
from django.contrib import messages




# Create your views here.

def index(request):
    return render(request, 'index.html')

def query1(request):
    
    # return HttpResponse("this is query1")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cab where cab_location LIKE '%Room%' OR cab_location LIKE 'PO%';") # write down the query
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()
    return render(request, 'query1.html', context)
    # return render(request, 'query1.html' )

def query2(request):
    # return HttpResponse("this is query2")
    with connection.cursor() as cursor:
        cursor.execute("SELECT payment.payment_ID, passenger.passenger_ID, passenger.first_name, passenger.last_name, payment.Fare FROM passenger LEFT JOIN payment on payment.pass_ID = passenger.passenger_ID;") # write down the query
        rows = cursor.fetchall()

    # context = {'rows': rows}
    connection.close()
    return render(request, 'query2.html' , {'query2Model': rows})

def about(request):
    # return HttpResponse("this is about")
    return render(request, 'aboutUs.html')

def contact(request):
    # return HttpResponse("this is contact")
    return render(request, 'contactUs.html')

def trigger1(request):
    # return HttpResponse("this is contact")
    return render(request, 'trigger1.html')

def trigger2(request):
    # return HttpResponse("this is contact")
    return render(request, 'trigger2.html')

def checkTrigger1(request):

    with connection.cursor() as cursor:
        # cursor.execute("INSERT INTO driver (driver_ID, first_name, last_name, D_Email, Gender, date_of_birth, license_no) VALUES (2020102, 'aryan', 'sharma', 'aryan213@gmail.com', 'Female', '2002-02-18','232zvn817yx');") # write down the query
        #Inccorect query below, will give the trigger message and shown in the command terminal
        cursor.execute("INSERT INTO driver (driver_ID, first_name, last_name, D_Email, Gender, date_of_birth, license_no) VALUES (2020300, 'anikeda', 'shadadrma', 'anikdadaet1257@gmail.com', 'male', '2010-02-18','232zvn817yx');")
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()

    return render(request, 'checkTrigger1.html',context)

def checkTrigger2(request):

    with connection.cursor() as cursor:
        # cursor.execute("INSERT INTO d_contacts (driver_ID, contact) VALUES (2020102, 9869268502);") # write down the query
        #Inccorect query below, will give the trigger message and shown in the command terminal
        cursor.execute("INSERT INTO d_contacts (driver_ID, contact) VALUES (2020102, 98992685);")
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()

    return render(request, 'checkTrigger2.html',context)

def trigger1_message(request):
    if request.method == 'POST':
        # Retrieve the trigger message from the POST request
        message = request.POST.get('trigger1_message')
        # Add the message to the user's session using the messaging framework
        messages.success(request, message)
    return render(request,'trigger1_message.html')

def checkTrigger2(request):
    return render(request, 'checkTrigger2.html')

