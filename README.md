# yoka

YokaはDjangoで作成された掲示板アプリです。


## 互換性

* Python 3.8, 3.9, 3.10, 3.11
* Django 4.2

## 使い方

```
pip install -r requirements/local.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

アクセス [http://127.0.0.1:8000](http://127.0.0.1:8000)

サンプルデータ追加

```
python manage.py loaddata address contact_status category
```

## テスト

```
python manage.py test
```
