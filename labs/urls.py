from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lab/<slug:slug>/", views.detail, name="lab_detail"),

    # 1. SQLi
    path("demo/sql-injection/<str:mode>/", views.sqli_demo, name="lab_demo_sqli"),

    # 2. 反射型XSS
    path("demo/xss-reflected/<str:mode>/", views.xss_reflected_demo,
         name="lab_demo_xss_reflected"),

    # 3. 格納型XSS
    # 注: reset/ を <str:mode>/ より先に定義する(でないと mode="reset" として吸われる)
    path("demo/xss-stored/reset/", views.xss_stored_reset,
         name="lab_demo_xss_stored_reset"),
    path("demo/xss-stored/<str:mode>/", views.xss_stored_demo,
         name="lab_demo_xss_stored"),

    # 4. CSRF
    path("demo/csrf/before/", views.csrf_before, name="lab_demo_csrf_before"),
    path("demo/csrf/after/", views.csrf_after, name="lab_demo_csrf_after"),
    path("demo/csrf/trap/<str:mode>/", views.csrf_trap, name="lab_demo_csrf_trap"),

    # 5. 認証
    path("demo/auth/<str:mode>/", views.auth_demo, name="lab_demo_auth"),
    path("demo/auth/<str:mode>/reset/", views.auth_reset, name="lab_demo_auth_reset"),

    # 6. パストラバーサル
    path("demo/path-traversal/<str:mode>/", views.path_demo, name="lab_demo_path"),

    # 7. OSコマンドインジェクション
    path("demo/os-command/<str:mode>/", views.oscmd_demo, name="lab_demo_oscmd"),

    # 8. IDOR
    path("demo/idor/<str:mode>/", views.idor_demo, name="lab_demo_idor"),

    # 9. ファイルアップロード
    path("demo/file-upload/<str:mode>/", views.upload_demo, name="lab_demo_upload"),

    # 10. チャットボット機能
    path("chatbot/", views.chatbot_page, name="chatbot"),
    path("api/chatbot/", views.chatbot_api, name="chatbot_api"),

]