import json
from datetime import datetime, timedelta

import requests
from celery import shared_task

from home.models import Window, Device, Sensor, Light, Plan, Switch, Fan, Curtain
from .const import BAFA_UID


@shared_task
def sync_windows():
    windows = Device.objects.filter(category='window')
    for window in windows:
        first = Window.objects.filter(device_id=window.id).latest('id')
        first_timestamp = first.create_time.timestamp()
        params_data = {
            'uid': BAFA_UID,
            'topic': window.topic,
            'type': 1,
            'num': 5
        }
        res = requests.request('get', url='https://apis.bemfa.com/va/getmsg', params=params_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            continue
        res_data = res_data['data']
        for data in reversed(res_data):
            if data['unix'] - first_timestamp > 0:
                new = Window(device_id=window.id, operate=data['msg'], status='on' if 'on' in data['msg'] else 'off',
                             create_time=datetime.utcfromtimestamp(data['unix']) + timedelta(hours=8))
                new.save()


@shared_task
def sync_lights():
    lights = Device.objects.filter(category='light')
    for light in lights:
        first = Light.objects.filter(device_id=light.id).latest('id')
        first_timestamp = first.create_time.timestamp()
        params_data = {
            'uid': BAFA_UID,
            'topic': light.topic,
            'type': 1,
            'num': 5
        }
        res = requests.request('get', url='https://apis.bemfa.com/va/getmsg', params=params_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            continue
        res_data = res_data['data']
        for data in reversed(res_data):
            if data['unix'] - first_timestamp > 0:
                new = Light(device_id=light.id, operate=data['msg'], status='on' if 'on' in data['msg'] else 'off',
                            create_time=datetime.utcfromtimestamp(data['unix']) + timedelta(hours=8))
                new.save()


@shared_task
def sync_switchs():
    switchs = Device.objects.filter(category='switch')
    for switch in switchs:
        first = Switch.objects.filter(device_id=switch.id).latest('id')
        first_timestamp = first.create_time.timestamp()
        params_data = {
            'uid': BAFA_UID,
            'topic': switch.topic,
            'type': 1,
            'num': 5
        }
        res = requests.request('get', url='https://apis.bemfa.com/va/getmsg', params=params_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            continue
        res_data = res_data['data']
        for data in reversed(res_data):
            if data['unix'] - first_timestamp > 0:
                new = Switch(device_id=switch.id, operate=data['msg'], status='on' if 'on' in data['msg'] else 'off',
                             create_time=datetime.utcfromtimestamp(data['unix']) + timedelta(hours=8))
                new.save()


@shared_task
def sync_fans():
    fans = Device.objects.filter(category='fan')
    for fan in fans:
        first = Fan.objects.filter(device_id=fan.id).latest('id')
        first_timestamp = first.create_time.timestamp()
        params_data = {
            'uid': BAFA_UID,
            'topic': fan.topic,
            'type': 1,
            'num': 5
        }
        res = requests.request('get', url='https://apis.bemfa.com/va/getmsg', params=params_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            continue
        res_data = res_data['data']
        for data in reversed(res_data):
            if data['unix'] - first_timestamp > 0:
                if '1' in data['msg']:
                    status = 'one'
                elif '2' in data['msg']:
                    status = 'two'
                elif '3' in data['msg']:
                    status = 'three'
                elif '4' in data['msg']:
                    status = 'four'
                else:
                    status = 'off'
                new = Fan(device_id=fan.id, operate=data['msg'], status=status,
                          create_time=datetime.utcfromtimestamp(data['unix']) + timedelta(hours=8))
                new.save()


@shared_task
def sync_curtains():
    curtains = Device.objects.filter(category='curtain')
    for curtain in curtains:
        first = Curtain.objects.filter(device_id=curtain.id).latest('id')
        first_timestamp = first.create_time.timestamp()
        params_data = {
            'uid': BAFA_UID,
            'topic': curtain.topic,
            'type': 1,
            'num': 5
        }
        res = requests.request('get', url='https://apis.bemfa.com/va/getmsg', params=params_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            continue
        res_data = res_data['data']
        for data in reversed(res_data):
            if data['unix'] - first_timestamp > 0:
                new = Curtain(device_id=curtain.id, operate=data['msg'],
                              status=int(data['msg'][3:]) if data['msg'][3:] else 0,
                              create_time=datetime.utcfromtimestamp(data['unix']) + timedelta(hours=8))
                new.save()


@shared_task
def sync_sensors():
    sensors = Device.objects.filter(category='sensor')
    for sensor in sensors:
        first = Sensor.objects.filter(device_id=sensor.id).latest('id')
        first_timestamp = first.create_time.timestamp()
        params_data = {
            'uid': BAFA_UID,
            'topic': sensor.topic,
            'type': 1,
            'num': 5
        }
        res = requests.request('get', url='https://apis.bemfa.com/va/getmsg', params=params_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            continue
        res_data = res_data['data']
        for data in reversed(res_data):
            if data['unix'] - first_timestamp > 0:
                new = Sensor(device_id=sensor.id, data=data['msg'],
                             create_time=datetime.utcfromtimestamp(data['unix']) + timedelta(hours=8))
                new.save()
                if sensor.id == 19:
                    plan = Plan.objects.filter(sensor_id=sensor.id).first()
                    if plan.active:
                        if float(data['msg'][1:]) < plan.limit:
                            curtain = Device.objects.filter(id=plan.device_id).first()
                            curtain_text = Curtain.objects.filter(device_id=curtain.id).last()
                            if '100' not in curtain_text.operate:
                                print(1111111)
                                request_data = {
                                    'uid': BAFA_UID,
                                    'topic': curtain.topic,
                                    'type': 1,
                                    'msg': 'on#100'
                                }
                                res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg',
                                                       data=json.dumps(request_data),
                                                       headers={'Content-Type': 'application/json; charset=utf-8'})
                elif sensor.id == 22:
                    plan = Plan.objects.filter(sensor_id=sensor.id).first()
                    if plan.active:
                        if float(data['msg'][1:]) > plan.limit:
                            sound = Device.objects.filter(id=plan.device_id).first()
                            request_data = {
                                'uid': BAFA_UID,
                                'topic': sound.topic,
                                'type': 1,
                                'msg': 'on'
                            }
                            res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg',
                                                   data=json.dumps(request_data),
                                                   headers={'Content-Type': 'application/json; charset=utf-8'})
                elif sensor.id == 21:
                    plan = Plan.objects.filter(sensor_id=sensor.id).first()
                    if plan.active:
                        if float(data['msg'][1:]) == plan.limit:
                            window = Device.objects.filter(id=plan.device_id).first()
                            window_text = Window.objects.filter(device_id=window.device_id).last()
                            if 'off' not in window_text.operate:
                                request_data = {
                                    'uid': BAFA_UID,
                                    'topic': window.topic,
                                    'type': 1,
                                    'msg': 'off'
                                }
                                res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg',
                                                       data=json.dumps(request_data),
                                                       headers={'Content-Type': 'application/json; charset=utf-8'})
