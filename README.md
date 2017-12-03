## Requirement

- pipenv
- python 3.6.x
- npm 8.9.1

## Install python package and run backend server

```
pipenv install

cd photo-uploader

pipenv run python manage.py migrate

# run backend server on http://127.0.0.1:8000/
pipenv run python manage.py runserver

```

## Install frontend package and run frontend server

```
cd photo-uploader/photo_uploader/frontend

npm install 

# run frontend server on http://localhost:8080
npm start
```
## Start developing

You can now visit http://localhost:8080