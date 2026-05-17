from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.votes.models import Vote
from apps.votes.serializers import VoteSerializer, VoteCreateSerializer

# Create your views here.
class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.select_related('user', 'post').all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        post = self.get_object()
        serializer = VoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unvote(self, request, pk=None):
        post = self.get_object()
        Vote.objects.filter(user=request.user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        