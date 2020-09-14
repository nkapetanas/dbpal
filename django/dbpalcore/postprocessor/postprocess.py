from django.db import connection

cursor = connection.cursor()

PLACEHOLDERS = ["@id", "@age", "@length_of_stay", "@first", "@last", "@diagnosis"]


class Postprocessor:
    def replace_placeholders_with_constants(self, replaced_constants, preprocessed_users_input):
        for key, value in replaced_constants.items():

            if key == 'femal':
                key = 'female'

            key = '\'' + key.lower() + '\''
            preprocessed_users_input = preprocessed_users_input.replace(value.lower(), key)

        return preprocessed_users_input

    def check_and_replace_wrong_placeholders(self, postprocessed_query):
        for placeholder in PLACEHOLDERS:
            postprocessed_query = postprocessed_query.replace(placeholder, "'unknown'")

        return postprocessed_query

    def get_query_results(self, query):
        cursor.execute(query + ''';''')

        return cursor.fetchall()
