from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from .manager import CustomerManager
from django.utils import timezone

# Create your models here.


# class CustomUser(AbstractBaseUser, PermissionsMixin):

#     email = models.EmailField(unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     data_joined = models.DateTimeField(default=timezone.now)
#     passengerID = models.BigAutoField(primary_key=True , auto_created=True)
    

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomerManager()
#     def _str_(self):
#         return self.email


class query2Model(models.Model):
    payment_id = models.IntegerField(unique=True)  # Field name made lowercase
    passenger_id = models.IntegerField()  # Field name made lowercase.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Fare = models.IntegerField()

class Account(models.Model):
    account_id = models.AutoField(db_column='account_ID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(max_length=255)
    username = models.CharField(db_column='UserName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    passenger_id = models.IntegerField(db_column='passenger_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'



class Bookedcab(models.Model):
    bookedcab_id = models.AutoField(db_column='bookedCab_ID', primary_key=True)  # Field name made lowercase.
    drop_time = models.TimeField(blank=True, null=True)
    pickup_time = models.TimeField(db_column='pickUp_time', blank=True, null=True)  # Field name made lowercase.
    passenger = models.ForeignKey('Passenger', models.DO_NOTHING, db_column='passenger_ID', blank=True, null=True)  # Field name made lowercase.
    driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='Driver_ID', blank=True, null=True)  # Field name made lowercase.
    cab = models.ForeignKey('Cab', models.DO_NOTHING, db_column='Cab_ID', blank=True, null=True)  # Field name made lowercase.
    ride_date = models.DateField(blank=True, null=True)
    pickup = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'bookedcab'


class Cab(models.Model):
    cab_id = models.IntegerField(db_column='Cab_ID', primary_key=True)  # Field name made lowercase.
    owner_name = models.CharField(db_column='Owner_name', max_length=100)  # Field name made lowercase.
    number_plate = models.CharField(db_column='Number_plate', max_length=100)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=45)  # Field name made lowercase.
    cab_location = models.CharField(db_column='Cab_location', max_length=100)  # Field name made lowercase.
    cab_status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'cab'


class Card(models.Model):
    card_id = models.AutoField(db_column='card_ID', primary_key=True)  # Field name made lowercase.
    card_number = models.CharField(unique=True, max_length=20, blank=True, null=True)
    expiry = models.DateField(db_column='Expiry')  # Field name made lowercase.
    cvv = models.IntegerField(db_column='CVV')  # Field name made lowercase.
    holders_name = models.CharField(db_column='Holders_name', max_length=50)  # Field name made lowercase.
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='Account_ID')  # Field name made lowercase.
    balance = models.IntegerField(db_column='Balance', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'card'


class DContacts(models.Model):
    driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='driver_ID', blank=True, null=True)  # Field name made lowercase.
    contact = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_contacts'

class Driver(models.Model):
    driver_id = models.AutoField(db_column='driver_ID', primary_key=True)  # Field name made lowercase.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    d_email = models.CharField(db_column='D_Email', unique=True, max_length=50)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    date_of_birth = models.DateField()
    license_no = models.CharField(max_length=20)
    wallet = models.IntegerField(blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'driver'


class Feedback(models.Model):
    feedback_id = models.AutoField(db_column='Feedback_ID', primary_key=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=500)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='driver_ID', blank=True, null=True)  # Field name made lowercase.
    passenger = models.ForeignKey('Passenger', models.DO_NOTHING, db_column='Passenger_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feedback'
        unique_together = (('driver', 'passenger'),)


class PContacts(models.Model):
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='account_ID', blank=True, null=True)  # Field name made lowercase.
    contact = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p_contacts'


class Passenger(models.Model):
    passenger_id = models.AutoField(db_column='passenger_ID', primary_key=True)  # Field name made lowercase.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    location = models.CharField(max_length=100)
    cab = models.ForeignKey(Cab, models.DO_NOTHING, db_column='Cab_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'passenger'


class Payment(models.Model):
    payment_id = models.IntegerField(db_column='payment_ID', primary_key=True)  # Field name made lowercase.
    payment_time = models.DateTimeField(db_column='Payment_time')  # Field name made lowercase.
    fare = models.FloatField(db_column='Fare', blank=True, null=True)  # Field name made lowercase.
    card = models.ForeignKey(Card, models.DO_NOTHING, db_column='card_ID', blank=True, null=True)  # Field name made lowercase.
    pass_field = models.ForeignKey(Passenger, models.DO_NOTHING, db_column='pass_ID', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'payment'