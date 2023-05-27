from django.http import JsonResponse
from rest_framework.fields import IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserListSerializer(ModelSerializer):
    total_ads = IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'total_ads']

class UserCreateUpdateSerializer(ModelSerializer):

    locations = SlugRelatedField(slug_field='name', many=True, queryset=Location.objects.all(), required=False)

    def is_valid(self, *, raise_exception=False):


        for loc_name in self.initial_data.get('locations', []):
            loc, _ = Location.objects.get_or_create(name=loc_name)

        return super().is_valid(raise_exception=raise_exception)


    class Meta:
        model = User
        fields = '__all__'


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
