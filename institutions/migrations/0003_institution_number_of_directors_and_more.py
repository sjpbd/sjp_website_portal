# Generated by Django 5.1.2 on 2024-10-28 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='number_of_directors',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='number_of_formees',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='administration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='employees',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='grades',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='office_staff',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='ownership',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='students',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='teachers',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
