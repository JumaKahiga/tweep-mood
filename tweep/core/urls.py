from django.urls import path

from .views import AllTweetsAPIView

app_name = 'core'

urlpatterns = [
    path('all/', AllTweetsAPIView.as_view())
]
