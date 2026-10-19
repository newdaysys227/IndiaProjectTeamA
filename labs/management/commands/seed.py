# -*- coding: utf-8 -*-
"""デモ用の初期データを投入する: python manage.py seed"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from labs.models import Account, Comment, Product


class Command(BaseCommand):
    help = "Put demo data (products, users, accounts)"

    def handle(self, *args, **options):
        # --- products (SQLi) ---
        Product.objects.all().delete()
        products = [
            ("Gift card 1000 yen", "gift", True, 1000),
            ("Gift card 3000 yen", "gift", True, 3000),
            ("Laptop stand", "accessory", True, 2500),
            ("USB hub", "accessory", True, 1800),
            ("[Hidden] New top model", "secret", False, 99800),
            ("[Hidden] Special gift", "secret", False, 0),
        ]
        for name, cat, rel, price in products:
            Product.objects.create(name=name, category=cat, released=rel, price=price)

        # --- ユーザー(認証/IDOR) ---
        users = {
            "admin": "letmein123",
            "alice": "alicepass",
            "bob": "bobpass",
        }
        for uname, pw in users.items():
            u = User.objects.filter(username=uname).first()
            if u is None:
                u = User(username=uname)
            u.set_password(pw)
            u.email = f"{uname}@example.com"
            u.save()

        # --- 口座(IDOR) ---
        Account.objects.all().delete()
        alice = User.objects.get(username="alice")
        bob = User.objects.get(username="bob")
        # IDを必ず 1,2,3 に固定する(IDORデモを分かりやすくするため)。
        # 全削除後、SQLiteの自動採番カウンタも戻してから、明示的にpkを指定して作成する。
        from django.db import connection
        with connection.cursor() as cur:
            try:
                cur.execute("DELETE FROM sqlite_sequence WHERE name='labs_account'")
            except Exception:
                pass  # sqlite_sequence が無い環境では無視
        Account.objects.create(pk=1, owner=alice, full_name="Alice Tanaka",
                               balance=50000, secret_memo="Secret word: sakura")
        Account.objects.create(pk=2, owner=bob, full_name="Bob Suzuki",
                               balance=120000, secret_memo="Secret word: himawari")
        Account.objects.create(pk=3, owner=bob, full_name="Bob Suzuki (savings)",
                               balance=800000, secret_memo="Secret word: tsubaki")

        # --- comments (stored XSS): just clear ---
        Comment.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            "seed done: %d products / %d users / %d accounts" % (
                Product.objects.count(), User.objects.count(),
                Account.objects.count())))
        self.stdout.write("Demo users you can log in: "
                          "admin/letmein123, alice/alicepass, bob/bobpass")
