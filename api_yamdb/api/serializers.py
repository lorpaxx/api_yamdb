from datetime import date
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Review, Comment, Category, Genre, Title
from users.models import User


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    username = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role', )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверка чтобы пользователь не мог добавить более одного отзыва."""
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        user = None
        if request and hasattr(request, 'user'):
            user = request.user
        kwargs = request.parser_context.get('kwargs')
        title_id = kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_exist = Review.objects.filter(
            author=user,
            title=title
        ).exists()
        if review_exist:
            raise serializers.ValidationError(
                'Нельзя добавлять более одного отзыва!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    '''
    Класс CategorySerializer для модели Category.
    '''
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    '''
    Класс GenreSerializer для модели Genre.
    '''
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    '''
    Класс TitleSerializer для модели Title.
    '''
    rating = serializers.SerializerMethodField(method_name='get_rating')
    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(many=False, required=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, title_obj):
        if title_obj.reviews.count() > 0:
            score = title_obj.reviews.aggregate(Avg('score'))
            return int(score.get('score__avg'))
        return None


class TitleEditSerializer(serializers.ModelSerializer):
    '''
    Класс TitleEditSerializer для редактирования модели Title.
    '''
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, value):
        now_year = date.today().year
        if value > now_year:
            raise serializers.ValidationError(
                f'{value} ещё не наступил!'
            )
        return value
