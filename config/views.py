from django.shortcuts import render
from django.db import connection
from django.conf import settings


def home(request):
    """
    Renders the Healthcare Management System landing page.
    Performs real-time database connectivity verification so that system
    status is accurately reported rather than assumed.
    """
    db_connected = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            db_connected = bool(cursor.fetchone())
    except Exception:
        db_connected = False

    context = {
        "db_connected": db_connected,
        "db_name": settings.DATABASES["default"].get("NAME", "PostgreSQL"),
        "debug_mode": settings.DEBUG,
    }
    return render(request, "home.html", context)
