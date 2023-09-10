from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.utils import timezone
from markdown import markdown


class Note(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content_raw = models.TextField()
    content_html = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            num = 1
            base_slug = slug
            while Note.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug

        # Generate content_html from content_raw
        self.content_html = markdown(self.content_raw)

        super().save(*args, **kwargs)

    def get_body_html(self):
        # You can use a library like Markdown to convert raw text to HTML here
        # For simplicity, let's assume a simple HTML conversion
        return mark_safe(self.content_raw)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None
