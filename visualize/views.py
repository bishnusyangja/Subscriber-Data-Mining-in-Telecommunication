from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template import loader,Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Max, Min, Avg
from analysis.models import district, zone, dev_region, phy_region, address, subscriber, date, time, service, call

# import rpy2.robjects as robjects

# default filter pages
def index(request):
   template = loader.get_template('visualize/visualize_home.html')
   return render(request,'visualize/visualize_home.html') 
 
def makenNlist(nlist):
   nnlist=[]
   for item in nlist:
      if item==None:
         item=0
      nnlist.append(item)
   return nnlist

def truncate(xlist):
   ylist=[]
   for item in xlist:
      if item==0 or item == None:
         continue
      ylist.append(item)
   return ylist



@csrf_exempt
def view_type(request):    
   # get either select drill or store False if no value is selected   
   selected_viz_gen = request.POST.get('category',False)   
   selected_drill = request.POST.get('drill',False)
   selected_drill2 = request.POST.get('drill2',False)
   selected_viz_res = request.POST.get('category2',False)   
   selected_anim = request.POST.get('animate',False)      
   # mask viz_gen if no value is given
   if selected_viz_gen=='select':
      selected_viz_gen=False
   if selected_viz_res=='select':
      selected_viz_res=False
   if selected_drill=='select':
      selected_drill=False
   if selected_drill2=='select':
      selected_drill2=False         

   title,category,xname,measure,yname=[],[],[],[],[]

   option1=selected_viz_gen and selected_drill and selected_drill2
   option2=selected_viz_res
   option3=selected_anim

   o1=option1 and (not option2) and (not option3)
   o2=option2 and (not option1) and (not option3)
   o3=option3 and (not option1) and (not option2)

   if o1:
      if selected_drill==selected_drill2:
         feedback='Drill Conflict!'
      else:
         # feedback='Drill Selection'         
         # print subscriber.objects.filter(age=25)
         if selected_viz_gen=='dur_avg':
            if selected_drill=='gender': 
               feedback='Drill Selection'
               title.append('Gender')         
               category.append('Gender')
               xname.append(['male','female','total'])
               measure.append('Average Call Duration')
               yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = i).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for i in range(2)]+[call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg']]))

               if selected_drill2=='age':
                  title.append('Age Group')
                  category.append('Age-group')               
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]])
                  measure.append('Average Call Duration')
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k,age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0,age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))
                                                    
               if selected_drill2=='month':               
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Average Call Duration')
                  mlist=[11,5,6,7]
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  
               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Average Call Duration')                  
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')                                
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Average Call Duration')                  
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                  
            if selected_drill=='age':
               feedback='Drill Selection'
               title.append('Age Group')         
               category.append('Age-group')
               xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
               measure.append('Average Call Duration')
               yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*i,age__lte=25+5*i).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for i in range(10)]+[call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg']]))

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Average Call Duration')
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x,age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender=x,age__gte=0).values_list('card_no', flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))
                                                    
               if selected_drill2=='month':               
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Average Call Duration')
                  mlist=[11,5,6,7]
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  
               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Average Call Duration')                  
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Average Call Duration')                  
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))         
            
            if selected_drill=='month':
               feedback='Drill Selection'
               title.append('Months')
               category.append('Months')               
               xname.append(['November','May','June','July'])
               measure.append('Average Call Duration')
               mlist=[11,5,6,7]
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]+[call.objects.filter(date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg']]))                             
               
               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Average Call Duration')
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Average Call Duration')
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                                                                 

               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Average Call Duration')                  
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=k,day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month__gte=0,day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Average Call Duration')  
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                                              
            if selected_drill=='day_of_week':
               feedback='Drill Selection'
               title.append('Day of Week')
               category.append('Day of Week')               
               xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
               measure.append('Average Call Duration')
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]+[call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg']]))                             
               mlist=[11,5,6,7]

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Average Call Duration')
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Average Call Duration')
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                                                                 

               if selected_drill2=='month':
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Average Call Duration')                  
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x,day_week=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x,day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')            
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Average Call Duration')  
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]))                             
                  
            if selected_drill=='hour':
               feedback='Drill Selection'
               title.append('HOur of Day')
               category.append('Hour of Day')               
               xname.append([str(j) for j in range(24)])
               measure.append('Average Call Duration')                 
               yname.append(makenNlist([call.objects.filter(time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(24)]+[call.objects.filter(time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg']]))                             

               mlist=[11,5,6,7]

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Average Call Duration')
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                  # yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Average Call Duration')
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                             
                  # yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(10)]))                                                                 

               if selected_drill2=='month':
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Average Call Duration')                  
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  # yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in mlist]))                             
                  
               title.append('Day of Week')
               category.append('Day of Week')               
               xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
               measure.append('Average Call Duration')
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]+[call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg']]))                             

               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Average Call Duration')  
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                  # yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=x+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Avg('duration'))['duration__avg'] for x in range(7)]))                             
                                                      
         elif selected_viz_gen=='dur_tot':
            if selected_drill=='gender': 
               feedback='Drill Selection'
               title.append('Gender')         
               category.append('Gender')
               xname.append(['male','female','total'])
               measure.append('Total Call Duration')
               yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = i).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for i in range(2)]+[call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum']]))

               if selected_drill2=='age':
                  title.append('Age Group')
                  category.append('Age-group')               
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]])
                  measure.append('Total Call Duration')
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k,age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0,age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))
                                                    
               if selected_drill2=='month':               
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Total Call Duration')
                  mlist=[11,5,6,7]
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  
               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Total Call Duration')                  
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Total Call Duration')                  
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                  
            if selected_drill=='age':
               feedback='Drill Selection'
               title.append('Age Group')         
               category.append('Age-group')
               xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
               measure.append('Total Call Duration')
               yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*i,age__lte=25+5*i).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for i in range(10)]+[call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum']]))

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Total Call Duration')
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x,age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender=x,age__gte=0).values_list('card_no', flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))
                                                    
               if selected_drill2=='month':               
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Total Call Duration')
                  mlist=[11,5,6,7]
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  
               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Total Call Duration')                  
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Total Call Duration')                  
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))         
            
            if selected_drill=='month':
               feedback='Drill Selection'
               title.append('Months')
               category.append('Months')               
               xname.append(['November','May','June','July'])
               measure.append('Total Call Duration')
               mlist=[11,5,6,7]
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]+[call.objects.filter(date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum']]))                             
               
               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Total Call Duration')
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Total Call Duration')
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                                                                 

               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Total Call Duration')                  
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=k,day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month__gte=0,day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Total Call Duration')  
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                                              
            if selected_drill=='day_of_week':
               feedback='Drill Selection'
               title.append('Day of Week')
               category.append('Day of Week')               
               xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
               measure.append('Total Call Duration')
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]+[call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum']]))                             
               mlist=[11,5,6,7]

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Total Call Duration')
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Total Call Duration')
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                                                                 

               if selected_drill2=='month':
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Total Call Duration')                  
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x,day_week=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x,day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Total Call Duration')  
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]))                             
                  
            if selected_drill=='hour':
               feedback='Drill Selection'
               title.append('HOur of Day')
               category.append('Hour of Day')         
               xname.append([str(j) for j in range(24)])
               measure.append('Total Call Duration')                 
               yname.append(makenNlist([call.objects.filter(time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(24)]+[call.objects.filter(time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum']]))                             

               mlist=[11,5,6,7]

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Total Call Duration')
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                  # yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Total Call Duration')
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                             
                  # yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(10)]))                                                                 

               if selected_drill2=='month':
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Total Call Duration')                  
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  # yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in mlist]))                             
                  
               title.append('Day of Week')
               category.append('Day of Week')               
               xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
               measure.append('Total Call Duration')
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]+[call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum']]))                             

               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Total Call Duration')  
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                  # yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=x+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).aggregate(Sum('duration'))['duration__sum'] for x in range(7)]))                             
                                                 
         else:
            if selected_drill=='gender': 
               feedback='Drill Selection'
               title.append('Gender')         
               category.append('Gender')
               xname.append(['male','female','total'])
               measure.append('Call Count')
               yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = i).values_list('card_no', flat=True)),called=True).count() for i in range(2)]+[call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),called=True).count()]))

               if selected_drill2=='age':
                  title.append('Age Group')
                  category.append('Age-group')               
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]])
                  measure.append('Call Count')
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k,age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),called=True).count() for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0,age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),called=True).count() for x in range(10)]))
                                                    
               if selected_drill2=='month':               
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Call Count')
                  mlist=[11,5,6,7]
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  
               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Call Count')                  
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Call Count')                  
                  for k in range(2):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = k).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender__gte=0).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                  
            if selected_drill=='age':
               feedback='Drill Selection'
               title.append('Age Group')         
               category.append('Age-group')
               xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
               measure.append('Call Count')
               yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*i,age__lte=25+5*i).values_list('card_no', flat=True)),called=True).count() for i in range(10)]+[call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),called=True).count()]))

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Call Count')
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x,age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),called=True).count() for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender=x,age__gte=0).values_list('card_no', flat=True)),called=True).count() for x in range(2)]))
                                                    
               if selected_drill2=='month':               
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Call Count')
                  mlist=[11,5,6,7]
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  
               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Call Count')                  
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Call Count')                  
                  for k in range(10):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*k,age__lte=25+5*k).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=0).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))         
            
            if selected_drill=='month':
               feedback='Drill Selection'
               title.append('Months')
               category.append('Months')               
               xname.append(['November','May','June','July'])
               measure.append('Call Count')
               mlist=[11,5,6,7]
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),called=True).count() for x in mlist]+[call.objects.filter(date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).count()]))                             
               
               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Call Count')
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),called=True).count() for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).count() for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Call Count')
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),called=True).count() for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),called=True).count() for x in range(10)]))                                                                 

               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Call Count')                  
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=k,day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month__gte=0,day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Call Count')  
                  for k in mlist:
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=k).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month__gte=0).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                                              
            if selected_drill=='day_of_week':
               feedback='Drill Selection'
               title.append('Day of Week')
               category.append('Day of Week')               
               xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
               measure.append('Call Count')
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]+[call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).count()]))                             
               mlist=[11,5,6,7]

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Call Count')
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),called=True).count() for x in range(2)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).count() for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Call Count')
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),called=True).count() for x in range(10)]))                             
                  yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).count() for x in range(10)]))                                                                 

               if selected_drill2=='month':
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Call Count')                  
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x,day_week=k+1).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x,day_week__gte=0).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                           
               if selected_drill2=='hour':
                  title.append('HOur of Day')
                  category.append('Hour of Day')               
                  xname.append(([str(j) for j in range(24)]))
                  measure.append('Call Count')  
                  for k in range(7):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=k+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                  yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]))                             
                  
            if selected_drill=='hour':
               feedback='Drill Selection'
               title.append('HOur of Day')
               category.append('Hour of Day')               
               xname.append([str(j) for j in range(24)])
               measure.append('Call Count')                 
               yname.append(makenNlist([call.objects.filter(time_key__in=(time.objects.filter(hours__gte=x,hours__lte=x+1).values_list('id',flat=True)),called=True).count() for x in range(24)]+[call.objects.filter(time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).count()]))                             

               mlist=[11,5,6,7]

               if selected_drill2=='gender':
                  title.append('Gender')
                  category.append('Gender')               
                  xname.append(['male','female'])
                  measure.append('Call Count')
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).count() for x in range(2)]))                             
                  # yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(gender = x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).count() for x in range(2)]))                             
                                                    
               if selected_drill2=='age':               
                  title.append('Age Group')         
                  category.append('Age-group')
                  xname.append([str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total'])               
                  measure.append('Call Count')
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).count() for x in range(10)]))                             
                  # yname.append(makenNlist([call.objects.filter(card_no__in=(subscriber.objects.filter(age__gte=20+5*x,age__lte=25+5*x).values_list('card_no', flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).count() for x in range(10)]))                                                                 

               if selected_drill2=='month':
                  title.append('Months')
                  category.append('Months')               
                  xname.append(['November','May','June','July'])
                  measure.append('Call Count')                  
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  # yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(month=x).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).count() for x in mlist]))                             
                  
               title.append('Day of Week')
               category.append('Day of Week')               
               xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
               measure.append('Call Count')
               yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),called=True).count() for x in range(7)]+[call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=0).values_list('id',flat=True)),called=True).count()]))                             

               if selected_drill2=='day_of_week':
                  title.append('Day of Week')
                  category.append('Day of Week')               
                  xname.append(['Sunday','Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday'])
                  measure.append('Call Count')  
                  for k in range(24):
                     yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week=x+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=k,hours__lte=k+1).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                  # yname.append(makenNlist([call.objects.filter(date_key__in=(date.objects.filter(day_week__gte=x+1).values_list('id',flat=True)),time_key__in=(time.objects.filter(hours__gte=0).values_list('id',flat=True)),called=True).count() for x in range(7)]))                             
                                                                
         
   elif o2:
      feedback='Generic Selection'                      
      if selected_viz_res == 'gender_base':
         title.append('Genderwise Subscriber Distribution')         
         category.append('Gender')
         xname = ['male','female','total']
         measure.append('Number of Subscriber')
         alist = [subscriber.objects.filter(gender = i).count() for i in range(2)]
         alist.append(subscriber.objects.filter(gender__gte = 0).count())
         yname = alist
      elif selected_viz_res == 'age_base':
         title.append('Agegroupwise Subscriber Distribution')         
         category.append('AgeGroup')
         xname = [str(j)+'-'+str(j+5) for j in [20+5*i for i in range(10)]]+['total']
         measure.append('Number of Subscriber')
         yname = [subscriber.objects.filter(age__gte=20+i*5, age__lte=25+i*5).count() for i in range(10)]

      elif selected_viz_res == 'tot_week':   
         title.append('Weekly Call Count for Total Subscriber')         
         category.append('Number of week')
         measure.append('Call Count')
         yname = [call.objects.filter(date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
         yname = truncate(yname)
         xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'male_week':
         title.append('Weekly Call Count for male Subscriber')         
         category.append('Number of week')
         measure.append('Call Count')
         yname = [call.objects.filter(card_no__in = subscriber.objects.filter(gender=0).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
         yname = truncate(yname)
         xname = [i+1 for i in range(len(yname))]


      elif selected_viz_res == 'female_week':
         title.append('Weekly Call Count for female Subscriber')         
         category.append('Number of week')
         measure.append('Call Count')
         yname = [call.objects.filter(card_no__in = subscriber.objects.filter(gender=1).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
         yname = truncate(yname)
         xname = [i+1 for i in range(len(yname))]


      elif selected_viz_res == 'age20_week':
         title.append('Weekly Call Count for AgeGroup 20-25 Subscriber')         
         category.append('Number of week')
         measure.append('Call Count')
         yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=20,age__lt=25).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
         yname = truncate(yname)
         xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age25_week':
            title.append('Weekly Call Count for AgeGroup 25-30 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=25,age__lt=30).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age30_week':
            title.append('Weekly Call Count for AgeGroup 30-35 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=30,age__lt=35).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age35_week':
            title.append('Weekly Call Count for AgeGroup 35-40 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=35,age__lt=40).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age40_week':
            title.append('Weekly Call Count for AgeGroup 40-45 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=40,age__lt=45).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age45_week':
            title.append('Weekly Call Count for AgeGroup 45-50 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=40,age__lt=45).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age50_week':
            title.append('Weekly Call Count for AgeGroup 50-55 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=50,age__lt=55).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age55_week':
            title.append('Weekly Call Count for AgeGroup 55-60 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=55,age__lt=60).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age60_week':
            title.append('Weekly Call Count for AgeGroup 60-65 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=60,age__lt=65).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

      elif selected_viz_res == 'age65_week':
            title.append('Weekly Call Count for AgeGroup 65-70 Subscriber')
            category.append('Number of week')
            measure.append('Call Count')
            yname = [call.objects.filter(card_no__in = subscriber.objects.filter(age__gte=65,age__lt=70).values_list('card_no'), date_key__in = (date.objects.filter(week = i+1).values_list('id'))).count() for i in range(53)]
            yname = truncate(yname)
            xname = [i+1 for i in range(len(yname))]

   elif o3:
      feedback='Animation Selection'                      


   else:
      feedback='Selection Error!'
   
      

   return render_to_response("visualize/visualize_home.html",Context({'xname':xname,'yname':yname,'category':category,'measure':measure,'title':title,'feedback':feedback}))

