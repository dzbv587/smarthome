# Generated by Django 4.2 on 2024-05-02 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_light_color_alter_light_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curtain',
            name='schedule',
        ),
        migrations.AlterField(
            model_name='curtain',
            name='status',
            field=models.IntegerField(verbose_name='状态'),
        ),
    ]
