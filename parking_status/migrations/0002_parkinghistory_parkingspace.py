# Generated by Django 5.0.7 on 2024-08-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_status', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_text', models.CharField(max_length=20)),
                ('index', models.IntegerField()),
                ('entry_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_text', models.CharField(blank=True, max_length=20, null=True)),
                ('index', models.IntegerField()),
                ('entry_time', models.DateTimeField(blank=True, null=True)),
                ('exit_time', models.DateTimeField(blank=True, null=True)),
                ('is_occupied', models.BooleanField(default=False)),
            ],
        ),
    ]