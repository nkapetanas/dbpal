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

TABLE_SCHEMA = 'dbpal'
TABLE_NAME = 'patients'
PLACEHOLDER_SIGN = '@'
DIAGNOSIS_COLUMN = 'diagnosis'
AGE = 'age'
LENGTH_OF_STAY = 'length of stay'
phrases_identifying_existence_of_numerical_values = [AGE, LENGTH_OF_STAY]


def get_unique_db_columns():
    cursor.execute('''SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`
        WHERE `TABLE_SCHEMA`=\'''' + TABLE_SCHEMA + '''\' AND `TABLE_NAME`=\'''' + TABLE_NAME + '''\';''')

    return cursor.fetchall()


def get_unique_column_values(column):
    cursor.execute('''SELECT DISTINCT( ''' + column + ''') AS ''' + column + ''' FROM 
            ''' + TABLE_NAME + ''';''')

    return cursor.fetchall()


def create_place_holders_from_db(unique_db_columns):
    placeholders = dict()
    for column in unique_db_columns:
        placeholders[column] = PLACEHOLDER_SIGN + column[0].upper()

    return placeholders


def get_n_grams(n, sentence):
    return ngrams(sentence.split(), n)


class Preprocessor:
    def __init__(self):
        self.unique_db_columns = get_unique_db_columns()
        self.placeholders = create_place_holders_from_db(self.unique_db_columns)
        self.diagnosis_values_list = get_unique_column_values(DIAGNOSIS_COLUMN)

    def clean_html(self, user_input):
        cleaner = re.compile(HTML_TAGS_REGEX)
        return re.sub(cleaner, '', user_input)

    def clean_users_input(self, user_input):
        html_cleaned_text = self.clean_html(user_input)
        tokens = word_tokenize(html_cleaned_text)
        stemmed_words = [porter.stem(word) for word in tokens]
        return " ".join(stemmed_words)

    def replace_numeric_constants_with_placeholders(self, user_input):
        placeholders = dict()
        constants_detected = dict()

        placeholders[AGE] = "@AGE"
        placeholders[LENGTH_OF_STAY] = "@LENGTH_OF_STAY"

        constants_detected[AGE] = 0
        constants_detected[LENGTH_OF_STAY] = 0

        splitted_user_input = user_input.split()
        for phrase in phrases_identifying_existence_of_numerical_values:
            if phrase in user_input:
                constants_detected[phrase] = constants_detected[phrase] + 1

        if constants_detected[AGE] > 0 and constants_detected[LENGTH_OF_STAY] > 0:
            age_index = user_input.find(AGE)
            length_of_stay_index = user_input.find(LENGTH_OF_STAY)

            for word in splitted_user_input:
                if word.isnumeric():
                    word_index = user_input.find(word)
                    if age_index < word_index < length_of_stay_index:
                        user_input = user_input.replace(word, placeholders[AGE])

                    elif length_of_stay_index < word_index < age_index:
                        user_input = user_input.replace(word, placeholders[LENGTH_OF_STAY])

                    elif word_index > age_index and word_index > length_of_stay_index > age_index:
                        user_input = user_input.replace(word, placeholders[LENGTH_OF_STAY])

                    else:
                        user_input = user_input.replace(word, placeholders[AGE])

        elif constants_detected[AGE] > 0:
            for word in splitted_user_input:
                if word.isnumeric():
                    user_input = user_input.replace(word, placeholders[AGE])

        elif constants_detected[LENGTH_OF_STAY] > 0:
            for word in splitted_user_input:
                if word.isnumeric():
                    user_input = user_input.replace(word, placeholders[LENGTH_OF_STAY])

        return user_input
