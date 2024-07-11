import requests
import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .models import Device, Light, Switch, Window, Fan, Curtain, Sensor, Plan
from .serializers import (
    DevicesSerializer,
    LightSerializer,
    SwitchSerializer,
    WindowSerializer,
    FanSerializer,
    CurtainSerializer,
    SensorSerializer,
    PlanSerializer
)
from .const import TOPIC_MAP, BAFA_UID


# Create your views here.


class DeviceViewSet(viewsets.ModelViewSet):
    """
    设备
    """
    queryset = Device.objects.all()
    serializer_class = DevicesSerializer
    filterset_fields = ['position', 'category']

    def create(self, request, *args, **kwargs):
        """
        创建设备和主题
        """
        data = request.data.copy()
        data['topic'] = data['topic'] + TOPIC_MAP[data['category']]
        request_data = {
            'uid': BAFA_UID,
            'topic': data['topic'],
            'type': 1,
            'name': data['name']
        }
        res = requests.request('post', url='https://pro.bemfa.com/v1/addtopic', data=request_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        删除设备和主题
        """
        instance = self.get_object()
        request_data = {
            'uid': BAFA_UID,
            'topic': instance.topic,
            'type': 1
        }
        res = requests.request('post', url='https://pro.bemfa.com/v1/deltopic', data=request_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request_data = {
            'uid': BAFA_UID,
            'topic': instance.topic,
            'type': 1,
            'name': request.data.get('name')
        }
        res = requests.request('post', url='https://apis.bemfa.com/va/setName', data=request_data)
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class LightViewSet(viewsets.ModelViewSet):
    """
    灯
    """
    queryset = Light.objects.all()
    serializer_class = LightSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('limit'):
            queryset = queryset[:int(request.query_params.get('limit'))]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        request_data = {
            'uid': BAFA_UID,
            'topic': data['topic'],
            'type': 1,
            'msg': data['operate']
        }
        res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg', data=json.dumps(request_data),
                               headers={'Content-Type': 'application/json; charset=utf-8'})
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SwitchViewSet(viewsets.ModelViewSet):
    """
    插座
    """
    queryset = Switch.objects.all()
    serializer_class = SwitchSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('limit'):
            queryset = queryset[:int(request.query_params.get('limit'))]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        request_data = {
            'uid': BAFA_UID,
            'topic': data['topic'],
            'type': 1,
            'msg': data['operate']
        }
        res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg', data=json.dumps(request_data),
                               headers={'Content-Type': 'application/json; charset=utf-8'})
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WindowViewset(viewsets.ModelViewSet):
    """
    窗户
    """
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('limit'):
            queryset = queryset[:int(request.query_params.get('limit'))]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        request_data = {
            'uid': BAFA_UID,
            'topic': data['topic'],
            'type': 1,
            'msg': data['operate']
        }
        res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg', data=json.dumps(request_data),
                               headers={'Content-Type': 'application/json; charset=utf-8'})
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FanViewSet(viewsets.ModelViewSet):
    """
    风扇
    """
    queryset = Fan.objects.all()
    serializer_class = FanSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('limit'):
            queryset = queryset[:int(request.query_params.get('limit'))]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        request_data = {
            'uid': BAFA_UID,
            'topic': data['topic'],
            'type': 1,
            'msg': data['operate']
        }
        res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg', data=json.dumps(request_data),
                               headers={'Content-Type': 'application/json; charset=utf-8'})
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        status_map = {
            'on#1': 'one',
            'on#2': 'two',
            'on#3': 'three',
            'on#4': 'four',
            'off': 'off'
        }
        data['status'] = status_map[data['operate']]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CurtainViewSet(viewsets.ModelViewSet):
    """
    床帘
    """
    queryset = Curtain.objects.all()
    serializer_class = CurtainSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('limit'):
            queryset = queryset[:int(request.query_params.get('limit'))]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        request_data = {
            'uid': BAFA_UID,
            'topic': data['topic'],
            'type': 1,
            'msg': data['operate']
        }
        res = requests.request('post', url='https://apis.bemfa.com/va/postJsonMsg', data=json.dumps(request_data),
                               headers={'Content-Type': 'application/json; charset=utf-8'})
        res_data = json.loads(res.text)
        if res_data['code'] != 0:
            return Response({'detail': res_data['message']}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SensorViewSet(viewsets.ModelViewSet):
    """
    温湿度传感器
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('limit'):
            queryset = queryset[:int(request.query_params.get('limit'))]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device__id']
    ordering_fields = ['id']
