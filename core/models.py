from django.db import models
import os

# Function to categorize uploads into subfolders based on category
def categorized_upload_to(instance, filename):
    # Dynamically set folder name based on the category
    category_folder = instance.category.lower()  # Convert category to lowercase
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

    # Model fields
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=categorized_upload_to)  # Dynamic upload path
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.user.username}'  # Include username for easier identification
