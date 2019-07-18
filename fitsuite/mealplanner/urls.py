from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

	# eg /mealplanner/fooditems/5/
	path('fooditems/<int:fooditem_id>/', views.fooditem, name='fooditem'),
	path('recipes/<int:fooditem_id>/', views.recipe, name='recipe'),

	path('addRecipe/', views.addRecipe, name="Add Recipe"),
	path('addFoodItem/', views.addFoodItem, name="Add Food Item"),
]
