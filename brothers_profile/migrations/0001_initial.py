# Generated by Django 5.1.2 on 2024-10-15 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=200)),
                ('grade', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, default='img/default_avatar_profile.jpg', null=True, upload_to='profile_pictures/')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=100)),
                ('mobile_number', models.CharField(blank=True, max_length=20)),
                ('email_address', models.EmailField(blank=True, max_length=50)),
                ('father_name', models.CharField(blank=True, max_length=100)),
                ('mother_name', models.CharField(blank=True, max_length=100)),
                ('parish_name', models.CharField(blank=True, max_length=100)),
                ('village_name', models.CharField(blank=True, max_length=100)),
                ('dist_name', models.CharField(blank=True, max_length=100)),
                ('blood_group', models.CharField(blank=True, max_length=5)),
                ('passport_number', models.CharField(blank=True, max_length=20)),
                ('nid_number', models.CharField(blank=True, max_length=20)),
                ('title', models.CharField(default='Religious Brother', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('authors', models.CharField(max_length=200)),
                ('journal', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('doi', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReligiousInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_joining', models.DateField(blank=True, null=True)),
                ('date_of_first_vows', models.DateField(blank=True, null=True)),
                ('date_of_final_vows', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=50)),
                ('url', models.URLField()),
            ],
        ),
    ]
