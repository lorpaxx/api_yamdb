from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination

from api_yamdb import settings

from users.models import User
from reviews.models import Review, Comment, Category, Genre, Title
from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserEmailSerializer,
    ConfirmationCodeSerializer,
    UserSerializer,
    MeSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleEditSerializer
)
from api.permissions import (
    IsAdministrator,
    AuthorStaffOrReadOnly,
    IsAdministratorOrReadOnly
)
from api.filters import TitleFilter


USERNAME_ME = 'me'


@api_view(('POST',))
def send_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    if username == USERNAME_ME:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)

    mail_subject = 'Код подтверждения для регистрации в YaMDB'
    message = f'Ваш {mail_subject.lower()}: {confirmation_code}'
    recipient_email = email
    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        (recipient_email,),
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(
        'Неправильный код подтверждения',
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdministrator)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=('patch', 'get'),
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        url_path=USERNAME_ME,
        url_name=USERNAME_ME
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = MeSerializer(user)
        if self.request.method != 'PATCH':
            return Response(serializer.data)
        serializer = MeSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetUserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdministrator)
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorStaffOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorStaffOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    '''
    Класс CategoryViewSet для модели Category.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdministratorOrReadOnly,)
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = ('name',)


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    '''
    Класс GenreViewSet для модели Genre.
    '''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdministratorOrReadOnly,)
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    '''
    Класс TitleViewSet для модели Title.
    '''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdministratorOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = TitleFilter

    def create(self, request, *args, **kwargs):
        serializer = TitleEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        output_serializer = TitleSerializer(serializer.instance)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = TitleEditSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        output_serializer = TitleSerializer(instance)
        return Response(output_serializer.data)
