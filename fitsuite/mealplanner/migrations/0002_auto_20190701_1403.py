# Generated by Django 2.2.2 on 2019-07-01 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealplanner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='b_cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='b_quantity',
            field=models.FloatField(),
        ),
    ]
