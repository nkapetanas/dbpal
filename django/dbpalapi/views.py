from django.http import JsonResponse, HttpResponse

from dbpalcore.preprocessor.preprocess import *
from dbpalcore.postprocessor.postprocess import *
from dbpalcore.neuraltranslator.seq2seqService import *
from rest_framework.utils import json

from .models import Patients
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from .utils import get_auth0_user_id_from_request

from .serializers import PatientSerializer
import sys

sys.path.append('../../dbpalcore/preprocessor/preprocessor')

preprocessor = Preprocessor()
postprocessor = Postprocessor()
seq2seqService = Seq2SeqService()


class PatientsDetails(APIView):

    """
    We then pass this queryset to an instance of PatientSerializer, specifying many=True. This tells the serializer that we want to serialize a collection of objects, and not just a single instance.

    Lastly, with the return Response(serializer.data), we return the list of serialized Patient objects.
    """
    def get(self, request, format=None):
        """
        Return a list of all patients.
        """
        patients = Patients.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def getData(self, search_input):
        try:
            unique_db_columns_names = get_unique_db_columns()
            db_column_names = []
            for column_name in unique_db_columns_names:
                db_column_names.append(''.join(column_name))

            placeholders = create_place_holders_from_db(db_column_names)
            return HttpResponse('The input value is {}'.format(placeholders))
        except Patients.DoesNotExist:
            raise Http404

class CombinedAPIView(APIView):

    def getCombinedData(request):
        searchInput = request.GET.get('searchInput')

        # users_input_cleaned = preprocessor.clean_users_input(searchInput)
        # users_input_with_placeholders = preprocessor.replace_constants_with_placeholders(users_input_cleaned)
        # users_input_with_numeric_placeholders = preprocessor.replace_numeric_constants_with_placeholders(users_input_with_placeholders)
        #
        # postprocessed_users_input = postprocessor.replace_placeholders_with_constants(preprocessor.replaced_constants,
        #                                                               users_input_with_numeric_placeholders)

        # translated_query = seq2seqService.evaluate_query(postprocessed_users_input)
        translated_query = seq2seqService.evaluate_query(searchInput)
        patients = Patients.objects.all()
        serializer = PatientSerializer(patients, many=True)

        context = {
            'patients': serializer.data,
            'sqlResponse': translated_query,
        }

        data = json.dumps(context, indent=4, sort_keys=True, default=str)
        return HttpResponse(data, content_type='application/json')
