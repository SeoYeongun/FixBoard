from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.posts.models import Post
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

    # 커스텀 API (조회수 증가)
    # POST /api/posts/{id}/view/
    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        post = self.get_object()
        post.view_count += 1
        post.save()
        return Response({"message": "view count increased"})