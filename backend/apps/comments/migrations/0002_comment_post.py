from django.db import migrations, models
import django.db.models.deletion


def copy_target_id_to_post(apps, schema_editor):
    Comment = apps.get_model('comments', 'Comment')
    Post = apps.get_model('posts', 'Post')

    for comment in Comment.objects.all():
        post_id = comment.target_id
        if Post.objects.filter(id=post_id).exists():
            comment.post_id = post_id
            comment.save(update_fields=['post'])


def delete_orphan_comments(apps, schema_editor):
    Comment = apps.get_model('comments', 'Comment')
    # target_id가 실제 게시글과 매핑되지 않는 고아 댓글 제거
    Comment.objects.filter(post__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_post_is_deleted_post_updated_at_post_view_count_and_more'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='posts.post',
            ),
        ),
        migrations.RunPython(copy_target_id_to_post, migrations.RunPython.noop),
        migrations.RunPython(delete_orphan_comments, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='comment',
            name='target_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='posts.post',
            ),
        ),
    ]
