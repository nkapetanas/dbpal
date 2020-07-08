
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'
stop = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')


def get_unique_db_columns():
    pass


def create_place_holders_from_db():
    pass

def get_n_grams():
    pass

class Preprocessor:
    def __init__(self):
        self.unique_db_columns = get_unique_db_columns()
        self.placeholders = create_place_holders_from_db()
        self.n_grams = get_n_grams()

    def clean_users_input(self, user_input):
        pass
