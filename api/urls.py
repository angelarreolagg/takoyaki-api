from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from news.views import NewsViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('status/', views.status_check, name='status'),
    path('', include(router.urls)),
]
