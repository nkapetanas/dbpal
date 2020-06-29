from rest_framework import serializers
from .models import Patients


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ('id', 'first_name', 'last_name', 'diagnosis',  'gender', 'length_of_stay', 'age')

        # extra_kwargs = {
        #     'created_by':  { 'read_only': True }
        # }
