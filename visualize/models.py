from django.db import models

# Create your models here.
class Demo(models.Model):
    card_no=models.CharField(max_length=20,primary_key=True)
    gender=models.IntegerField()
    age=models.IntegerField()
    age_group=models.IntegerField()

class Fact_table(models.Model):
    pri_key=models.BigIntegerField(primary_key=True)
    card_no=models.CharField(max_length=20)
    duration=models.IntegerField()
    time_8bit=models.CharField(max_length=8)
    time_of_day=models.IntegerField()
    isBusinessHr=models.IntegerField()
    Day_of_week=models.IntegerField()
    Day=models.IntegerField()

class call(models.Model):
    pri_key=models.BigIntegerField(primary_key=True)
    card_no=models.CharField(max_length=20)
    service_key=models.IntegerField()
    calling_no=models.CharField(max_length=20)
    called_no=models.CharField(max_length=20)
    answer_date_time=models.DateTimeField()
    clear_date_time=models.DateTimeField()
    Duration=models.IntegerField()
    sub_fee1=models.FloatField()

