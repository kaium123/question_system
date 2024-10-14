if you have docker , just apply
    docker compose up

if you dont have docker, 

    python3 -m venv qenv
    source testvenv/bin/activate.fish   (if you are linux user then replace it by source testvenv/bin/activate)
    pip3 install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate

start project by applying :
    python3 manage.py runserver

postman collection : 
    https://api.postman.com/collections/32612509-5da4bc96-b760-4c73-95c1-8e0d84275d38?access_key=PMAT-01JA65E6V8JZHAAN1DRWAJYE3B