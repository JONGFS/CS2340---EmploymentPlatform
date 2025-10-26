from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None 
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['privacy']
        widgets = {
            'privacy': forms.Select(attrs={'class': 'form-control'})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'company', 'headline', 'skills', 'education', 'work_experience', 'portfolio_link', 'linkedin_link', 'github_link', 'other_links']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name (if you are a recruiter)'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Engineer, Marketing Specialist'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your skills (one per line or comma-separated)'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Educational background and qualifications'}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Work experience and professional history'}),
            'portfolio_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourportfolio.com'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/yourusername'}),
            'other_links': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Other relevant links (one per line)'}),
        }
        labels = {
            'headline': 'Professional Headline',
            'skills': 'Skills',
            'education': 'Education',
            'work_experience': 'Work Experience',
            'portfolio_link': 'Portfolio/Website',
            'linkedin_link': 'LinkedIn Profile',
            'github_link': 'GitHub Profile',
            'other_links': 'Other Links',
        }