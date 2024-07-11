from rest_framework import serializers
from .models import Device, Light, Switch, Fan, Window, Curtain, Sensor, Plan


class DevicesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Device model
    """

    class Meta:
        model = Device
        fields = ('id', 'url', 'name', 'topic', 'category', 'position')


class LightSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Light model
    """

    class Meta:
        model = Light
        fields = ('id', 'url', 'device', 'status', 'operate', 'lightness', 'create_time')


class SwitchSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Switch model
    """

    class Meta:
        model = Switch
        fields = ('id', 'url', 'device', 'operate', 'status', 'create_time')


class FanSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Fan model
    """

    class Meta:
        model = Fan
        fields = ('id', 'url', 'device', 'operate', 'status', 'create_time')


class WindowSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Windows model
    """

    class Meta:
        model = Window
        fields = ('id', 'url', 'device', 'operate', 'status', 'create_time')


class CurtainSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Curtain model
    """

    class Meta:
        model = Curtain
        fields = ('id', 'url', 'device', 'operate', 'status', 'create_time')


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Sensor model
    """

    class Meta:
        model = Sensor
        fields = ('id', 'url', 'device', 'data', 'create_time')


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'url', 'device', 'sensor', 'limit', 'operate', 'active', 'create_time')
