# views.py

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, DocumentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Document
from django.contrib.auth.views import LoginView
from PyPDF2 import PdfReader
from django.conf import settings
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next', 'upload_and_summarize')  # Default redirect URL
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('upload_and_summarize')  # Redirect to upload & summarize
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


# Custom Login View
class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'core/login.html'
    next_page = 'upload_and_summarize'


# Home View
def home_view(request):
    return render(request, 'core/home.html')


# Dashboard View
def dashboard_view(request):
    if request.user.is_authenticated:
        documents = Document.objects.filter(user=request.user)
        return render(request, 'core/dashboard.html', {'documents': documents})
    else:
        return redirect('login')
    
# Function to summarize text using Sumy
def summarize_with_sumy(content):
    parser = PlaintextParser.from_string(content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)  # Summarize to 3 sentences
    return " ".join(str(sentence) for sentence in summary)


# Upload and Summarize View
def upload_and_summarize_text(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user  # Assign the document to the logged-in user
            document.save()

            file = document.file
            content = ""

            # Extract text from the uploaded file
            try:
                if file.name.endswith('.txt'):
                    content = file.read().decode('utf-8')
                elif file.name.endswith('.pdf'):
                    pdf_reader = PdfReader(file)
                    content = " ".join(page.extract_text() for page in pdf_reader.pages)
            except Exception as e:
                return HttpResponseBadRequest(f"Error reading file: {str(e)}")

            # Summarize the content using Sumy
            try:
                if content.strip():  # Only summarize if content is non-empty
                    summary = summarize_with_sumy(content)
                else:
                    summary = "No content to summarize."
            except Exception as e:
                summary = f"Error during summarization: {str(e)}"

            # Render results
            return render(request, 'core/summarize.html', {
                'document': document,
                'content': content,
                'summary': summary
            })
        else:
            return HttpResponseBadRequest("Invalid form submission.")
    else:
        form = DocumentForm()
    return render(request, 'core/upload.html', {'form': form})