
from rest_framework import serializers

from images_app.accounts.models import CustomUser
from images_app.images.serializers import UserImageSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    images = UserImageSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'images')
