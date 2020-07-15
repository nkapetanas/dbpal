from nltk.corpus import stopwords
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import re

from django.db import connection

TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'
HTML_TAGS_REGEX = '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

cursor = connection.cursor()

TABLE_SHEMA = 'dbpal'
TABLE_NAME = 'patients'
PLACEHOLDER_SIGN = '@'
DIAGNOSIS_COLUMN = 'diagnosis'
phrases_identifying_existence_of_numerical_values = ["age", "length of stay"]



def get_unique_db_columns():
    cursor.execute('''SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`
        WHERE `TABLE_SCHEMA`=\'''' + TABLE_SHEMA + '''\' AND `TABLE_NAME`=\'''' + TABLE_NAME + '''\';''')

    return cursor.fetchall()


def get_unique_column_values(column):
    cursor.execute('''SELECT DISTINCT( ''' + column + ''') AS ''' + column + ''' FROM 
            ''' + TABLE_NAME + ''';''')

    return cursor.fetchall()


def create_place_holders_from_db(unique_db_columns):
    placeholders = dict()
    for column in unique_db_columns:
        placeholders[column] = PLACEHOLDER_SIGN + column.upper()

    return placeholders


def get_n_grams(n, sentence):
    return ngrams(sentence.split(), n)

class Preprocessor:
    def __init__(self):
        self.unique_db_columns = get_unique_db_columns()
        self.placeholders = create_place_holders_from_db(self.unique_db_columns)
        self.diagnosis_values_list = get_unique_column_values(DIAGNOSIS_COLUMN)
        self.n_grams = get_n_grams()

    def clean_html(self, user_input):
        cleaner = re.compile(HTML_TAGS_REGEX)
        return re.sub(cleaner, '', user_input)

    def clean_users_input(self, user_input):
        html_cleaned_text = self.clean_html(user_input)
        tokens = word_tokenize(html_cleaned_text)
        words = [word for word in tokens if word.isalpha()]
        words = [w for w in words if not w in stop_words]
        stemmed = [porter.stem(word) for word in words]

def replace_numeric_constants_with_placeholders(user_input):

        user_input.replace('', '')
        pass
