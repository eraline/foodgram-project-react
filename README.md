# Foodgram: Service For Your Recipes

In the scope of the service you can:
- Create user and change passwords (djoser)
- Create recipes
- Subscribe to different authors
- Add recipes to favourites list
- Add recipes to shopping cart and download the shopping list

Project is available at http://84.201.178.166/recipes
Admin user: admin@mail.ru
password: afiyetolsun


#### Stack: 
Python 3, Django, gunicorn, PostgreSQL, nginx, react

## How start project:

Clone a repository and go to command line:

```sh
git clone https://github.com/eraline/foodgram-project-react.git
```

```sh
cd foodgram-project-react/infra/
```

Create .env file.

```sh
touch .env
```

Fill it in with your data. 

```sh
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='djangosecretkey'
```

```sh
cd infra
```

Run docker compose

```sh
docker compose up
```

Login to backend container

```
docker exec -it infra-backend-1 bash
```

Run migrate

```
python /app/manage.py migrate
```

#### Optional (load ingredients from dump)

In backend container run:
```
python /app/manage.py shell
```
In the python shell run the following commands:
```
from recipes.tools import load_ingredients
load_ingredients('/app/data/ingredients.csv')
```

Done!

### Author
##### backend: https://github.com/eraline
