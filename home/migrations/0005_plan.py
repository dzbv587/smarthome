# Generated by Django 4.2 on 2024-05-23 18:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_sensor_humidity_remove_sensor_temperature_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.IntegerField(null=True, verbose_name='阈值')),
                ('operate', models.CharField(max_length=50, verbose_name='操作')),
                ('active', models.BooleanField(default=True, verbose_name='活动')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.device', verbose_name='设备')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sensor', verbose_name='传感器')),
            ],
            options={
                'verbose_name': '计划',
                'verbose_name_plural': '计划',
            },
        ),
    ]
