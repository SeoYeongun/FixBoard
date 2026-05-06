from rest_framework import serializers
from apps.comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'post', 'created_at', 'updated_at']