from .models import (
    File,
    User,
    News,
    Player,
    Trophy,
    RoleHistory,
    Match,
    Sponsor,
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
                  'first_name', 'last_name')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name',
                  'last_name', 'is_active')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_url', 'file_type')


class FileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file_url', 'file_type')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'content', 'status', 'news_hashtags')


class NewsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('user_id', 'title', 'content', 'status',
                  'news_hashtags', 'created_at', 'updated_at')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('name', 'type', 'status', 'description', 'img_ids')


class PlayerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'type', 'status', 'description', 'img_ids')


class TrophySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trophy
        fields = ('name', 'category', 'date', 'img_url')


class TrophyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trophy
        fields = ('id', 'name', 'category', 'date', 'img_url')


class RoleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHistory
        fields = ('player_id', 'role', 'start_date', 'end_date')


# currently not used
class RoleHistoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleHistory
        fields = ('id', 'player_id', 'role',
                  'start_date', 'end_date')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('rival_team_name', 'rival_logo_id', 'location',
                  'team_points', 'rival_points', 'watch_url', 'match_day', 'match_time')


class MatchGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'rival_team_name', 'rival_logo_id', 'location',
                  'team_points', 'rival_points', 'watch_url', 'match_day', 'match_time')


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('name', 'link_id', 'description',
                  'sponsorship_period')


class SponsorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('id', 'name', 'link_id', 'description',
                  'sponsorship_period')


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
