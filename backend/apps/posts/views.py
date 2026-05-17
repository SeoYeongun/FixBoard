from django.db.models import F
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.posts.models import Post
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.posts.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer
)


class PostViewSet(ModelViewSet):
    # soft delete 적용 → 삭제된 데이터 제외
    queryset = Post.objects.filter(is_deleted=False)

    # 로그인 사용자만 수정/삭제 가능, 읽기는 누구나 가능
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 요청 종류에 따라 다른 serializer 사용
    # → 성능 + 응답 구조 최적화
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer   # 목록용 (가벼움)
        elif self.action == 'retrieve':
            return PostDetailSerializer  # 상세용
        elif self.action == 'comments':
            return CommentSerializer  # 게시글 하위 댓글 조회/생성용
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer  # 생성/수정용
        return PostDetailSerializer

    # 게시글 생성 시 작성자를 자동으로 현재 유저로 설정
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # 삭제 대신 soft delete 처리
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    # 상세 조회(GET) 시 작성자 본인을 제외하고 조회수 자동 증가
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        if not (request.user.is_authenticated and request.user == post.author):
            Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
            post.refresh_from_db(fields=['view_count'])

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    # GET/POST /api/posts/{id}/comments/
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == 'GET':
            comments = Comment.objects.filter(post=post).select_related('user').order_by('created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)