from django.db import models

class Census(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    house_address = models.CharField(max_length=255)
    residential_building = models.CharField(max_length=255, blank=True)
    lga_of_residence = models.CharField(max_length=255)
    state_of_residence = models.CharField(max_length=255)
    lga_of_origin = models.CharField(max_length=255)
    state_of_origin = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255, blank=True)
    place_of_work = models.CharField(max_length=255, blank=True)
    level_of_education = models.CharField(max_length=255, blank=True)
    type_of_family = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming you want to link the Census model to Django's built-in User model

    def __str__(self):
        return '%s %s' % (self.last_name, self.first_name)
    