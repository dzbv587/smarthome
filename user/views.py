from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from .serializers import UserDetailSerializer, MyTokenObtainPairSerializer, PasswordChangeSerializer

# Create your views here.

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    @action(methods=['post'], detail=True)
    def update_password(self, request, pk=None):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # 更新密码
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # 更新会话中的认证哈希，以防止会话中的用户被踢出
            # update_session_auth_hash(request, user)

            return Response({'detail': '密码修改成功。'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
