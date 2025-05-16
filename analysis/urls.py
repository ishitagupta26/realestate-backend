from django.urls import path
from .views import chatbot_analysis

urlpatterns = [
    path('chatbot/', chatbot_analysis, name='chatbot_analysis'),
]
