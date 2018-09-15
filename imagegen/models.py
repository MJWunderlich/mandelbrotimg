from django.db import models
from django.urls import reverse
from datetime import datetime


class GeneratedImage(models.Model):
    slug = models.CharField(max_length=300)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now, auto_created=True, blank=True)
    viewed_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    class Meta:
        verbose_name = "Generated Image record"
        verbose_name_plural = "Generated Image records"
        ordering = ["-created_at"]
        get_latest_by = "-viewed_at"
        index_together = ["created_at", "viewed_at"]

    def aspect_ratio(self):
        return float(self.width) / float(self.height)

    def get_absolute_url(self):
        reverse('saved', (self.slug,))

    def __str__(self):
        return "/imagegen/saved/%s" % self.slug
