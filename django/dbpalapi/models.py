from django.db import models


class Patients(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    diagnosis = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    length_of_stay = models.IntegerField()
    age = models.IntegerField()

    # Meta data about the database table.
    class Meta:
        db_table = 'patients'

        # Set default ordering
        ordering = ['id']
