from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import ModelForm
from django import forms
from PIL import Image
from App.account.models import *
from App.blog.models import *
from App.product.models import *
from captcha.fields import CaptchaField, CaptchaTextInput
from App.contact_us.models import Contact


class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'email_confirmed', 'activation_code', 'password_reset_code']

    title = forms.CharField(label='Anrede', required=False, max_length=10)
    name = forms.CharField(label='name', required=False, max_length=50)
    company_name = forms.CharField(label='Name des Gewerbes', required=False, max_length=50)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label='Anschrift', required=False)
    phone_number = forms.CharField(label='Telefonnummer', required=False, max_length=15)
    picture = forms.ImageField(label='Picture', required=False)

    title.widget.attrs.update({'class': 'form-control', 'placeholder': 'Anrede'})
    name.widget.attrs.update({'class': 'form-control', 'placeholder': 'Vor, und Nachname'})

    company_name.widget.attrs.update({'class': 'form-control', 'placeholder': 'Name des Gewerbes'})
    address.widget.attrs.update({'class': 'form-control', 'placeholder': 'Anschrift'})
    phone_number.widget.attrs.update({'class': 'form-control', 'placeholder': 'Telefonnummer'})
    picture.widget.attrs.update({'class': 'form-control-file', 'placeholder': 'Telefonnummer'})
    title.error_messages = {
        'required': 'Enter your title',
        'max_length': 'title is too long',
    }
    name.error_messages = {
        'required': 'Enter your first name',
        'max_length': 'first name is too long',
    }
    company_name.error_messages = {
        'required': 'Enter your company name',
        'max_length': 'company name is too long',
    }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Benutaname',
    }),
        label='username'
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Passwort',
    }),
        label='password'
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'repeat Passwort',
    }),
        label='repeat password'
    )
    email = forms.EmailField(max_length=50)
    email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
    email.error_messages = {
        'required': 'Enter your Email',
        'max_length': 'email is too long',
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'captcha/custom_field.html'


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['checked', 'time']

    subject = forms.CharField()
    phone_number = forms.CharField(required=False)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea, )
    captcha = CaptchaField(widget=CustomCaptchaTextInput, label='Enter code')
    subject.widget.attrs.update({'class': 'form-control', 'placeholder': 'Subject'})
    phone_number.widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone number'})
    email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
    content.widget.attrs.update({'class': 'form-control', 'placeholder': 'Message', 'rows': '5'})


class PostForm(ModelForm):
    post_image_width = 500
    post_image_height = 500

    class Meta:
        model = Post
        fields = ('slug', 'title', 'author', 'category', 'content', 'status', 'view',
                  'picture')

    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )

    slug = forms.CharField()
    title = forms.CharField()
    author = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="admin"))
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS)
    view = forms.DecimalField()
    picture = forms.ImageField(label='Picture', required=False)
    slug.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    title.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    author.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    category.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    content.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    status.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    view.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    picture.widget.attrs.update({'class': 'form-control-file', 'placeholder': ''})

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        image = Image.open(picture.file)
        if picture.size > 1048576:
            raise ValidationError("Picture size should be less than 1MB")
        if image.width > self.post_image_width:
            raise ValidationError(f"Picture width is more {self.post_image_width}")
        if image.height > self.post_image_height:
            raise ValidationError(f"Picture height is more {self.post_image_height}")
        return picture


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ExtensionForm(ModelForm):
    class Meta:
        model = Extension
        fields = '__all__'

    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    price = forms.FloatField()
    icon = forms.CharField()

    title.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    description.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    image.widget.attrs.update({'class': 'form-control-file', 'placeholder': ''})
    price.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    icon.widget.attrs.update({'class': 'form-control', 'placeholder': ''})


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    url = forms.CharField()
    title = forms.CharField()
    sub_title = forms.CharField()
    bg_class = forms.CharField()
    card_header = forms.CharField()
    card_body = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), )
    post_title = forms.CharField()
    post_content = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), )
    online_demo = forms.URLField()
    overview = forms.FileField()
    extensions = forms.ModelMultipleChoiceField(queryset=Extension.objects.all())
    price = forms.FloatField()
    image = forms.ImageField()

    title.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    sub_title.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    bg_class.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    card_header.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    card_body.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    post_title.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    post_content.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    online_demo.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    overview.widget.attrs.update({'class': 'form-control-file', 'placeholder': ''})
    url.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    extensions.widget.attrs.update({'class': 'custom-select', 'placeholder': ''})
    price.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    image.widget.attrs.update({'class': 'form-control-file', 'placeholder': ''})

    def clean_url(self):
        url = self.cleaned_data['url']
        print(url)
        if any(not c.isalnum() for c in url):
            raise ValidationError("url should be alphanumeric")
        url = url.lower()
        return url


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_owner", "comment_owner_email", "comment_content")
