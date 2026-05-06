from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import LoginSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        next_url = request.query_params.get('next', '/api/auth/login/')
        accept_header = request.META.get('HTTP_ACCEPT', '')
        wants_json = 'application/json' in accept_header
        if not wants_json:
            return redirect(next_url)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny],
        url_path='login'
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {'detail': '아이디 또는 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)
        next_url = request.query_params.get('next', '/api/posts/')
        accept_header = request.META.get('HTTP_ACCEPT', '')
        wants_json = 'application/json' in accept_header
        if not wants_json:
            return redirect(next_url)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):
        logout(request)
        return Response({'detail': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)