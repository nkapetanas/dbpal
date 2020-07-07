from django.db import models


class Patients(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    diagnosis = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    length_of_stay = models.IntegerField(max_length=4)
    age = models.IntegerField(max_length=4)

    # Meta data about the database table.
    class Meta:
        db_table = 'dbpal'

        # Set default ordering
        ordering = ['id']
