from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

	# eg /mealplanner/fooditems/5/
	path('fooditems/<int:fooditem_id>/', views.fooditem, name='fooditem'),
]
