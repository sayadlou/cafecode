from django.db import models
from django.forms.models import model_to_dict
from django.core import serializers


class Contact(models.Model):
    checked_type = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    subject = models.CharField(max_length=50, db_column="Subject")
    phone_number = models.CharField(max_length=15, null=True, blank=True, db_column="Phone Number")
    email = models.EmailField(max_length=50, db_column="Email Address")
    content = models.TextField(null=True, db_column="Content")
    owner = models.CharField(max_length=50)
    checked = models.CharField(max_length=50, choices=checked_type, db_column="Read")
    attachment = models.FileField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)

    def __str__(self):
        return self.subject

    def view_it(self, item):
        try:
            item = int(item)
        except ValueError:
            return False
        try:
            obj = self.objects.get(id=item)
            return obj
        except self.DoesNotExist:
            return False

    def delete_it(self, item):
        try:
            item = int(item)
        except ValueError:
            return False
        if not isinstance(item, int):
            return False
        print(item)
        try:
            obj = self.objects.get(id=item)
            obj.delete()
            return True
        except self.DoesNotExist:
            return False
