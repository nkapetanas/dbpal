from dbpalcore.preprocessor.preprocess import *
from dbpalcore.postprocessor.postprocess import *
from dbpalcore.neuraltranslator.seq2seqService import *
from .models import Patients


def preprocess_query(searchInput):
    preprocessor = Preprocessor()
    postprocessor = Postprocessor()
    seq2seqService = Seq2SeqService()

    users_input_cleaned = preprocessor.clean_users_input(searchInput)
    users_input_with_placeholders = preprocessor.replace_constants_with_placeholders(users_input_cleaned)
    users_input_with_numeric_placeholders = preprocessor.replace_numeric_constants_with_placeholders(users_input_with_placeholders)

    translated_query = seq2seqService.evaluate_query(users_input_with_numeric_placeholders)

    postprocessed_users_input = postprocessor.replace_placeholders_with_constants(preprocessor.replaced_constants,
                                                                          translated_query)

    validated_result = postprocessor.check_and_replace_wrong_placeholders(postprocessed_users_input)
    patients = Patients.objects.raw(validated_result.lower() + ''';''')

    return users_input_with_numeric_placeholders, translated_query, validated_result, patients