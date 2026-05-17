from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # =========================
    # 기본 정보
    # =========================

    # 닉네임 (커뮤니티에서 표시용)
    nickname = models.CharField(max_length=50, unique=True)

    # 프로필 이미지
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    password = models.CharField(max_length=128)

    # 자기소개
    bio = models.TextField(blank=True)

    # =========================
    # 커뮤니티 활동
    # =========================

    # 경험치 (활동 점수)
    points = models.IntegerField(default=0)

    # 레벨 (단순 계산 or 추후 자동화)
    level = models.IntegerField(default=1)

    # 채택된 답변 수 (신뢰도)
    accepted_answers = models.IntegerField(default=0)

    # =========================
    # 상태 관리
    # =========================

    # 계정 활성화 여부
    is_active = models.BooleanField(default=True)

    # 관리자 여부
    is_staff = models.BooleanField(default=False)

    # =========================
    # 타임스탬프
    # =========================

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =========================
    # 표시용
    # =========================

    def __str__(self):
        return self.username