Installation:
```
pip install -r requirements.txt
```
Run Doker:
```
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```
Create database:
```
python manage.py migrate
```
Load demo database(optional):
```
python manage.py fake_date
```
run server:
```
python manage.py runserver
```