from .permissions import UserAdminPermission
from .models import User
from .serializers import MyTokenObtainPairSerializer, ChangePasswordSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


# API endpoints
class getRoutesView(APIView):
    permission_classes = [AllowAny]

    # TO DO
    # Define routes to urls.py

    routes = [
        {'GET': '/swagger', 'description': 'API Documentation'},
        {'GET': '/admin', 'description': 'Admin Dashboard'},
        {'GET': '/api/users'},
        {'GET': '/api/users/<int:pk>'},
        {'GET': '/api/users/<int:pk>/requests'},

        {'GET': '/api/players'},
        {'GET': '/api/players/<int:pk>'},

        {'GET': '/api/matches'},
        {'GET': '/api/matches/<int:pk>'},

        {'GET': '/api/trophies'},
        {'GET': '/api/trophies/<int:pk>'},

        {'GET': '/api/sponsors'},
        {'GET': '/api/sponsors/<int:pk>'},

        {'GET': '/api/news'},
        {'GET': '/api/news/<int:pk>'},

        {'POST': '/api/token'},
        {'POST': '/api/token/refresh'},
        {'POST': '/api/token/blacklist'},
        {'POST': '/api/me'},
    ]

    def get(self, request):
        if request.method == 'GET':
            return Response(self.routes)


class ChangePasswordView(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def post(self, request, pk=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(pk=pk)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
