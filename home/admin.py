from django.contrib import admin

from .models import Device, Light, Switch, Fan, Window, Curtain, Sensor
# Register your models here.

admin.site.register(Device)
admin.site.register(Light)
admin.site.register(Sensor)
admin.site.register(Switch)
admin.site.register(Fan)
admin.site.register(Window)
admin.site.register(Curtain)
