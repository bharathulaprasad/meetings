### Meeting | Admin

Small meeting plan app for small team

### Installation
```
docker-compose run -d --build
```

**NOTE:** To create a super user;
```
docker exec -ti meetings_web_1 bash
root@c35893d02286:/app# python manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: admin@email.com
Password: 
Password (again): 
Superuser created successfully.
```

### Usage

Go to *http://localhost_or_ip* in browser then enter super user credentials. 

**NOTE:** You need to give staff permission to every registered user

### Screen shot
![ss](ss.png)
