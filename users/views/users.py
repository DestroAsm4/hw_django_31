
from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework.generics import  ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    CreateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer

TOTAL_ON_PAGE = 10



class UserListView(ListAPIView):
    queryset = User.objects.prefetch_related('locations').annotate(
        total_ads=Count('ad', filter=Q(ad__is_published=True)))
    serializer_class = UserListSerializer





class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

