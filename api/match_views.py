from .models import User, Match, File
from datetime import datetime
from .serializers import MatchSerializer, MatchGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Matches
class MatchList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def list(self, request):
        matches = Match.objects.all()
        serializer = MatchGetSerializer(matches, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MatchSerializer(data=request.data)
        # perform validation checks

        # user = User.objects.get(id=request.user.id)

        if serializer.is_valid():
            match = Match.objects.create(
                rival_team_name=serializer.validated_data['rival_team_name'],
                # add logic for rival_logo_id. Upload image and save id to db.
                # this is incorrect
                rival_logo_id=serializer.validated_data['rival_logo_id'],
                location=serializer.validated_data['location'],
                team_points=serializer.validated_data['team_points'],
                rival_points=serializer.validated_data['rival_points'],
                watch_url=serializer.validated_data['watch_url'],
                match_day=serializer.validated_data['match_day'],
                match_time=serializer.validated_data['match_time'],
            )
            match.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        match = get_object_or_404(Match, pk=pk)
        serializer = MatchSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        match = get_object_or_404(Match, pk=pk)
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        match = get_object_or_404(Match, pk=pk)
        serializer = MatchGetSerializer(match)
        return Response(serializer.data)
