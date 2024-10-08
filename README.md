# Online Shop

Online Shop is a free and open source website. Django framework is used in
the back-end of this site.

## Authors

- [@AbolfazlKameli](https://github.com/AbolfazlKameli/) (back-end dev)

## Run Locally

Clone the project

```shell
git clone https://github.com/AbolfazlKameli/Online-shop.git
```

Go to the project directory

```shell
cd Online-shop/
```

make a virtual environment

```shell
python3 -m venv .venv
```

activate virtual environment

```shell
source .venv/bin/activate 
```

install requirements

```shell
pip install -r requirements.txt
```

start celery project

```shell
celery -A Ecommerce worker -l INFO  
```

start the django server

```shell
python manage.py runserver
```
