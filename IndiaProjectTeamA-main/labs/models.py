from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    """SQLインジェクション・ラボで使う商品データ。"""

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    released = models.BooleanField(default=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """格納型XSSラボで使うコメント。"""

    author = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author}: {self.body[:20]}"


class Account(models.Model):
    """アクセス制御(IDOR)ラボで使う口座情報。"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    full_name = models.CharField(max_length=80)
    balance = models.IntegerField(default=0)
    secret_memo = models.CharField(max_length=200, default="")

    def __str__(self):
        return f"Account #{self.pk} ({self.full_name})"
