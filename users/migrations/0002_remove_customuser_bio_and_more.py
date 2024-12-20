# Generated by Django 5.1.2 on 2024-10-17 04:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='registration_code',
        ),
        migrations.AddField(
            model_name='customuser',
            name='blood_group',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AddField(
            model_name='customuser',
            name='current_ministry',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='designation',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='diocese',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='final_profession_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_profession_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nid_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='parish',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='passport_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='village',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('admin', 'Admin'), ('moderator', 'Moderator')], default='member', max_length=20),
        ),
        migrations.CreateModel(
            name='AcademicInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_name', models.CharField(max_length=100)),
                ('institution_name', models.CharField(max_length=200)),
                ('passing_year', models.IntegerField()),
                ('gpa', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApostolicInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('designation', models.CharField(max_length=100)),
                ('apostolate_name', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apostolic_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
