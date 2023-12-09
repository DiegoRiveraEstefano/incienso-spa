from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer, UserWriteSerializer, UserLoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data.get('password'))
            user.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def create(self, request, *args, **kwargs):
        serialized_user = UserWriteSerializer(data=request.data)

        if not serialized_user.is_valid(raise_exception=False):
            return redirect('user-register-form')

        user = User.objects.create_user(
            is_admin=False,
            **serialized_user.data
        )
        user.save()

        return redirect('user-login-form')

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serialized_user = UserLoginSerializer(data=request.data)
        if not serialized_user.is_valid(raise_exception=False):
            return redirect('user-login-form')

        user = authenticate(username=serialized_user.data['username'], password=serialized_user.data['password'])
        if user:
            login(request, user)
            return redirect('user-profile')

        return redirect('user-login-form')

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated, ])
    def profile(self, request):
        return Response(
            {'user': request.user}, status=status.HTTP_200_OK,
            template_name='views/user/user_profile.html'
        )

    @action(methods=['GET'], detail=False, permission_classes=[AllowAny, ], url_name='login-form')
    def login_form(self, request):
        serializer = UserLoginSerializer()
        return Response(
            {'serializer': serializer},
            status=status.HTTP_200_OK,
            template_name='views/user/user_login.html'
        )

    @action(methods=['GET'], detail=False, permission_classes=[AllowAny, ], url_name='register-form')
    def register_form(self, request):
        serializer = UserWriteSerializer()
        return Response(
            {'serializer': serializer},
            status=status.HTTP_200_OK,
            template_name='views/user/user_register.html'
        )


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data.get('password'))
            user.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        if not self.request:
            return User.objects.none()

        if self.request.user.is_staff:
            return self.queryset
        return User.objects.filter(username=self.request.user.username)

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ], url_name='login')
    def login(self, request: Request):
        serialized_user = UserLoginSerializer(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        user = serialized_user.save
        token: Token = get_object_or_404(Token, user=user)
        return Response(
            data={'token': token.key},
            status=200
        )