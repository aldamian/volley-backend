from .views import ChangePasswordView
from .user_views import Me, UserList, UserDetail
from .news_views import NewsList
from .player_views import PlayerList


from rest_framework.routers import DefaultRouter


app_name = 'api'


router = DefaultRouter()
router.register('me', Me, basename='me')
router.register('change_password', ChangePasswordView,
                basename='change_password')
router.register('users', UserList, basename='post')
router.register('users', UserDetail, basename='update')

router.register('news', NewsList, basename='post')
router.register('players', PlayerList, basename='post')


urlpatterns = router.urls
