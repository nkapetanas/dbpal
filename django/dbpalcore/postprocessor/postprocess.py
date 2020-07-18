
class Postprocessor:
    def replace_placeholders_with_constants(self, replaced_constants, preprocessed_users_input):

        for key, value in replaced_constants.items():
            preprocessed_users_input = preprocessed_users_input.replace(value, key)

        return preprocessed_users_input
