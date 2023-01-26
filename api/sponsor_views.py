from .models import User, Sponsor
from datetime import datetime
from .serializers import SponsorSerializer, SponsorGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


class SponsorList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

    def list(self, request):
        sponsors = Sponsor.objects.all()
        serializer = SponsorGetSerializer(sponsors, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SponsorSerializer(data=request.data)
        # perform validation checks

        # user = User.objects.get(id=request.user.id)

        if serializer.is_valid():
            sponsor = Sponsor.objects.create(
                user_id=request.user.id,
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content'],
                status=serializer.validated_data['status'],
                sponsor_hastags=serializer.validated_data['sponsor_hastags'],
            )

            sponsor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a news

    def update(self, request, pk=None):
        sponsor = get_object_or_404(Sponsor, pk=pk)
        serializer = SponsorSerializer(sponsor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sponsor = get_object_or_404(Sponsor, pk=pk)
        sponsor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
