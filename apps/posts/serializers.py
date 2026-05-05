from rest_framework import serializers
from apps.posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    # 작성자를 문자열로 보여줌 (username)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        # 목록에서는 가볍게 필요한 정보만 반환 (성능 최적화)
        fields = ['id', 'title', 'author', 'view_count', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    # 상세 페이지에서는 모든 정보 반환
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # 생성 시 필요한 필드만 받음
        # author는 서버에서 자동 설정 (보안)
        fields = ['title', 'content']