from django.shortcuts import render
from django.template import loader

def index(request):
	template = loader.get_template('telde/home.html')
	return render(request,'telde/home.html')

# def about(request):
# 	template = loader.get_template('telde/about.html')
# 	return render(request,'telde/about.html')