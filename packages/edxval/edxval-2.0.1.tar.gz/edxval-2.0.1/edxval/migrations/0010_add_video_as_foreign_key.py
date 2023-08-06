from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edxval', '0009_auto_20171127_0406'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='videotranscript',
            unique_together={('language_code',)},
        ),
        migrations.RemoveField(
            model_name='videotranscript',
            name='video_id',
        ),
        migrations.AddField(
            model_name='videotranscript',
            name='video',
            field=models.ForeignKey(related_name='video_transcripts', to='edxval.Video', null=True, on_delete = models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='videotranscript',
            unique_together={('video', 'language_code')},
        ),
    ]
