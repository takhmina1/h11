from django.urls import path
from .views import (
    StoriesView,
    CardListOneView,
    CardListTwoView,
    AllCardView,
    CardDetailView,
    NotificationsListView,
    NotificationsDetailView,
    VersionsView,
)

urlpatterns = [
    path('stories/', StoriesView.as_view(), name='stories-list'),
    path('cards/one/', CardListOneView.as_view(), name='card-list-one'),
    path('cards/two/', CardListTwoView.as_view(), name='card-list-two'),
    path('cards/all/', AllCardView.as_view(), name='all-card-list'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('notifications/', NotificationsListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/', NotificationsDetailView.as_view(), name='notifications-detail'),
    path('versions/', VersionsView.as_view(), name='versions-detail'),
   
]
