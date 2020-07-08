from django.http import JsonResponse, HttpResponse

from .models import Patients
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer

import sys
sys.path.append('../../dbpalcore/preprocessor/preprocessor')

from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

from .utils import get_auth0_user_id_from_request
from .serializers import PatientSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator


class PatientsDetails(APIView):
    """
    Lists and creates tasks.
    """
    queryset = Patients.objects.all()
    # serializer_class = PatientSerializer

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

    def getData(self, searchInput):
        try:

            return HttpResponse('The input value is {}'.format(searchInput))
            # return Patients.objects.get(pk=task_id)
        except Patients.DoesNotExist:
            raise Http404

    # def get(self, request, task_id, format=None):
    #     task = self.get_object(task_id)
    #     serializer = PatientSerializer(task)
    #     return Response(serializer.data)
    #
    # def perform_create(self, serializer):
    #     auth0_user_id = get_auth0_user_id_from_request(self.request)
    #     # Set the user to the one in the token.
    #     serializer.save(created_by=auth0_user_id)
    #
    # def get_queryset(self):
    #     """
    #     This view should return a list of all Patients
    #     for the currently authenticated user.
    #     """
        # auth0_user_id = get_auth0_user_id_from_request(self.request)
        # return Patients.objects.filter(created_by=auth0_user_id)


@csrf_exempt
def get_data(request):
    data = Patients.objects.all()
    if request.method == 'GET':
        serializer = PatientSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
