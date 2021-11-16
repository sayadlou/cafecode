from django.forms import ModelForm
from django import forms
from .models import Contact
from captcha.fields import CaptchaField, CaptchaTextInput
from django.utils.translation import ugettext_lazy as _

owner_email = (
    ('info@cafecode.de', _('Moshavere')),
    ('g.madar@cafecode.de', _('Graphic')),
    ('s.sayad@cafecode.de', _('Poshtibanie')),
)


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
    owner = forms.ChoiceField(choices=owner_email)
    attachment = forms.FileField()
    subject.widget.attrs.update({'class': 'form-control', 'placeholder': _("Subject")})
    phone_number.widget.attrs.update({'class': 'form-control', 'placeholder': _('Phone number')})
    email.widget.attrs.update({'class': 'form-control', 'placeholder': _('Email')})
    content.widget.attrs.update({'class': 'form-control', 'placeholder': _('Message'), 'rows': '5'})
    owner.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
    attachment.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
