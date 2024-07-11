from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'name', 'email', 'mobile')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录认证
    """
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("用户名和密码不能为空")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("用户名或密码不正确")
        refresh = self.get_token(user)
        data = {"userId": user.id, "token": str(refresh.access_token), "refresh": str(refresh)}
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError('密码错误')
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError('新密码不能与旧密码相同')
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
