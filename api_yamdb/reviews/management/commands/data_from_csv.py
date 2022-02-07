import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

from csv import DictReader
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Genre, Title, Genre_Title,
    User,
    Review, Comment,
)

from api_yamdb.settings import BASE_DIR

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    f'{__name__}.log',
    encoding='utf-8',
    mode='w',
)
logger.addHandler(handler)
formatter = logging.Formatter(
    '[%(asctime)s]-[%(module)s]-[%(funcName)s]-[%(levelname)s]-%(message)s'
)
handler.setFormatter(formatter)

LOG_STATUS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'error': logging.ERROR,
    'default': logging.ERROR
}


class Command(BaseCommand):
    help = 'Копирование данных из csv'
    shift_path = os.path.join(BASE_DIR, 'static')
    shift_path = os.path.join(shift_path, 'data')

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '-log_level', type=str,
            help='Режим логгирования'
        )

    def handle(self, *args, **kwargs):
        '''
        Основная функция выполнения команды.
        '''
        print('start inserts')
        log_level = kwargs.get('log_level')
        print('log_level', log_level)
        if log_level and log_level.lower() in (LOG_STATUS):
            logger.setLevel(LOG_STATUS[log_level.lower()])
        else:
            logger.setLevel(LOG_STATUS['default'])
        self.insert_categories()
        self.insert_genres()
        self.insert_titles()
        self.insert_genge_titles()
        self.insert_users()
        self.insert_reviews()
        self.insert_comments()
        print('stop inserts')

    def insert_categories(self):
        '''
        Вставка данных в модель Category.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'category.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    Category.objects.create(**row)
                    logger.info('row inserts in database')
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')

    def insert_genres(self):
        '''
        Вставка данных в модель Genre.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'genre.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    Genre.objects.create(**row)
                    logger.info('row inserts in database')
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')

    def insert_titles(self):
        '''
        Вставка данных в модель Title.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'titles.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    num_category = int(row.pop('category'))
                    logger.debug('num_category: ' + str(num_category))
                    category = Category.objects.get(pk=num_category)
                    logger.debug(category)
                    if category:
                        Title.objects.create(category=category, **row)
                        logger.info('row inserts in database')
                    else:
                        logger.error(
                            'category ' + str(num_category) + ' does not exist'
                        )
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')

    def insert_genge_titles(self):
        '''
        Вставка данных в модель Genre_Title.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'genre_title.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    genre_id = int(row.pop('genre_id'))
                    logger.debug('genre_id: ' + str(genre_id))
                    genre = Genre.objects.get(pk=genre_id)
                    logger.debug(genre)
                    title_id = int(row.pop('title_id'))
                    logger.debug('title_id: ' + str(title_id))
                    title = Title.objects.get(pk=title_id)
                    logger.debug(title)
                    if all((genre, title)):
                        Genre_Title.objects.create(
                            genre=genre, title=title, **row)
                        logger.info('row inserts in database')
                    else:
                        logger.error("row doesn't insert")
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')

    def insert_users(self):
        '''
        Вставка данных в модель User.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'users.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    User.objects.create(**row)
                    logger.info('row inserts in database')
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')

    def insert_reviews(self):
        '''
        Вставка данных в модель Review.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'review.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    format_dt = '%Y-%m-%dT%H:%M:%S.%fZ'
                    logger.debug(f'format_dt: {format_dt}')
                    dt = datetime.datetime.strptime(
                        row.pop('pub_date'), format_dt)
                    logger.debug(dt)
                    title_id = int(row.pop('title_id'))
                    logger.debug(f'title_id: {title_id}')
                    title = Title.objects.get(pk=title_id)
                    logger.debug(title)
                    author_id = int(row.pop('author'))
                    logger.debug(f'author_id: {author_id}')
                    author = User.objects.get(pk=author_id)
                    logger.debug(author)
                    id = row.pop('id')
                    logger.debug(f'id: {id}')
                    text = row.pop('text')
                    logger.debug(f'text: {text}')
                    score = row.pop('score')
                    logger.debug(f'score: {score}')
                    if all((title, author, dt, text, score, id)):
                        Review.objects.create(
                            title=title, author=author, id=id,
                            text=text, score=score, pub_date=dt)
                        logger.info('row inserts in database')
                    else:
                        logger.error("row doesn't insert")
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')

    def insert_comments(self):
        '''
        Вставка данных в модель Comment.
        '''
        logger.info('====START====')
        filename = os.path.join(self.shift_path, 'comments.csv')
        logger.debug('filename')
        logger.debug(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            csvdict = DictReader(f)
            for row in csvdict:
                logger.info(row)
                try:
                    format_dt = '%Y-%m-%dT%H:%M:%S.%fZ'
                    logger.debug(f'format_dt: {format_dt}')
                    dt = datetime.datetime.strptime(
                        row.pop('pub_date'), format_dt)
                    logger.debug(dt)
                    review_id = int(row.pop('review_id'))
                    logger.debug(f'review_id: {review_id}')
                    review = Review.objects.get(pk=review_id)
                    logger.debug(review)
                    author_id = int(row.pop('author'))
                    logger.debug(f'author_id: {author_id}')
                    author = User.objects.get(pk=author_id)
                    logger.debug(author)
                    if all((review, author, dt)):
                        Comment.objects.create(
                            review=review, author=author, pub_date=dt, **row)
                        logger.info('row inserts in database')
                    else:
                        logger.error("row doesn't insert")
                except Exception as err:
                    logger.error(err)
        logger.info('====STOP====')
