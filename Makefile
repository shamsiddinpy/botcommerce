mig:
	python manage.py makemigrations
	python manage.py migrate

flak:
	isort .
	flake8 .



load:
	python manage.py loaddata service
	python manage.py loaddata country
	python manage.py loaddata currecny
	python manage.py loaddata languages
	python manage.py loaddata shop_category
	python manage.py loaddata plan
	python manage.py loaddata quotas


#Databaseni tozlash
database:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path ".venv/*" -delete
	find . -path "*/migrations/*.pyc"  -delete


#Keshni fayllarni tozalash:
test:
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '*.pyc' -delete