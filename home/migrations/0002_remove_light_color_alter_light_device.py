# Generated by Django 4.2 on 2024-05-01 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='light',
            name='color',
        ),
        migrations.AlterField(
            model_name='light',
            name='device',
            field=models.ForeignKey(help_text='设备', on_delete=django.db.models.deletion.CASCADE, to='home.device', verbose_name='设备'),
        ),
    ]
