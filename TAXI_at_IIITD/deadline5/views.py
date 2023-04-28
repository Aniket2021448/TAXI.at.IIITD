import random
from django.shortcuts import render, HttpResponse,redirect
from django.db import connection, IntegrityError
from deadline5.models import query2Model
from django.http import JsonResponse
from django.contrib import messages
from deadline5.models import Passenger,Driver, Account, Cab, Bookedcab, DContacts, Card
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.core.cache import cache 
from django.utils import timezone
from datetime import date, datetime
from django.db import transaction


# Create your views here.
passengerID = 0
cabID = 0
driverID = 0

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

def OLAP1(request):
    
    with connection.cursor() as cursor:
        # cursor.execute("INSERT INTO d_contacts (driver_ID, contact) VALUES (2020102, 9869268502);") # write down the query
        #Inccorect query below, will give the trigger message and shown in the command terminal
        cursor.execute("SELECT * FROM cab_passenger_payments_view;")
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()

    return render(request, 'OLAP1.html', context)

def OLAP2(request):
    

    with connection.cursor() as cursor:
        # cursor.execute("INSERT INTO d_contacts (driver_ID, contact) VALUES (2020102, 9869268502);") # write down the query
        #Inccorect query below, will give the trigger message and shown in the command terminal
        cursor.execute("SELECT passenger.passenger_ID,  passenger.Gender, DATE_FORMAT(ride_date, '%Y-%m-%d') AS day, COUNT(*) AS total_rides, SUM(fare) AS total_revenue FROM bookedcab INNER JOIN passenger ON passenger.passenger_ID = bookedCab.passenger_ID INNER JOIN payment ON passenger.passenger_ID = payment.pass_ID WHERE ride_date >= '2022-01-01' AND ride_date <= '2022-12-31' GROUP BY DAY(ride_date),DATE_FORMAT(ride_date, '%Y-%m-%d'), passenger.Gender, passenger.passenger_ID WITH ROLLUP ORDER BY  day desc,total_revenue desc;")
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()
    return render(request, 'OLAP2.html', context)

def OLAP3(request):

    with connection.cursor() as cursor:
        # cursor.execute("INSERT INTO d_contacts (driver_ID, contact) VALUES (2020102, 9869268502);") # write down the query
        #Inccorect query below, will give the trigger message and shown in the command terminal
        cursor.execute("SELECT * FROM passenger_spend_view WHERE year = 2022;")
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()
    return render(request, 'OLAP3.html', context)

def OLAP4(request):
    
    with connection.cursor() as cursor:
        # cursor.execute("INSERT INTO d_contacts (driver_ID, contact) VALUES (2020102, 9869268502);") # write down the query
        #Inccorect query below, will give the trigger message and shown in the command terminal
        cursor.execute("SELECT * FROM passenger_rides_view;")
        rows = cursor.fetchall()

    context = {'rows': rows}
    connection.close()
    return render(request, 'OLAP4.html', context)


def passengerLogin(request):
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        request.session['email'] = email
        accOBJ = Account.objects.get(email = request.session.get('email'))
        # print("accobj: ",accOBJ)

        passengerID = accOBJ.passenger_id
        passName = Passenger.objects.get(passenger_id = passengerID).first_name
        

        with connection.cursor() as cursor:
            try:

                cursor.execute("select first_name from passenger where passenger_ID=(SELECT passenger_ID from account where email = %s and password = %s)", [email, password])
                reqUser = cursor.fetchone()
                
                return render(request, 'passengerUI.html', {'name':passName.upper()})
            except:
                messages.error(request, 'Error while loading the login details')
                return redirect('passenger_ui')
            finally:
                cursor.close()

    return render(request,'passenger_login.html')

    
def passengerUI(request):

    if request.method == "POST":

        pickup = request.POST['pickup']
        destination = request.POST['destination']
        # request.session['email'] = email
        accOBJ = Account.objects.get(email = request.session.get('email'))
        # print("accobj: ",accOBJ)

        passengerID = accOBJ.passenger_id

        # print(passengerID)
        # passengerID = 
        with connection.cursor() as cursor:
            try:
            # print("In try block")
                cursor.execute("START TRANSACTION;")
                cursor.execute("SET @cabID = 0;")
                cursor.execute("SELECT cab_ID INTO @cabID FROM Cab WHERE cab_status = 'available' ORDER BY RAND() LIMIT 1;")
                cursor.execute("UPDATE Cab SET cab_status = 'Busy' WHERE cab_ID = @cabID;")
                cursor.execute("SELECT @cabID;")
                cabID = cursor.fetchall()
                cursor.execute("SET @driverID = 0;")
                cursor.execute("SELECT driver_ID INTO @driverID FROM driver WHERE Status = 'available' ORDER BY RAND() LIMIT 1;")
                cursor.execute("SELECT @driverID;")
                driverID = cursor.fetchall()
                cursor.execute("UPDATE driver SET Status = 'Busy' WHERE driver_ID = @driverID;") 
                cursor.execute("INSERT INTO bookedcab (drop_time, pickUp_time, passenger_ID, Driver_ID, Cab_ID, ride_date, pickup, destination) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [timezone.now().strftime('%H:%M:%S'),timezone.now().strftime('%H:%M:%S'),passengerID , driverID, cabID, date.today().strftime('%Y-%m-%d'), pickup, destination]) 
                cursor.execute("UPDATE passenger SET cab_ID = %s WHERE passenger_ID = %s", [cabID, passengerID])
                cursor.execute("COMMIT;")
                print("Executedall")

                return redirect('bookedDetails')

            except:
                print("In except block")
                cursor.execute("ROLLBACK")
                messages.error(request, 'Cannot book cab, try again.')
                return redirect('passenger_ui')
    else:

        return render(request, 'passengerUI.html')



def passengerSignup(request):
    if request.method == "POST" :

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        Gender = request.POST['gender']
        location = request.POST['location']
        email = request.POST['Email']
        password = request.POST['Password']
        username = firstname+'@'+password

        with connection.cursor() as cursor:
            try:

                cursor.execute("START TRANSACTION;")
                cursor.execute("INSERT INTO Passenger (first_name, last_name, gender, location) VALUES (%s, %s, %s, %s);", [firstname, lastname, Gender, location])
                cursor.execute("SET @passenger_id = LAST_INSERT_ID();")
                cursor.execute("select  @passenger_id;")
                passengerID = cursor.fetchall()
                cursor.execute("INSERT INTO ACCOUNT(email, password, username, passenger_ID) VALUES(%s, %s, %s, %s);", [email, password, username, passengerID])
                cursor.execute("COMMIT;")
                return render(request, 'passenger_login.html')

            except:
                cursor.execute("ROLLBACK")
                messages.error(request, 'There was a problem making changes to the database.')
                return redirect('Psignup')
            finally:
                cursor.close()
    else:
        return render(request, 'passenger_signup.html')

def driverLogin(request):
    if request.method == "POST" :
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        Email = request.POST['email']
        Gender = request.POST['gender']
        dob = request.POST['dob']
        license = request.POST['license_no']

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Driver (first_name, last_name,d_email, gender, date_of_birth, license_no) VALUES (%s, %s, %s, %s, %s, %s)", [firstname, lastname, Email, Gender, dob, license])
            # cursor.commit() is inbuilt in django
            #         finally:
            cursor.close() 
        return render(request, 'driverUI.html')
    
    else:
        return render(request, 'driver_login.html')
    

def paymentInfoPage(request):

    accOBJ = Account.objects.get(email = request.session.get('email'))
    passengerID = accOBJ.passenger_id

    with connection.cursor() as cursor:
        try:

            # cabBooked and passenger details are stored in passenger table
            user = Passenger.objects.get(passenger_id = passengerID)
            # print("got user")

            bookedDetails = Bookedcab.objects.filter(passenger = passengerID).order_by('-bookedcab_id').first()
            # print("got detials")
            bookedDriver = Driver.objects.get(driver_id = int(str(bookedDetails.driver).split()[2][1:-1]))
            # print("got driver")
            bookedCab = Cab.objects.get(cab_id= int(str(bookedDetails.cab).split()[2][1:-1]))
            # print("got cab")
            # print(int(str(bookedDetails.driver).split()[2][1:-1]))
            # driverMobile = DContacts.objects.get(driver = int(str(bookedDetails.driver).split()[2][1:-1]))
            # print(driverMobile.contact)
            # print("got mobile")
# ,'Dmobile':driverMobile
            context = {'bookingDetails': bookedDetails, 'cab': bookedCab, 'driver':bookedDriver}
            # print(context)

            return render(request, 'paymentPage.html', context)
            
        except:
            # cursor.execute("ROLLBACK")
            messages.error(request, 'There was a problem extracting details from the database.')
            return redirect('bookcab')

        finally:    
            cursor.close()

def cancelCab(request):

    accOBJ = Account.objects.get(email = request.session.get('email'))
    passengerID = accOBJ.passenger_id
    passengerName = Passenger.objects.get(passenger_id = passengerID).first_name


    with connection.cursor() as cursor:
        try:
            
            cursor.execute("START TRANSACTION;")
            cursor.execute("SET @cabID = 0;")
            cursor.execute("SET @driverID = 0;")
            cursor.execute("SELECT Cab_ID, driver_ID INTO @cabID,@driverID FROM bookedcab WHERE passenger_ID = %s AND pickUp_time = (SELECT MAX(pickUp_time) FROM (SELECT * FROM bookedcab) AS temp_table WHERE passenger_ID = %s);",[passengerID,passengerID ])
            cursor.execute("select @driverID;")
            driverID = cursor.fetchall()
            cursor.execute("select @cabID;")
            cabID = cursor.fetchall()
            cursor.execute("UPDATE cab SET cab_status = 'available' where cab_ID = @cabID;")
            cursor.execute("UPDATE driver SET status = 'available' where driver_ID = @driverID;")
            cursor.execute("delete FROM bookedcab WHERE passenger_ID = %s AND pickUp_time = (SELECT MAX(pickUp_time) FROM (SELECT * FROM bookedcab) AS temp_table WHERE passenger_ID = %s);",[passengerID,passengerID])
            cursor.execute("COMMIT;")
            
            return render(request ,'passengerUI.html', {'name': passengerName})
        except:

            messages.error(request, 'Cannot delete cab now, you are late.')
            return redirect('bookedDetails')
        finally:
            cursor.close()

def payNow(request):

    
    rand_num = random.randint(101, 500)
    print("Fare: ",rand_num)
    if 'pay' in request.POST:
    # if request.method == "POST":
        print(request.POST)
        cardNumber = request.POST['cardNumber']
        Hname = request.POST['Hname']
        cvv = request.POST['CVV']
        expiry = request.POST['Expiry Date']
        print(Hname)
        print(expiry)
        accOBJ = Account.objects.get(email = request.session.get('email'))
        accountID = accOBJ.account_id
        print("accontID: ",accountID)
        passengerID = accOBJ.passenger_id
        print("passenger: ",passengerID)
        bookedDetails = Bookedcab.objects.filter(passenger = passengerID).order_by('-bookedcab_id').first()
        
        bookedDriver = Driver.objects.get(driver_id = int(str(bookedDetails.driver).split()[2][1:-1]))
        driver = bookedDriver.driver_id
        print("driver: ",driver)
        bookedCab = Cab.objects.get(cab_id= int(str(bookedDetails.cab).split()[2][1:-1]))
        cab = bookedCab.cab_id
        print("cab: ",cab)
        
        with connection.cursor() as cursor:
            try:
                cursor.execute("select card_ID from card where card_number= %s ;", [cardNumber])
                cardID = cursor.fetchone()
                print("old card: ")
                if(cardID is not None):
                    # this card already exists
                    # use this cardID for further processing
                    cardOBJ = Card.objects.get(card_number = cardNumber)
                    print(cardOBJ)
                    cardID = cardOBJ.card_id
                    print("cardID:",cardID)
                    if cardOBJ.balance>=rand_num:

                        cursor.execute("START TRANSACTION;")
                        cursor.execute("UPDATE card SET balance = Balance - %s WHERE card_ID = %s;",[rand_num, cardID])
                        cursor.execute("UPDATE driver SET wallet = wallet + %s WHERE driver_ID = %s;",[rand_num, driver])
                        cursor.execute("UPDATE driver SET status = 'available' WHERE driver_ID = %s;",[driver])
                        cursor.execute("UPDATE cab SET cab_status = 'available' WHERE cab_ID = %s;",[cab])
                        cursor.execute("INSERT INTO payment (Payment_time,Fare, card_ID, pass_ID) VALUES (%s, %s, %s, %s);",[datetime.now() ,rand_num, cardID, passengerID])
                        cursor.execute("UPDATE bookedcab SET drop_time = %s where bookedCab_ID = %s;",[timezone.now().strftime('%H:%M:%S'), bookedDetails.bookedcab_id])    
                        cursor.execute("COMMIT;")

                        return render(request, "FeedbackByPass.html")

                    else:

                        messages.error(request, 'INSUFFICIENT BALANCE')
                        return redirect('pay')

                else:
                   
                    
                    cursor.execute("INSERT INTO card (card_number, Expiry,CVV, Holders_name, Account_ID) VALUES (%s, %s,%s, %s, %s);",[cardNumber, expiry, cvv, Hname,accountID])
                    
                    cardOBJ = Card.objects.get(card_number = cardNumber)
                    cardID = cardOBJ.card_id

                    cursor.execute("START TRANSACTION;")    
                    cursor.execute("UPDATE card SET balance = Balance - %s WHERE card_ID = %s;",[rand_num, cardID])
                    cursor.execute("UPDATE driver SET wallet = wallet + %s WHERE driver_ID = %s;",[rand_num, driver])
                    cursor.execute("UPDATE driver SET status = 'available' WHERE driver_ID = %s;",[driver])
                    cursor.execute("UPDATE cab SET cab_status = 'available' WHERE cab_ID = %s;",[cab])
                    cursor.execute("INSERT INTO payment (Payment_time,Fare, card_ID, pass_ID) VALUES (%s, %s, %s, %s);",[datetime.now() ,rand_num, cardID, passengerID])
                    cursor.execute("UPDATE bookedcab SET drop_time = %s where bookedCab_ID = %s;",[timezone.now().strftime('%H:%M:%S'), bookedDetails.bookedcab_id])    
                    cursor.execute("COMMIT;")
                    return render(request, "FeedbackByPass.html")
                
            except:
                print("in excpet")
                cursor.execute("ROLLBACK;")
                # dubara payment krlo
                return redirect('bookedDetails')


    return render(request, 'payGateway.html', {'fare':rand_num})

def feedback(request):
    

    if request.method == "POST" :
        message = request.POST["feedback"]
        rating = request.POST["rating"]
        rating = 2 * int(rating)

        accOBJ = Account.objects.get(email = request.session.get('email'))
        passengerID = int(accOBJ.passenger_id)
        bookedDetails = Bookedcab.objects.filter(passenger = passengerID).order_by('-bookedcab_id').first()
        driver = int(str(bookedDetails.driver).split()[2][1:-1])


        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO feedback (Message, Rating, driver_ID, passenger_ID) VALUES (%s,%s,%s,%s);",[message, rating, driver, passengerID])
            cursor.close()

        
        return render(request, 'passengerUI.html', {'name': Passenger.objects.get(passenger_id = passengerID).first_name})
    return render(request,'FeedbackByPass.html')

