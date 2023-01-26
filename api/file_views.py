from .models import User, File
from datetime import datetime
from .serializers import FileSerializer, FileGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Add connection to S3 for image and video hosting.
class FileList(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def list(self, request):
        files = File.objects.all()
        serializer = FileGetSerializer(files, many=True)
        return Response(serializer.data)


class FileCreate(viewsets.ViewSet):
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def create(self, request):
        serializer = FileSerializer(data=request.data)

        if serializer.is_valid():
            file = File.objects.create(
                file_url=serializer.validated_data['file_url'],
                file_type=serializer.validated_data['file_type'],
            )

            file.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetail(viewsets.ViewSet):
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = File.objects.all()
    serializer_class = FileGetSerializer

    def retrieve(self, request, pk=None):
        file = get_object_or_404(File, pk=pk)
        serializer = FileGetSerializer(file)
        return Response(serializer.data)

    def update(self, request, pk=None):
        file = get_object_or_404(File, pk=pk)
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        file = get_object_or_404(File, pk=pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
