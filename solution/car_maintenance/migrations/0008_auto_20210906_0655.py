# Generated by Django 3.2.7 on 2021-09-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_maintenance', '0007_alter_trip_distance_travelled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='gas_capacity',
            field=models.FloatField(default=55),
        ),
        migrations.AlterField(
            model_name='car',
            name='gas_count',
            field=models.FloatField(default=55),
        ),
    ]
