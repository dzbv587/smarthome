from datetime import datetime

from django.db import models


# Create your models here.

class Device(models.Model):
    """
    设备
    """
    category_choices = (
        ('light', '灯'),
        ('switch', '插座'),
        ('fan', '风扇'),
        ('window', '窗户'),
        ('curtain', '窗帘'),
        ('sensor', '传感器')
    )
    position_choices = (
        ('bedroom', '卧室'),
        ('livingroom', '客厅'),
        ('kitchen', '厨房')
    )
    name = models.CharField(max_length=20, unique=True, verbose_name='名字')
    topic = models.CharField(max_length=20, unique=True, verbose_name='主题')
    category = models.CharField(max_length=10,choices=category_choices, verbose_name='类别')
    position = models.CharField(max_length=10,choices=position_choices, verbose_name='位置')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Light(models.Model):
    """
    灯
    """
    status_choices = (
        ('on', '开'),
        ('off', '关')
    )
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE, help_text='设备')
    operate = models.CharField(max_length=50, verbose_name='操作')
    status = models.CharField(max_length=5,choices=status_choices, verbose_name='状态')
    lightness = models.IntegerField(verbose_name='亮度', null=True, blank=True)
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '灯'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.device.name} {self.status}'


class Switch(models.Model):
    """
    插座
    """
    status_choices = (
        ('on', '开'),
        ('off', '关')
    )
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE)
    operate = models.CharField(max_length=50, verbose_name='操作')
    status = models.CharField(max_length=5, choices=status_choices, verbose_name='状态')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '插座'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.device.name} {self.status}'


class Fan(models.Model):
    """
    风扇
    """
    status_choices = (
        ('on', '开'),
        ('one', '一档'),
        ('two', '二档'),
        ('three', '三档'),
        ('four', '四档'),
        ('off', '关')
    )
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE)
    operate = models.CharField(max_length=50, verbose_name='操作')
    status = models.CharField(max_length=5, choices=status_choices, verbose_name='状态')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '风扇'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.device.name} {self.status}'


class Window(models.Model):
    """
    窗户
    """
    status_choices = (
        ('on', '开'),
        ('off', '关')
    )
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE)
    operate = models.CharField(max_length=50, verbose_name='操作')
    status = models.CharField(max_length=5, choices=status_choices, verbose_name='状态')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '窗户'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.device.name} {self.status}'
        

class Curtain(models.Model):
    """
    窗帘
    """
    # status_choices = (
    #     ('on', '开'),
    #     ('off', '关'),
    #     ('pause', '暂停')
    # )
    # status = models.CharField(max_length=5, choices=status_choices, verbose_name='状态')
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE)
    operate = models.CharField(max_length=50, verbose_name='操作')
    status = models.IntegerField(verbose_name='状态')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    class Meta:
        verbose_name = '窗帘'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f'{self.device.name} {self.status}'


class Sensor(models.Model):
    """
    温湿度传感器
    """
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE)
    data = models.CharField(max_length=50, default="", verbose_name='数据')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    
    class Meta:
        verbose_name = '温湿度传感器'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f'{self.device.name}'


class Plan(models.Model):
    """
    条件计划
    """
    device = models.ForeignKey(Device, verbose_name='设备', on_delete=models.CASCADE, related_name='devices')
    sensor = models.ForeignKey(Device, verbose_name='传感器', on_delete=models.CASCADE)
    limit = models.IntegerField(verbose_name='阈值', null=True)
    operate = models.CharField(max_length=50, verbose_name='操作')
    active = models.BooleanField(default=True, verbose_name='活动')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '计划'
        verbose_name_plural = verbose_name

