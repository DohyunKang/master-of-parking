# Generated by Django 5.0.4 on 2024-06-03 04:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(max_length=9)),
                ('entry_time', models.TimeField()),
                ('exit_time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timesets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'weekday')},
            },
        ),
    ]
