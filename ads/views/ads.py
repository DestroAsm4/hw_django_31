from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdListSerializer, AdSerializer, AdDetailSerializer, AdCreateSerializer

TOTAL_ON_PAGE = 10



class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by('-price')
    serializers = {
        'list': AdListSerializer,
        'retrieve': AdDetailSerializer,
        'create': AdCreateSerializer,
    }
    default_serializer = AdSerializer

    permissions = {
        # 'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsOwner | IsStaff],
        'destroy': [IsOwner | IsStaff],
        'partial_update': [IsOwner | IsStaff]
    }
    default_permission = [AllowAny]
    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        cat_list = request.GET.getlist('cat')
        if cat_list:
            self.queryset = self.queryset.filter(category_id__in=cat_list)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get('price_from')

        if price_from and not price_from.isdigit():
            return Response(data={'message': 'int'}, status=status.HTTP_400_BAD_REQUEST)

        if price_from and price_from.isdigit():
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to and price_to.isdigit():
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)

