from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import Profile
from django import forms

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None 
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['privacy']
        widgets = {
            'privacy': forms.Select(attrs={'class': 'form-control'})
        }