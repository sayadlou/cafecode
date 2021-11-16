from App.account.models import *
from App.contact_us.models import *
from App.blog.models import *
from App.product.models import *
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField


class CustomerSerializerAll(serializers.ModelSerializer):
    user_name = ReadOnlyField(source='user.username')
    email = ReadOnlyField(source='user.email')

    class Meta:
        model = Customer
        fields = ('user_name', 'company_name', 'email', 'phone_number',)
        # exclude = ('user',)


class ContactSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        # fields = ('','','','','',)


class CustomerSerializerView(serializers.ModelSerializer):
    user_name = ReadOnlyField(source='user.username')
    email = ReadOnlyField(source='user.email')

    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ('user',)


class ContactSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class PostSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ('','','','','',)


class PostSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CategorySerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # fields = ('','','','','',)


class CategorySerializerView(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('','','','','',)


class CommentSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ExtensionSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Extension
        fields = '__all__'
        # fields = ('','','','','',)


class ExtensionSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Extension
        fields = '__all__'


class ExtensionSerializerAllField(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.title

    class Meta:
        model = Extension
        fields = '__all__'


class ExtensionSerializerViewField(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.title

    class Meta:
        model = Extension
        fields = '__all__'


class ProductSerializerAll(serializers.ModelSerializer):
    extensions = ExtensionSerializerAllField(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('','','','','',)


class ProductSerializerView(serializers.ModelSerializer):
    extensions = ExtensionSerializerViewField(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'
