from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('status/', views.status_check, name='status'),
]