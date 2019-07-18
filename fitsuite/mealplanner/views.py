from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse('Welcome to Meal Planner')

def fooditem(request, fooditem_id):
	return HttpResponse('Page for fooditem %s' % fooditem_id)

