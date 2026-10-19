# バグ修正report：格納型XSSの「Delete all comments」が効かない

## 症状
- 格納型XSSラボ（`/demo/xss-stored/before/`）で「**Delete all comments**」を押し、確認ダイアログで OK しても **コメントが消えない**。
- 画面は正常に見え、HTTPも 200 が返るが、DBのコメントは残ったまま。

## 原因
URL パターンの **定義順** の問題。

`labs/urls.py` で、何でも受け取る `<str:mode>/` のルートが、`reset/` の専用ルートより **先** に書かれていた。
Django は URL を上から順に照合するため、`/demo/xss-stored/reset/` が
「`mode="reset"` のデモ表示ページ」として先にマッチしてしまい、
**削除用のビュー `xss_stored_reset` が一度も呼ばれていなかった**。

- 実際に呼ばれていた処理：`xss_stored_demo(mode="reset")`（＝ただの表示。削除しない）
- 本来呼ばれるべき処理：`xss_stored_reset`（＝`Comment.objects.all().delete()`）

そのため「200は返るが削除されない」という紛らわしい挙動になっていた。

## 修正箇所
ファイル：`labs/urls.py`（格納型XSSのセクション）

`reset/` の専用ルートを、`<str:mode>/` の汎用ルートより **先** に移動した。

### 修正前（NG）
```python
path("demo/xss-stored/<str:mode>/", views.xss_stored_demo,
     name="lab_demo_xss_stored"),
path("demo/xss-stored/reset/", views.xss_stored_reset,
     name="lab_demo_xss_stored_reset"),
```

### 修正後（OK）
```python
# 注: reset/ を <str:mode>/ より先に定義する(でないと mode="reset" として吸われる)
path("demo/xss-stored/reset/", views.xss_stored_reset,
     name="lab_demo_xss_stored_reset"),
path("demo/xss-stored/<str:mode>/", views.xss_stored_demo,
     name="lab_demo_xss_stored"),
```

## 検証
修正後のサーバーで、HTTP 経由で確認：
- コメント **3件** → `/demo/xss-stored/reset/` 実行 → **0件**
- ブラウザでも「Delete all comments」→ OK で消えることを確認

## ポイント（再発防止）
- Django の URL は **上から順にマッチ** する。
- `<str:xxx>/` のような可変パスは何でも拾うので、
  同じ階層に固定パス（`reset/` など）がある場合は **固定パスを先に** 書く。
- もしくは可変側を正規表現等で制限する（例：`<slug:mode>` でも今回は `reset` を拾ってしまうため、順序での対応が確実）。

## 補足（環境メモ）
- 調査中、`manage.py runserver` のプロセスが複数多重起動していたため全て停止し、
  プロジェクトの `.venv` から1つだけ起動し直した。
- 他の reset（認証ラボ `/demo/auth/<mode>/reset/`）は階層が1つ深く、
  `<mode>/` と衝突しないため同じ問題はない。
