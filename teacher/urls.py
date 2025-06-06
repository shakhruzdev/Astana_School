from django.urls import path
from .views import teacher_view

urlpatterns = [
    path('teachers/', teacher_view, name='teachers'),
]
