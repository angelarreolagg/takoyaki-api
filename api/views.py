from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import django

@api_view(['GET'])
def status_check(request):
    """
    Health check endpoint
    Returns system status and version info
    """
    
    # Check database connection
    db_status = "healthy"
    db_info = {}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            db_info = {
                "status": "connected",
                "engine": "postgresql",
                "version": db_version.split()[0:2]  # PostgreSQL version
            }
    except Exception as e:
        db_info = {
            "status": "disconnected",
            "error": str(e)
        }
    
    data = {
        "status": "ok",
        "service": "takoyaki-news",
        "version": "1.0.0",
        "django_version": django.get_version(),
        "database": db_info,
    }
    
    return Response(data, status=status.HTTP_200_OK)