from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from visualize.models import Demo,Fact_table
# default filter pages
def index(request):
	template = loader.get_template('analysis/fit_home.html')
	return render(request,'analysis/fit_home.html')	

# filter page after post method
	#print selected_gender	



#Another method to do it
#method - 1 
#try:
#     is_private = request.POST['is_private']
# except MultiValueDictKeyError:
#     is_private = False
#method - 2
# if request.method == 'POST':
# 	print "asdfds"
# if "gender" in request.POST:
# 	selected_value = request.POST["sample"]
# else:
# 	selected_value = None
# <QueryDict: {u'colName': [u'duration'], u'end_date': [u'07/16/2013'], u'gender': [u'0'], 
# u'end_age': [u'34'], u'aggregation': [u'grpBy'], u'start_age': [u'27'], u'startTime': [u'9'], 
# u'aggId': [u'date'], u'endTime': [u'16'], u'start_date': [u'07/01/2013'], u'select': [u'avg']}>


@csrf_exempt
def filter(request):
	dates = False
	print "Before edit"
	print request.POST 
	#get either select gender or store False if no value is selected
	selected_gender = request.POST.get('gender',False)
	selected_start_age = request.POST.get('start_age',False)
	#mask start_age if no value is given
	if selected_start_age=='-1':
		selected_start_age=False
	selected_end_age = request.POST.get('end_age',False)
	#mask end_age if no value is given
	if selected_end_age=='-1':
		selected_end_age=False
	#Q:- What to do if user left on field on put value on either start_age or in end_age box
	if selected_start_age or selected_end_age:
		if selected_start_age == False:
			selected_start_age = 16
		if selected_end_age == False:
			selected_end_age = 72
	selected_select = request.POST.get('select',False)
	if selected_select == 'select':
		selected_select = False
	selected_colName = request.POST.get('colName',False)
	if selected_colName == 'select':
		selected_colName = False	
	selected_start_time = request.POST.get('startTime',False)
	if selected_start_time=='-1':
		selected_start_time=False
	print "start time"
	print selected_start_time
	selected_end_time = request.POST.get('endTime',False)
	if selected_end_time=='-1':
		selected_end_time=False
	print "end time"
	print selected_end_time
	#Q:- What to do if user left on field on put value on either start_time or in end_time box
	#ans:- if user enter value only in start_time then filter the call duration between start_time and mid_night
	# if user enter value only in end_time then filter the call duration between morning(0) to that time
	#------------------------------------------------------------------------
	# if selected_start_time or selected_end_time:
	# 	if selected_start_age == False:
	# 		selected_start_age = 00#equeal to initial time of the day
	# 	if selected_end_age == False:
	# 		selected_end_age = 4 #should be changed to 23 for 24 hours in updated database
	# also you have to do for the cyclic pattern of the time if between 22 hours to 6 hours
	selected_start_date = (request.POST.get('start_date',False))
	if selected_start_date:
		selected_start_day = selected_start_date.split('/')[1]
		print "Start Day"
		print selected_start_day
	selected_end_date = (request.POST.get('end_date',False))
	if selected_end_date:
		selected_end_day = selected_end_date.split('/')[1]
		print "End Day"
		print selected_end_day
	
	selected_aggregation = request.POST.get('aggregation',False)
				
	#-------------------------------------------------------
	if selected_aggregation == 'select':
		selected_aggregation = False
	selected_aggId = request.POST.get('aggId',False)
	if selected_aggId == 'select':
		selected_aggId = False
	#initialize the variable dates_demo
	#testing the loop
	print selected_end_time 
	print selected_start_time 
	print (selected_end_time>=selected_start_time)
	dates_demo = False 
	dates_fact_table = False
	#-----------------------------------datetime block--------------------
	if selected_gender and selected_start_age and selected_end_age:
		# dates_demo = Demo.objects.filter(gender=int(selected_gender), age__range=[self.selected_start_age,self.selected_end_date])
		dates_demo = Demo.objects.filter(gender=int(selected_gender), age__gte=selected_start_age, age__lte=selected_end_age)
		return render_to_response("analysis/fit_home.html", 
		{'dates_demo':dates_demo})
	elif selected_gender:
		dates_demo = Demo.objects.filter(gender=int(selected_gender))
		return render_to_response("analysis/fit_home.html", 
		{'dates_demo':dates_demo})
	elif selected_start_age and selected_end_age:
		dates_demo = Demo.objects.filter(age__gte=selected_start_age, age__lte=selected_end_age)
		return render_to_response("analysis/fit_home.html", 
		{'dates_demo':dates_demo})
	#do operation of date and time slot to filter the data
	elif selected_end_time and selected_start_time and (selected_end_time>=selected_start_time):
		if selected_end_date and selected_start_date:
			dates_fact_table = Fact_table.objects.filter(time_of_day__gte=selected_start_time,time_of_day__lte=selected_end_time,Day__gte=selected_start_day,Day__lte=selected_end_day)[:100]
			return render_to_response("analysis/fit_home.html", 
				{'dates_fact_table':dates_fact_table})
		else:
			dates_fact_table = Fact_table.objects.filter(time_of_day__gte=selected_start_time,time_of_day__lte=selected_end_time)[:100]
			return render_to_response("analysis/fit_home.html", 
				{'dates_fact_table':dates_fact_table})
	elif selected_end_time and selected_start_time and (selected_end_time<selected_start_time):
		if selected_end_day and selected_start_day:
			dates_fact_table = Fact_table.objects.filter(time_of_day__lte=selected_start_time,time_of_day__gte=selected_end_time,Day__get=selected_start_day,Day__lte=selected_end_day)[:100]
			return render_to_response("analysis/fit_home.html",
				{'dates_fact_table':dates_fact_table})
		else:
			dates_fact_table = Fact_table.objects.filter(time_of_day__lte=selected_start_time,time_of_day__gte=selected_end_time)[:100]
			return render_to_response("analysis/fit_home.html", 
				{'dates_fact_table':dates_fact_table})
	#------------------------Sex, Gender Block-------------------------------------
	
	return render_to_response("analysis/fit_home.html", 
		{'dates_demo' : dates_demo}) 

