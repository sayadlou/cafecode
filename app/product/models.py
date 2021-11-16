from django.db import models
from django.forms.models import model_to_dict
from django.core import serializers


class Extension(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    icon = models.CharField(max_length=50)

    def __str__(self):
        return self.title

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
        try:
            obj = self.objects.get(id=item)
            obj.delete()
            return True
        except self.DoesNotExist:
            return False


class Product(models.Model):
    url = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50)
    bg_class = models.CharField(max_length=50)
    card_header = models.CharField(max_length=50)
    card_body = models.TextField()
    post_title = models.CharField(max_length=50)
    price = models.FloatField()
    extensions = models.ManyToManyField(Extension)
    post_content = models.TextField()
    online_demo = models.URLField(max_length=50)
    overview = models.FileField(null=True)
    image = models.ImageField()

    def __str__(self):
        return self.title

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
        try:
            obj = self.objects.get(id=item)
            obj.delete()
            return True
        except self.DoesNotExist:
            return False
