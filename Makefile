mig:
	python manage.py makemigrations
	python manage.py migrate

flak:
	isort .
	flake8 .

load:
	python manage.py loaddata service country currecny languages shop_category quotas fields



jsonremove_migration:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path ".venv/*" -delete
	find . -path "*/migrations/*.pyc"  -delete

