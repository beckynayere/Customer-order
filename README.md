# Customer Order Service

A Django-based application designed for managing customer orders efficiently. This service integrates with PostgreSQL for data persistence and offers robust authentication using Django-Allauth.

---

## 🚀 Features

- **Order Management**: Add, update, and track customer orders.
- **User Authentication**: Powered by Django-Allauth for secure user management.
- **PostgreSQL Database**: Reliable and scalable storage for customer and order data.
- **RESTful API**: Clean and structured endpoints for interacting with the system.
- **Scalability**: Built with scalability and extensibility in mind.

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Virtualenv
- Git

### Clone the Repository

```bash
git clone https://github.com/your-repo/customer-order-service.git
cd customer-order-service

### Setup Virtual Env

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate

### Install Dependencies

```bash

pip install -r requirements.txt

##### Setup Database  
  SetUp your database User,Password, Host then make migrate  
 ```bash 
python manage.py makemigrations hood
 ``` 
 Now Migrate  
 ```bash 
 python manage.py migrate 
```
##### Run the application  
 ```bash 
 python manage.py runserver 
``` 
##### Testing the application  
 ```bash 
 python manage.py test 
```
Open the application on your browser `127.0.0.1:8000`.  
  
 
## Technology used  
  
* [Python3.6](https://www.python.org/)  
* [Django 2.2.6](https://docs.djangoproject.com/en/2.2/)  
* [Heroku](https://heroku.com)
*  
  
  
## Known Bugs  
* There are no known bugs currently but pull requests are allowed incase you spot a bug  
  
## Contact Information   
If you have any question or contributions, please email me at [nereahhopebecky@gmail.com]  
  
## License 

* [![License](https://img.shields.io/packagist/l/loopline-systems/closeio-api-wrapper.svg)](https://beckynayere/Customer-order/blob/master/LICENSE)  
* Copyright (c) 2020 **Becky Nayere**


