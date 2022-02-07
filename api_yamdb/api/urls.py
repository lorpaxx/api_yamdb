from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import (
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UsersViewSet,
    send_confirmation_code,
    get_token
)


app_name = 'api'

router = DefaultRouter()
router.register('v1/users', UsersViewSet, basename='user')
router.register('v1/titles', TitleViewSet)
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet
)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)

urlpatterns = [
    path(
        'v1/auth/signup/',
        send_confirmation_code,
        name='SendConfirmationCode'
    ),
    path('v1/auth/token/', get_token, name='GetToken'),
    path('', include(router.urls)),
]
