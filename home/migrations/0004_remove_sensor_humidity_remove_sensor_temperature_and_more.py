# Generated by Django 4.2 on 2024-05-23 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_curtain_schedule_alter_curtain_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='humidity',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='temperature',
        ),
        migrations.AddField(
            model_name='sensor',
            name='data',
            field=models.CharField(default='', max_length=50, verbose_name='数据'),
        ),
    ]
