from .models import Player, Team
from .serializers import PlayerSerializer, TeamSerializer, PlayerGetSerializer, TeamGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Display Players
class PlayerList(viewsets.ViewSet):
    permission_classes = [UserAdminPermission | UserContentCreatorPermission]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def list(self, request):
        players = Player.objects.all()
        serializer = PlayerGetSerializer(players, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        player = get_object_or_404(Player, pk=pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    def create(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            player = Player.objects.create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                nationality=serializer.validated_data['nationality'],
                role=serializer.validated_data['role'],
                birth_date=serializer.validated_data['birth_date'],
                height=serializer.validated_data['height'],
                description=serializer.validated_data['description'],
            )
            player.save()
            # player added succesfully
            return Response({"Success": "Player added succesfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a player
    def update(self, request, pk=None):
        player = get_object_or_404(player, pk=pk)
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
