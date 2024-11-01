# Generated by Django 5.1.2 on 2024-10-15 06:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brothers_profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='experience',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='brothers_profile.profile'),
        ),
        migrations.AddField(
            model_name='academicrecord',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_records', to='brothers_profile.profile'),
        ),
        migrations.AddField(
            model_name='publication',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='brothers_profile.profile'),
        ),
        migrations.AddField(
            model_name='religiousinfo',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='brothers_profile.profile'),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='brothers_profile.profile'),
        ),
    ]
