from django.db import models

# Create your models here.
class district(models.Model):
   name=models.CharField(max_length=50)

class zone(models.Model):
   name=models.CharField(max_length=50)   

class dev_region(models.Model):
   name=models.CharField(max_length=50)

class phy_region(models.Model):
   name=models.CharField(max_length=50)

class address(models.Model):
   district_id=models.ForeignKey(district)
   zone_id=models.ForeignKey(zone)
   region_dev_id=models.ForeignKey(dev_region)
   region_phy_id=models.ForeignKey(phy_region)

class subscriber(models.Model):
   card_no=models.CharField(max_length=20,primary_key=True)
   name=models.CharField(max_length=100)
   surname=models.CharField(max_length=50)
   gender=models.BooleanField() # True for male & False for female
   dob=models.DateField()
   address_id=models.ForeignKey(address)
   age=models.IntegerField()

class date(models.Model):
   day=models.IntegerField()
   week=models.IntegerField()
   month=models.IntegerField()
   quater=models.IntegerField()
   half_year=models.BooleanField() # True for 1st half & False for 2nd half
   holiday=models.BooleanField()
   day_week=models.IntegerField()

class time(models.Model):
   sec=models.IntegerField()
   minute=models.IntegerField()
   hours=models.IntegerField()
   quater=models.IntegerField()

class service(models.Model):
   ser_id=models.IntegerField(primary_key=True)
   name=models.CharField(max_length=50)

class call(models.Model):
   card_no=models.ForeignKey(subscriber)
   date_key=models.ForeignKey(date)
   time_key=models.ForeignKey(time)
   service_key=models.ForeignKey(service)
   duration=models.IntegerField()   
   duration_classifier=models.IntegerField() # half , a, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10, 15, more than 15   
   peak_time=models.BooleanField() # peak: 8am to 8pm  offpeak:8pm to 8am
   sql_time_stamp=models.DateTimeField()
   called=models.BooleanField()
   received=models.BooleanField()
   sms=models.BooleanField()
   tran_card_id=models.CharField(max_length=20)

  