from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']