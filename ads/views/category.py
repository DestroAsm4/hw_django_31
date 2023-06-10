import json

from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from ads.models import Categories
from ads.serializers import CategorySerializer

def root(request):
    return JsonResponse({'status': 'ok'})
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()