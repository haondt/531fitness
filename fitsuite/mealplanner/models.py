from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Define base food item
class FoodItem(models.Model):
	name = models.CharField(max_length=100)
	unit = models.CharField(max_length=10)
	s_quantity = models.FloatField(default=0)
	s_cost = models.FloatField(default=0)
	s_cal = models.FloatField(default=0)
	s_protein = models.FloatField(default=0)
	s_fat = models.FloatField(default=0)
	s_carbs = models.FloatField(default=0)
	b_quantity = models.FloatField(null=True, blank=True)
	b_cost = models.FloatField(null=True, blank=True)
	has_ingredients = models.BooleanField(null=False, blank=False, default=False)
	def __str__(self):
		return self.name


# Define recipie ingredient table
class RecipeIngredient(models.Model):
	recepie = models.ForeignKey('FoodItem', on_delete=models.CASCADE,
		related_name='ingredient_recipe',)
	ingredient = models.ForeignKey('FoodItem', on_delete=models.CASCADE,
		related_name='ingredient_ingredient',)

	def __str__(self):
		return self.Ingredient
