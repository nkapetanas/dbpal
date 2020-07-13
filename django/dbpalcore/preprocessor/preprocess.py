# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
# from nltk import ngrams
from django.db import connection, transaction

from dbpalapi.models import Patients

TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'
# stop = set(stopwords.words('english'))
# stemmer = SnowballStemmer('english')
cursor = connection.cursor()

TABLE_SHEMA = 'dbpal'
TABLE_NAME = 'patients'
PLACEHOLDER_SIGN = '@'


def get_unique_db_columns():
    cursor.execute('''SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`
        WHERE `TABLE_SCHEMA`=\'''' + TABLE_SHEMA + '''\' AND `TABLE_NAME`=\'''' + TABLE_NAME + '''\';''')

    return cursor.fetchall()


def create_place_holders_from_db(unique_db_columns):
    placeholders = list()
    for column in unique_db_columns:
        placeholders.append(PLACEHOLDER_SIGN + column.upper())

    return placeholders


def get_n_grams(n, list_of_words):
    list_of_ngrams = list()
    for word in list_of_words:
        # list_of_ngrams.append(ngrams(word.split(), n))
        list_of_ngrams.append(n)


class Preprocessor:
    def __init__(self):
        self.unique_db_columns = get_unique_db_columns()
        self.placeholders = create_place_holders_from_db(self.unique_db_columns)
        self.n_grams = get_n_grams()

    def clean_users_input(self, user_input):
        pass
