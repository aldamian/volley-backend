from .models import News
from .serializers import NewsSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display News
class NewsList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    # create a new desk
    def create(self, request):
        serializer = NewsSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            news = News.objects.create(
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content'],
                status=serializer.validated_data['status'],
                user_id=serializer.validated_data['user_id'],
            )
            news.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a news
    def update(self, request, pk=None):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a news
    # to-do: can only be deleted by admin/ content creator
    def destroy(self, request, pk=None):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
