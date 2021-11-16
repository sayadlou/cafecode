from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.forms.models import model_to_dict


def random_string():
    return get_random_string(length=32)


class Customer(models.Model):
    ACCOUONT_TYPE = (
        ('Company', 'Company'),
        ('Personal', 'Personal'),
    )
    title = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True, db_column="Name")
    company_name = models.CharField(max_length=50, null=True, blank=True, db_column="Company name")
    picture = models.ImageField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False, db_column="Email confirmation")
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    activation_code = models.CharField(default=random_string, max_length=32)
    password_reset_code = models.CharField(max_length=32, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    def delete_it(self, item):
        if not isinstance(item, str):
            return False
        try:
            user = User.objects.get(username=item)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def view_it(self, item):
        if not isinstance(item, str):
            return False
        try:
            user = User.objects.get(username=item)
        except User.DoesNotExist:
            return False
        try:
            obj = self.objects.get(user=user)
            return obj
        except self.DoesNotExist:
            return False

