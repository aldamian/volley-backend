from .models import (
    User,
    News, NewsHashtag, NewsImage, NewsVideo,
    Team, Player,
    Trophy,
    RoleHistory,
    Championship,
    Location,
    Match,
    Sponsor,
    ClubDetail,
)

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import django.contrib.auth.password_validation as validate_password


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'role',
                  'first_name', 'last_name', 'img_url')


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role',
                  'first_name', 'last_name', 'img_url')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name',
                  'last_name', 'img_url', 'is_active')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('user_id', 'title', 'content',
                  'status', 'created_at', 'updated_at')


class NewsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'user_id', 'title', 'content',
                  'status', 'created_at', 'updated_at')


class NewsHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsHashtag
        fields = ('news_id', 'name')


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ('news_id', 'img_url')


class NewsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsVideo
        fields = ('news_id', 'video_url')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'category')


class TeamGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'category')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        # use the fields from Player model in models.py
        fields = ('team_id', 'first_name', 'last_name', 'nationality', 'role',
                  'birth_date', 'height', 'description')


class PlayerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'team_id', 'first_name', 'last_name', 'nationality', 'role',
                  'birth_date', 'height', 'description')


class TrophySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trophy
        fields = ('team_id', 'name', 'category', 'date')


class TrophyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trophy
        fields = ('id', 'team_id', 'name', 'category', 'date')


class RoleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHistory
        fields = ('player_id', 'team_id', 'role', 'start_date', 'end_date')


class RoleHistoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHistory
        fields = ('id', 'player_id', 'team_id',
                  'role', 'start_date', 'end_date')


class ChampionshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = ('name', 'location', 'prize',
                  'category', 'start_date', 'end_date')


class ChampionshipGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = ('id', 'name', 'location', 'prize',
                  'category', 'start_date', 'end_date')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'country', 'city')


class LocationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'country', 'city')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('championship_id', 'team_id', 'rival_team_name', 'rival_logo_url', 'location_id',
                  'team_points', 'rival_points', 'result', 'watch_url', 'start_time', 'end_time')


class MatchGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'championship_id', 'team_id', 'rival_team_name', 'rival_logo_url', 'location_id',
                  'team_points', 'rival_points', 'result', 'watch_url', 'start_time', 'end_time')


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('name', 'link', 'logo_url', 'start_date', 'end_date')


class SponsorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('id', 'name', 'link', 'logo_url', 'start_date', 'end_date')


class ClubDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDetail
        fields = ('name', 'vision', 'history', 'description', 'img_url')


class ClubDetailGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDetail
        fields = ('id', 'name', 'vision', 'history', 'description', 'img_url')


# admin can set new password for user
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('new_password', 'new_password2')

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("Passwords don't match.")

        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token['user_id'] = user.id
        token['role'] = user.role

        return token

    # check if user is active
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise serializers.ValidationError("User is not active.")

        return data
