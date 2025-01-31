from django.contrib import admin
from core.models import Document
from core.forms import DocumentForm

class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm

admin.site.register(Document, DocumentAdmin)