from django.http import JsonResponse

from .models import Patients
from .serializers import PatientSerializer

from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

from .utils import get_auth0_user_id_from_request
from .serializers import PatientSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator


class PatientList(generics.ListCreateAPIView):
    """
    Lists and creates tasks.
    """
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        auth0_user_id = get_auth0_user_id_from_request(self.request)
        # Set the user to the one in the token.
        serializer.save(created_by=auth0_user_id)

    def get_queryset(self):
        """
        This view should return a list of all Patients
        for the currently authenticated user.
        """
        auth0_user_id = get_auth0_user_id_from_request(self.request)
        return Patients.objects.filter(created_by=auth0_user_id)


@csrf_exempt
def get_data(request):
    data = Patients.objects.all()
    if request.method == 'GET':
        serializer = PatientSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
