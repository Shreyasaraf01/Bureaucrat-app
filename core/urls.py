from django.urls import path
from django.contrib.auth.views import LogoutView  # Correct import here
from . import views
from .views import (
    signup_view,
    CustomLoginView,
    dashboard_view,
    upload_and_summarize_text,
    home_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # LogoutView correctly used
    path('dashboard/', dashboard_view, name='dashboard'),
    path('summarize/', views.upload_and_summarize_text, name='upload_and_summarize'),
]
