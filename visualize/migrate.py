'''
Created on Jul 14, 2013

@author: Bishal Timilsina
'''
from django.db import connections
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ConnectionDoesNotExist    
from visualize import models

def setup_cursor():
   try:
      cursor = connections['legacy'].cursor()
      print 'Reached Here'
      return cursor
   except ConnectionDoesNotExist:
      print "Legacy database is not configured"
      return None

#CASE: DEMO
#def import_demo():
#CASE: FACT_TABLE
def import_fact():
    print 'You are not done'
    cursor = setup_cursor()
    if cursor is None:
        print 'Not Processing.....'
        return
    ## it's important selecting the id field, so that we can keep the publisher - book relationship

#CASE: DEMO
#    sql = """SELECT card_no, gender, age, age_group FROM demo"""
    sql = """SELECT pri_key, card_no, duration, time_8bit, time_of_day, isBusinessHr, Day_of_week, Day FROM fact_table"""    

    cursor.execute(sql)
    for row in cursor.fetchall():
#CASE: DEMO        
#        demo = models.Demo(card_no=row[0], gender=row[1], age=row[2],age_group=row[3])
#        print 'Processing.....'
#        demo.save()
#CASE: CALL_DETAILS
        fact = models.Fact_table(pri_key=row[0], card_no=row[1], duration=row[2], time_8bit=row[3], time_of_day=row[4], isBusinessHr=row[5], Day_of_week=row[6], Day=row[7])
        print 'Migrating.....'
        fact.save()
        
    print 'You are done'

def main():
#.........just appropriate naming
#CASE: DEMO
#    import_demo()
#CASE: FACT_TABLE
    import_fact()
    
if __name__=="__main__":
    main()
