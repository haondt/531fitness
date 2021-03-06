# Generated by Django 2.2.2 on 2019-07-01 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=10)),
                ('s_quantity', models.FloatField(default=0)),
                ('s_cost', models.FloatField(default=0)),
                ('s_cal', models.FloatField(default=0)),
                ('s_protein', models.FloatField(default=0)),
                ('s_fat', models.FloatField(default=0)),
                ('s_carbs', models.FloatField(default=0)),
                ('b_quantity', models.FloatField(default=None)),
                ('b_cost', models.FloatField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='RecepieIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_ingredient', to='mealplanner.FoodItem')),
                ('recepie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recepie', to='mealplanner.FoodItem')),
            ],
        ),
    ]
