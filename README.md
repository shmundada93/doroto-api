Backend for doroto.

```
sudo docker-compose -f docker-compose-dev.yml build
sudo docker-compose -f docker-compose-dev.yml up
```

Manage Database:

```
docker-compose -f docker-compose-dev.yml exec api python manage.py seed
docker-compose -f docker-compose-dev.yml exec api python manage.py db migrate
docker-compose -f docker-compose-dev.yml exec api python manage.py db upgrade
```

DB Admin UI:
http://localhost:9000/
