from .views import ChangePasswordView
from .user_views import Me, UserList, UserDetail

from .player_views import PlayerList, PlayerCreate, PlayerDetail
from .match_views import MatchList, MatchCreate, MatchDetail
from .trophy_views import TrophyList, TrophyCreate, TrophyDetail
from .sponsor_views import SponsorList, SponsorDetail, SponsorCreate


from .news_views import NewsList, NewsCreate, NewsUpdate
from .file_views import FileList, FileDetail, FileCreate


from rest_framework.routers import DefaultRouter


app_name = 'api'


router = DefaultRouter()
router.register('me', Me, basename='me')
router.register('change_password', ChangePasswordView,
                basename='change_password')
router.register('users', UserList, basename='post')
router.register('users', UserDetail, basename='update')

router.register('players', PlayerList, basename='get')
router.register('players', PlayerCreate, basename='post')
router.register('players', PlayerDetail, basename='update')

router.register('matches', MatchList, basename='get')
router.register('matches', MatchCreate, basename='post')
router.register('matches', MatchDetail, basename='update')

router.register('trophies', TrophyList, basename='get')
router.register('trophies', TrophyCreate, basename='post')
router.register('trophies', TrophyDetail, basename='update')

router.register('sponsors', SponsorList, basename='get')
router.register('sponsors', SponsorCreate, basename='post')
router.register('sponsors', SponsorDetail, basename='update')

router.register('news', NewsList, basename='get')
router.register('news', NewsCreate, basename='post')
router.register('news', NewsUpdate, basename='update')

router.register('files', FileList, basename='get')
router.register('files', FileCreate, basename='post')
router.register('files', FileDetail, basename='update')

urlpatterns = router.urls
