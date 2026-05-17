from rest_framework import serializers
from apps.votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    # 응답에서 투표한 유저를 문자열(username)로 표시
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ["id", "user", "post", "vote_type", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        # user는 뷰에서 request.user로 주입
        fields = ["post", "vote_type"]
        