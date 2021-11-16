from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_title = models.CharField(max_length=50)

    def __str__(self):
        return self.category_title

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


class Post(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    picture = models.ImageField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        print(picture.size)
        if picture.size > 1048576:
            raise ValidationError("Picture size shold be less than 1MB")
        return picture

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


class Comment(models.Model):
    COMMENT = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    comment_owner = models.CharField(max_length=50)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_owner_email = models.EmailField(max_length=50)
    comment_content = models.TextField()
    comment_status = models.CharField(max_length=20, choices=COMMENT)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_owner

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
