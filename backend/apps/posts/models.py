from django.db import models
from django.conf import settings  # 커스텀 유저 모델을 안전하게 참조하기 위해 사용

class Post(models.Model):
    # 게시글 제목 (검색/목록에서 핵심 필드)
    title = models.CharField(max_length=255)

    # 게시글 본문 내용
    content = models.TextField()

    # 작성자 (User 모델과 관계)
    # settings.AUTH_USER_MODEL을 사용하면 User 모델 변경에도 안전
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # 유저 삭제 시 게시글도 삭제
        related_name='posts'        # user.posts 로 역참조 가능
    )

    # 조회수 (트래픽/인기글 기능에 사용)
    view_count = models.PositiveIntegerField(default=0)

    # 생성/수정 시간 (정렬, 최신순 기능에 사용)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # soft delete (실제 삭제하지 않고 숨김 처리)
    # → 데이터 복구 / 로그 분석 가능
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title