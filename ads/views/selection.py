from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Selection
from ads.permissions import IsOwner
from ads.serializers import SelectionSerializer, SelectionCreateSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializers = {
        "create": SelectionCreateSerializer
    }
    default_serializer = SelectionSerializer
    permissions = {
        # 'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsOwner],
        'destroy': [IsOwner],
        'partial_update': [IsOwner]

    }
    default_permission = [AllowAny]
    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)