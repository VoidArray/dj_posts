from django.db import models

from django.core.cache import cache
from django.utils import timezone


class Tag(models.Model):
    title = models.CharField(max_length=128)
    is_hide = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=128)
    is_hide = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='photos/', max_length=1000)
    creation_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_photo_key(self):
        return self.id

    def add_like(self):
        key = self.get_photo_key()
        try:
            cache.incr(key, delta=1)
        except ValueError:
            cache.set(key, 1)

    @property
    def like_count(self):
        key = self.get_photo_key()
        count = cache.get(key)
        if not count:
            return 0
        return count

    class Meta:
        verbose_name = u'Photos'
        verbose_name_plural = u'Photo'

