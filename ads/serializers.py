from rest_framework import serializers

from ads.models import Category, Location, User, ADS, Selection


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    location_id = serializers.SlugRelatedField(slug_field="name", queryset=Location.objects.all())

    class Meta:
        model = User
        exclude = ['password']

class UserListSerializer(serializers.ModelSerializer):
    location_id = serializers.SlugRelatedField(slug_field="name", queryset=Location.objects.all())
    t_ads = serializers.IntegerField()

    class Meta:
        model = User
        exclude = ['password']

class UserCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(user.password)
        user.save()

        return user


class LocationNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['name']

class UserNameSerializer(serializers.ModelSerializer):
    location_id = LocationNameSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'location_id']

class ADSSerializer(serializers.ModelSerializer):
    author_id = UserNameSerializer(read_only=True)

    class Meta:
        model = ADS
        fields = ('id', 'name', 'author_id', 'price', 'description',
                'is_published', 'image', 'category_id')


class ADSSelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ADS
        fields = ('id', 'name', 'author_id', 'description',
                'is_published', 'image', 'category_id')

class SelectionSerializer(serializers.ModelSerializer):
    items = ADSSelSerializer(many=True)

    class Meta:
        model = Selection
        fields = ['id', 'name', 'items']

