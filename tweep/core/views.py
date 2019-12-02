from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView

from .models import Tweet
from .serializers import TweetLoadSerializer


# Create your views here.
class AllTweetsAPIView(ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetLoadSerializer
