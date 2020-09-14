from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import re

from django.db import connection

TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'
HTML_TAGS_REGEX = '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'
porter = PorterStemmer()

cursor = connection.cursor()

TABLE_SCHEMA = 'dbpal'
TABLE_NAME = 'patients'
PLACEHOLDER_SIGN = '@'
DIAGNOSIS_COLUMN = 'diagnosis'
FIRST_NAME_COLUMN = 'first_name'
LAST_NAME_COLUMN = 'last_name'
FIRST_NAME_PLACEHOLDER = 'first'
LAST_NAME_PLACEHOLDER = 'last'
GENDER = 'gender'
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
        placeholders[column[0]] = PLACEHOLDER_SIGN + column[0].upper()

    placeholders["first_name"] = "@FIRST"
    placeholders["last_name"] = "@LAST"
    for key, value in placeholders.items():
        print(key)
        print(value)

    return placeholders


def get_processed_values(db_values):
    values_list = list()

    for value in db_values:
        value = porter.stem(value[0])
        values_list.append(value.lower())

    return values_list


class Preprocessor:
    def __init__(self):
        self.unique_db_columns = get_unique_db_columns()
        self.placeholders = create_place_holders_from_db(self.unique_db_columns)

        unique_diagnosis_values = get_unique_column_values(DIAGNOSIS_COLUMN)
        self.diagnosis_values_list = get_processed_values(unique_diagnosis_values)

        unique_first_name_values = get_unique_column_values(FIRST_NAME_COLUMN)
        self.first_name_values_list = get_processed_values(unique_first_name_values)

        unique_last_name_values = get_unique_column_values(LAST_NAME_COLUMN)
        self.last_name_values_list = get_processed_values(unique_last_name_values)

        self.gender = ["male", "femal"]
        self.replaced_constants = dict()

    def clean_html(self, user_input):
        cleaner = re.compile(HTML_TAGS_REGEX)
        return re.sub(cleaner, '', user_input)

    def clean_users_input(self, user_input):
        html_cleaned_text = self.clean_html(user_input)
        tokens = word_tokenize(html_cleaned_text)
        stemmed_words = [porter.stem(word) for word in tokens]
        return " ".join(stemmed_words)

    def replace_constants_with_placeholders(self, user_input):
        self.replaced_constants = dict()

        if user_input is None:
            return ""

        splitted_user_input = user_input.split()

        for word in splitted_user_input:
            if word in self.first_name_values_list:
                user_input = user_input.replace(word, self.placeholders[FIRST_NAME_COLUMN])
                self.replaced_constants[word] = self.placeholders[FIRST_NAME_COLUMN]

            elif word in self.last_name_values_list:
                user_input = user_input.replace(word, self.placeholders[LAST_NAME_COLUMN])
                self.replaced_constants[word] = self.placeholders[LAST_NAME_COLUMN]

            elif word in self.gender:
                user_input = user_input.replace(word, self.placeholders[GENDER])
                self.replaced_constants[word] = self.placeholders[GENDER]

            elif word in self.diagnosis_values_list:
                user_input = user_input.replace(word, self.placeholders[DIAGNOSIS_COLUMN])
                self.replaced_constants[word] = self.placeholders[DIAGNOSIS_COLUMN]
        return user_input

    def replace_numeric_constants_with_placeholders(self, user_input):
        if user_input is None:
            return ""

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
                        self.replaced_constants[word] = placeholders[AGE]

                    elif length_of_stay_index < word_index < age_index:
                        user_input = user_input.replace(word, placeholders[LENGTH_OF_STAY])
                        self.replaced_constants[word] = placeholders[LENGTH_OF_STAY]

                    elif word_index > age_index and word_index > length_of_stay_index > age_index:
                        user_input = user_input.replace(word, placeholders[LENGTH_OF_STAY])
                        self.replaced_constants[word] = placeholders[LENGTH_OF_STAY]

                    else:
                        user_input = user_input.replace(word, placeholders[AGE])
                        self.replaced_constants[word] = placeholders[AGE]

        elif constants_detected[AGE] > 0:
            for word in splitted_user_input:
                if word.isnumeric():
                    user_input = user_input.replace(word, placeholders[AGE])
                    self.replaced_constants[word] = placeholders[AGE]

        elif constants_detected[LENGTH_OF_STAY] > 0:
            for word in splitted_user_input:
                if word.isnumeric():
                    user_input = user_input.replace(word, placeholders[LENGTH_OF_STAY])
                    self.replaced_constants[word] = placeholders[LENGTH_OF_STAY]

        return user_input
