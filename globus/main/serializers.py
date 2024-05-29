from rest_framework import serializers
from .models import Stories, StoryVideos, Cards, Notifications, NotificationsImg, Versions

class StoryVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryVideos
        fields = '__all__'

class StoriesSerializer(serializers.ModelSerializer):
    videos = StoryVideosSerializer(many=True, read_only=True)

    class Meta:
        model = Stories
        fields = '__all__'

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

class NotificationsImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsImg
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    images = NotificationsImgSerializer(many=True, read_only=True)

    class Meta:
        model = Notifications
        fields = '__all__'

class VersionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versions
        fields = '__all__'
