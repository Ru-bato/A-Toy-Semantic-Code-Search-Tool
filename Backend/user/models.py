from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, default='')

    def get_username(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
    )


class SearchRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_records')
    search_query = models.CharField(max_length=255)
    search_link = models.URLField(default='')
    search_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    item_title = models.CharField(max_length=255)
    item_link = models.URLField()
    added_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'item_title')  # 确保每个用户的收藏是唯一的
