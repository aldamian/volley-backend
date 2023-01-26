from .models import User, Trophy, File
from datetime import datetime
from .serializers import TrophySerializer, TrophyGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Trophies
class TrophyList(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Trophy.objects.all()
    serializer_class = TrophySerializer

    def list(self, request):
        trophies = Trophy.objects.all()
        serializer = TrophyGetSerializer(trophies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Trophy.objects.all()
        trophy = get_object_or_404(queryset, pk=pk)
        serializer = TrophyGetSerializer(trophy)
        return Response(serializer.data)


class TrophyCreate(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Trophy.objects.all()
    serializer_class = TrophySerializer

    def create(self, request):
        serializer = TrophySerializer(data=request.data)
        # perform validation checks

        # user = User.objects.get(id=request.user.id)
        # Add image url to trophy

        if serializer.is_valid():
            trophy = Trophy.objects.create(
                name=serializer.validated_data['name'],
                category=serializer.validated_data['category'],
                date=serializer.validated_data['date'],
            )

            trophy.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrophyDetail(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Trophy.objects.all()
    serializer_class = TrophySerializer

    def update(self, request, pk=None):
        trophy = get_object_or_404(Trophy, pk=pk)
        serializer = TrophySerializer(trophy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        trophy = get_object_or_404(Trophy, pk=pk)
        trophy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
