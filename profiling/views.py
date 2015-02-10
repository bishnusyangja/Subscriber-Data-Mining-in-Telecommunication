# Create your views here.
from django.shortcuts import render_to_response

# default profiling pages
def index(request):
	return render_to_response('profiling/fit_home.html')	