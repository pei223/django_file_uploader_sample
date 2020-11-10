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
mkdir -p /var/www/django_file_uploader_sample/media
mkdir -p /var/www/django_file_uploader_sample/static
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
apt install mysql-server mysql-client libmysqlclient-dev
pip install mysqlclient

# Database setting(MySQL)
create user <user name> identified by '<password>';
create database <DB name>;
grant all on <DB name>.* to '<user name>'@'localhost' identified by '<Password>';
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
gunicorn --env DJANGO_SETTINGSMODULE=config.settings config.wsgi:application --bind 127.0.0.1:<Port> -w 5 --threads 5 -D --log-syslog --access-logfile access.log --log-file error.log
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