from django.db import models
from django.contrib.auth.models import User
import os

# Function to categorize uploads into subfolders based on category
def categorized_upload_to(instance, filename):
    category_folder = instance.category.lower().replace(" ", "_")  # Safe folder name
    return os.path.join('documents', category_folder, filename)

class Document(models.Model):
    # Category constants
    LEGAL = 'Legal'
    FINANCIAL = 'Financial'
    POLICY = 'Policy'

    CATEGORY_CHOICES = [
        (LEGAL, 'Legal'),
        (FINANCIAL, 'Financial'),
        (POLICY, 'Policy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=categorized_upload_to)  # Dynamic folder path
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(blank=True, null=True)  # Add summary field

    def __str__(self):
        return f'{self.title} - {self.user.username}'