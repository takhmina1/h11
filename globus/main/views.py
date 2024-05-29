from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import generics
from .models import Stories, Cards, Versions, Notifications
from .serializers import (
    StoriesSerializers,
    CardSerializers,
    VersionsSerializer,
    NotificationsSerializer,
)


class StoriesView(ListAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializers


class CardListOneView(ListAPIView):
    queryset = Cards.objects.filter(type=1).order_by('-id')[:3]
    serializer_class = CardSerializers


class CardListTwoView(ListAPIView):
    queryset = Cards.objects.filter(type=2).order_by('-id')[:3]
    serializer_class = CardSerializers


class AllCardView(ListAPIView):
    queryset = Cards.objects.all()
    serializer_class = CardSerializers


class CardDetailView(RetrieveAPIView):
    queryset = Cards.objects.all()
    serializer_class = CardSerializers


class NotificationsListView(ListAPIView):
    queryset = Notifications.objects.order_by('-id')
    serializer_class = NotificationsSerializer


class NotificationsDetailView(RetrieveAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer


class VersionsView(RetrieveAPIView):
    queryset = Versions.objects.latest("date")
    serializer_class = VersionsSerializer


