# django image sample
画像・ファイルアップロード、認証機能をつけたテンプレートプロジェクト

## Lint
```
black app --line-length 120
flake8 app --show-source --max-complexity 5 --max-line-length 120
```

## Set lint
```
flake8 --install-hook git
git config --bool flake8.strict true
cp .flake8 ~/.flake8
```


## Setup
### Production
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
mkdir secret
mkdir -p /var/www/django_file_uploader_sample/media
mkdir -p /var/www/django_file_uploader_sample/static
```
### Development
```
pip install -r requirements.txt
python manage.py makemigrations --settings=config.dev_settings
python manage.py migrate --settings=config.dev_settings
mkdir secret
mkdir media
```

## Deploy
### Production
```
python manage.py collectstatic
gunicorn --env DJANGO_SETTINGSMODULE=config.settings config.wsgi:application --bind <IP Address>:<Port> -w 5 --threads 5 -D --log-syslog --access-logfile access.log --log-file error.log
```

### Development
```
python manage.py runserver --settings=config.dev_settings
```


## Test
```
python manage.py makemigrations --settings=config.test_settings
python manage.py migrate --settings=config.test_settings
python manage.py runserver --settings=config.test_settings

coverage run --source='./app' manage.py test app --settings=config.test_settings
coverage report
coverage html
```