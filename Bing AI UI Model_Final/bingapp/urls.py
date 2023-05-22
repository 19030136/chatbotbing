from django.urls import path
from bingapp import views
from .views import chat_view_wrapper

urlpatterns = [
    path('', chat_view_wrapper, name='chat'),
]
