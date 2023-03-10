from .models import User, News
from datetime import datetime
from .serializers import NewsSerializer, NewsGetSerializer
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
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request):
        news = News.objects.all()
        serializer = NewsGetSerializer(news, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = News.objects.all()
        news = get_object_or_404(queryset, pk=pk)
        serializer = NewsGetSerializer(news)
        return Response(serializer.data)


class NewsCreate(viewsets.ViewSet):
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def create(self, request):
        serializer = NewsSerializer(data=request.data)
        # perform validation checks

        # user = User.objects.get(id=request.user.id)

        if serializer.is_valid():
            news = News.objects.create(
                user_id=request.user.id,
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content'],
                status=serializer.validated_data['status'],
                news_hastags=serializer.validated_data['news_hastags'],
            )

            # do we do this from the front end?
            if news.status == 'Posted':
                news.published_at = datetime.now()

            else:
                news.published_at = None

            news.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsUpdate(viewsets.ViewSet):
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # update updated_at field
    def update(self, request, pk=None):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
