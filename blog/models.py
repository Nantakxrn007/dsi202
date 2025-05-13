from django.db import models

class BlogContent(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="รูปภาพประกอบ (ถ้ามี)")
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True, verbose_name="URL วิดีโอ (YouTube, Vimeo)")
    video_file = models.FileField(upload_to='blog_videos/', blank=True, null=True, verbose_name="ไฟล์วิดีโอ MP4")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title