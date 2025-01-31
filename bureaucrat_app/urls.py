# bureaucrat_app/urls.py (Project-level URLs)
from django.contrib import admin
from django.urls import path, include  # include() is used to include app URLs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface URL
    path('', include('core.urls')),  # Include core app URLs (this includes signup, login, etc.)
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
