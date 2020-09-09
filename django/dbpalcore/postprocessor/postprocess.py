from django.db import connection

cursor = connection.cursor()


class Postprocessor:
    def replace_placeholders_with_constants(self, replaced_constants, preprocessed_users_input):
        for key, value in replaced_constants.items():

            if key == 'femal':
                key = 'female'

            key = '\'' + key.lower() + '\''
            preprocessed_users_input = preprocessed_users_input.replace(value.lower(), key)

        print(preprocessed_users_input)
        return preprocessed_users_input

    def get_query_results(self, query):
        cursor.execute(query + ''';''')

        return cursor.fetchall()
