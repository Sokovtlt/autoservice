# Web applications for interaction between car owners and service stations
With this web application, car owners can find the nearest car repair station and get a repair offer. Car owners create a personal account and add their car to it. They create a car repair order. They can choose what kind of service they need: tire fitting, technical inspection or body repair. Registered car repair stations see this order in their personal account. They can make an offer to the customer.


## Content

- [Start](#start)
- [Technologies](#tech)
- [Nuances](#nuances)
- [Why am I creating this application?](#why)
- [To do](#todo)



## <a id="start">Start</a>
To run the application, download the project files. Download static.zip [here](https://drive.google.com/drive/folders/1EEW_9R36Qxe8lty2lRqLKscnAzhGL5D5?usp=sharing) and put it to folder account. Create docker-compose.yml file and add the Django secret key.

```python
version: '3.8'

services:

  django:
    container_name: django
    build:
      context: .
    command: python manage.py runserver 0.0.0.0:8080
    volumes:
      - .:/usr/src/app/
    ports:
      - 8000:8080
    environment:
      - DEBAG=True
      - SECRET_KEY= 'your secret key'
      - ALLOWED_HOSTS=localhost, 127.0.0.1
```

Open the terminal from the project's root directory, and enter the command:

```sh
$ cmod +x ./entrypoint.sh
```
```sh
$ docker-compose up -d --build
```


### <a id="tech">Technologies</a>
For the installation and launch of the project, you need [Docker](https://docker.com/).
Project uses [Python](https://www.python.org/downloads/release/python-3110/) v3.11,
[Django ](https://docs.djangoproject.com/en/4.2/) v4.2 and [JavaScript](https://devdocs.io/javascript/).

### <a id="nuances">Nuances</a>
The project has only the start page



### <a id="why">Why am I creating this application?</a>
This application will be useful for car owners and car repair stations.

## <a id="todo">To do</a>
- [x] add README
- [ ] create a personal account page for car owners
- [ ] create a personal account page for car repair stations
- [ ] create adding car
- [ ] create creating order
- [ ] create creating offer
