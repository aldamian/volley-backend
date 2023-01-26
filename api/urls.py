from .views import ChangePasswordView
from .user_views import Me, UserList, UserDetail

from .player_views import PlayerList
from .match_views import MatchList
from .trophy_views import TrophyList
from .sponsor_views import SponsorList


from .news_views import NewsList
from .file_views import FileList


from rest_framework.routers import DefaultRouter


app_name = 'api'


router = DefaultRouter()
router.register('me', Me, basename='me')
router.register('change_password', ChangePasswordView,
                basename='change_password')
router.register('users', UserList, basename='post')
router.register('users', UserDetail, basename='update')

router.register('players', PlayerList, basename='post')
router.register('matches', MatchList, basename='post')
router.register('trophies', TrophyList, basename='post')
router.register('sponsors', SponsorList, basename='post')

router.register('news', NewsList, basename='post')


urlpatterns = router.urls
