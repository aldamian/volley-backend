from .models import Player, File
from .serializers import PlayerSerializer, PlayerGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserContentCreatorPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Display Players
class PlayerList(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Player.objects.all()
    serializer_class = PlayerGetSerializer

    def list(self, request):
        players = Player.objects.all()
        serializer = PlayerGetSerializer(players, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        player = get_object_or_404(Player, pk=pk)
        serializer = PlayerGetSerializer(player)
        return Response(serializer.data)


class PlayerCreate(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def create(self, request):
        serializer = PlayerSerializer(data=request.data)

        # Use file upload

        if serializer.is_valid():
            player = Player.objects.create(
                name=serializer.validated_data['name'],
                type=serializer.validated_data['type'],
                status=serializer.validated_data['status'],
                description=serializer.validated_data['description'],
            )
            player.save()
            # player added succesfully
            return Response({"Success": "Player added succesfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerDetail(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def update(self, request, pk=None):
        player = get_object_or_404(Player, pk=pk)
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        player = get_object_or_404(Player, pk=pk)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
