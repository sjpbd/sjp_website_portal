# Generated by Django 5.1.2 on 2024-10-14 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='missiontype',
            name='icon',
            field=models.CharField(default='fas fa-map-marker-alt', max_length=50),
        ),
    ]