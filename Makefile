mig:
	python manage.py makemigrations
	python manage.py migrate

flak8:
	isort .
	flake8 .

load:
	python manage.py loaddata service.json
	python manage.py loaddata country.json
	python manage.py loaddata currecny.json
	python manage.py loaddata languages.json
	python manage.py loaddata shop_category.json
	python manage.py loaddata quotas.json
	python manage.py loaddata fields.json




jsonremove_migration:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path ".venv/*" -delete
	find . -path "*/migrations/*.pyc"  -delete

