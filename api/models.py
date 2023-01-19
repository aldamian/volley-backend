from re import T
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, role, first_name, last_name,
                    **other_fields):

        if not email:
            raise ValueError(_('Users must have an email address.'))
        if not password:
            raise ValueError(_('Users must have a password.'))
        if not role:
            raise ValueError(
                _('Users must have Admin or Content Creator role.'))
        if not first_name:
            raise ValueError(_('Users must have a first name.'))
        if not last_name:
            raise ValueError(_('Users must have a last name.'))

        user = self.model(
            email=self.normalize_email(email),
            role=role.capitalize(),
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            **other_fields
        )

        user.set_password(password)  # takes care of the hashing
        user.save()
        return user

    def create_superuser(self, email, password, role, first_name, last_name,
                         **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, role, first_name, last_name,
                                **other_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class UserObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)

    ADMIN = _('Admin')
    CONTENT_CREATOR = _('Content Creator')

    USER_TYPE_CHOICES = [
        (ADMIN, _('Admin')),
        (CONTENT_CREATOR, _('Content Creator')),
    ]

    email = models.EmailField(
        max_length=200, null=False, blank=False, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    role = models.CharField(max_length=200, choices=USER_TYPE_CHOICES,
                            default=CONTENT_CREATOR, null=False, blank=False)

    img_url = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'role', 'first_name', 'last_name']

    objects = CustomUserManager()  # custom permission manager
    userObjects = UserObjects()  # custom manager

    class Meta:
        ordering = ('role',)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def get_role(self):
        return self.role

    def get_img_url(self):
        return self.img_url


class News(models.Model):

    POSTED = 'P'
    DRAFT = 'D'

    STATUS_CHOICES = [
        (POSTED, 'Posted'),
        (DRAFT, 'Draft')
    ]

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=False, blank=False, db_column='user_id')
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT,
                              null=False, blank=False)

    news_hashtag_ids = ArrayField(models.IntegerField(), null=True, blank=True)
    news_image_ids = ArrayField(models.IntegerField(), null=True, blank=True)
    news_video_ids = ArrayField(models.IntegerField(), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return str(self.user_id)

    def get_user_id(self):
        return self.user_id

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def get_status(self):
        return self.status

    def get_created_at(self):
        return self.created_at

    def get_published_at(self):
        return self.published_at


class NewsHashtag(models.Model):
    news_id = models.ForeignKey('News', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='news_id')
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.news_id)

    def get_name(self):
        return self.name


class NewsImage(models.Model):
    news_id = models.ForeignKey('News', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='news_id')
    img_url = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.news_id)

    def get_img_url(self):
        return self.img_url


class NewsVideo(models.Model):
    news_id = models.ForeignKey('News', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='news_id')
    video_url = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return str(self.news_id)

    def get_video_url(self):
        return self.video_url


class Team(models.Model):

    PLAYERS = 'P'
    JUNIORS = 'J'
    CADETS = 'C'
    HOPEFULS = 'H'

    CATEGORY_CHOICES = [
        (PLAYERS, 'Jucători'),
        (JUNIORS, 'Juniori'),
        (CADETS, 'Cadeți'),
        (HOPEFULS, 'Speranțe')
    ]

    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=PLAYERS,
                                null=False, blank=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category


class Player(models.Model):
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    nationality = models.CharField(max_length=200, null=False, blank=False)
    role = models.CharField(max_length=200, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    height = models.PositiveIntegerField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    team_id = models.ForeignKey('Team', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='team_id')

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_nationality(self):
        return self.nationality

    def get_role(self):
        return self.role

    def get_birth_date(self):
        return self.birth_date

    def get_height(self):
        return self.height

    def get_description(self):
        return self.description

    def get_team_id(self):
        return self.team_id


# it shouldn't have player_id
class Trophy(models.Model):
    team_id = models.ForeignKey('Team', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='team_id')
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    # added as optional
    img_url = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_team_id(self):
        return self.team_id

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_date(self):
        return self.date

    def get_img_url(self):
        return self.img_url


class RoleHistory(models.Model):
    player_id = models.ForeignKey('Player', on_delete=models.CASCADE, null=False, blank=False,
                                  db_column='player_id')
    team_id = models.ForeignKey('Team', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='team_id')
    role = models.CharField(max_length=200, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.player_id + " " + self.team_id + " " + self.role + " " + self.start_date + " " + self.end_date

    def get_player_id(self):
        return self.player_id

    def get_team_id(self):
        return self.team_id

    def get_role(self):
        return self.role

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


class Championship(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    prize = models.CharField(max_length=200, null=False, blank=False)
    category = models.CharField(max_length=200, null=False, blank=False)

    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_prize(self):
        return self.prize

    def get_category(self):
        return self.category

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


class Location(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country

    def get_city(self):
        return self.city


class Match(models.Model):
    championship_id = models.ForeignKey('Championship', on_delete=models.CASCADE, null=False, blank=False,
                                        db_column='championship_id')
    team_id = models.ForeignKey('Team', on_delete=models.CASCADE, null=False, blank=False,
                                db_column='team_id')
    rival_team_name = models.CharField(max_length=200, null=False, blank=False)
    rival_logo_url = models.CharField(max_length=200, null=False, blank=False)
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE, null=False, blank=False,
                                    db_column='location_id')
    team_points = models.PositiveIntegerField(null=False, blank=False)
    rival_points = models.PositiveIntegerField(null=False, blank=False)
    result = models.CharField(max_length=200, null=False, blank=False)
    watch_url = models.CharField(max_length=200, null=False, blank=False)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.championship_id + " " + self.team_id + " " + self.rival_team_name + " " + self.location + " " + self.team_points + " " + self.rival_points + " " + self.result

    def get_championship_id(self):
        return self.championship_id

    def get_team_id(self):
        return self.team_id

    def get_rival_team_name(self):
        return self.rival_team_name

    def get_rival_logo(self):
        return self.rival_logo

    def get_location(self):
        return self.location

    def get_team_points(self):
        return self.team_points

    def get_rival_points(self):
        return self.rival_points

    def get_result(self):
        return self.result

    def get_watch_url(self):
        return self.watch_url

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time


class Sponsor(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    link = models.CharField(max_length=200, null=False, blank=False)
    logo_url = models.CharField(max_length=200, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_link(self):
        return self.link

    def get_logo_url(self):
        return self.logo_url

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


# add connection to trophies in serializer
class ClubDetail(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    vision = models.TextField(null=False, blank=False)
    history = models.TextField(null=False, blank=False)

    # added as optional
    description = models.TextField(null=True, blank=True)
    img_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_vision(self):
        return self.vision

    def get_history(self):
        return self.history

    def get_description(self):
        return self.description

    def get_img_url(self):
        return self.img_url
