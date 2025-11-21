from django import forms

class MessageForm(forms.Form):
    recipient_id = forms.IntegerField(widget=forms.HiddenInput)
    subject = forms.CharField(max_length=140, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':6}))

class EmailForm(forms.Form):
    recipient_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    subject = forms.CharField(max_length=140, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':6}))
