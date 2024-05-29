from django.contrib import admin
from .models import Stories, StoryVideos, Cards, Notifications, NotificationsImg, Versions

@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'img', 'link')

@admin.register(StoryVideos)
class StoryVideosAdmin(admin.ModelAdmin):
    list_display = ('story', 'url', 'created_at')

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('type', 'text', 'title', 'datefrom', 'dateto', 'date', 'img')
    list_filter = ('type', 'datefrom', 'dateto')
    search_fields = ('title', 'text')

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date')
    search_fields = ('title', 'description')

@admin.register(NotificationsImg)
class NotificationsImgAdmin(admin.ModelAdmin):
    list_display = ('notification', 'img')

@admin.register(Versions)
class VersionsAdmin(admin.ModelAdmin):
    list_display = ('version', 'appstore', 'googleplay', 'date')
