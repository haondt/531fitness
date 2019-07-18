from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse('Welcome to Meal Planner')

def fooditem(request, fooditem_id):
	return HttpResponse('Page for fooditem %s' % fooditem_id)

def addFoodItem(request):
	return HttpResponse('Page for adding a fooditem')

def addRecipe(request):
	return HttpResponse('Page for adding a recipe')

def recipe(request, fooditem_id):
	return HttpResponse('Page for viewing recipe %s' % fooditem_id)

