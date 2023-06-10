from datetime import datetime

from rest_framework.fields import SerializerMethodField, BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Categories, Selection
from ads.validators import check_not_published
from users.models import User, Location
from users.serializers import UserListSerializer, LocationSerializer

class UserAdSerializer(ModelSerializer):

    locations = LocationSerializer(many=True)


    class Meta:
        model = User
        fields = ['username', 'locations']

class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(ModelSerializer):

    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())
    author = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    is_published = BooleanField(required=False, read_only=True) # validators=[check_not_published],



    class Meta:
        model = Ad
        # exclude = ['is_published']
        fields = '__all__'


class AdListSerializer(ModelSerializer):
    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())
    user_locations = SerializerMethodField()

    def get_user_locations(self, obj):
        return [loc.name for loc in obj.author.locations.all()]

    class Meta:
        model = Ad
        fields = ['name', 'price', 'category', 'user_locations']


class AdDetailSerializer(ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'

class SelectionSerializer(ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'

class SelectionCreateSerializer(ModelSerializer):

    owner = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'