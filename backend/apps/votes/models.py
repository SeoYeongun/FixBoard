from django.db import models
from django.conf import settings

class Vote(models.Model):
    """
    게시물 추천/비추천 기록 모델.
    한 유저는 한 게시물에 대해 1번만 투표할 수 있다.
    """

    class VoteType(models.IntegerChoices):
        UP = 1, "upvote"
        DOWN = -1, "downvote"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    vote_type = models.SmallIntegerField(choices=VoteType.choices)

    # 추후 변경 이력/통계에 활용하기 위한 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 유저-게시물 조합의 중복 투표 방지
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_vote_per_user_post",
            )
        ]
        indexes = [
            models.Index(fields=["post", "vote_type"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user_id}:{self.post_id}:{self.get_vote_type_display()}"
