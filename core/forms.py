from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Document
from django.conf import settings

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different one.")
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Document Form
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'category']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (example: 10MB)
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("File size exceeds the 10MB limit.")
            # Check file type
            if not file.name.endswith(('.pdf', '.txt')):
                raise forms.ValidationError("Only PDF and TXT files are allowed.")
        return file


# Summarization Form
class SummarizationForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Paste the content of the file here...'}),
        label="File Content",
        required=True
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': 'readonly'}),
        label="Summary",
        required=False
    )