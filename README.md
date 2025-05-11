# Online Shop

💫 This **OnlineShop** has all the features that a store should have and made with Django(MVT)

---

## 🌐 Technologies

- [Django](https://www.djangoproject.com/) ➡️ Django is a Python framework that makes it easier to create web sites using Python.
- [Docker](https://www.docker.com/) ➡️ Docker is an open platform for developing, shipping, and running applications.
- [Nginx](https://nginx.org/) ➡️ NGINX is open-source web server software used for reverse proxy, load balancing, and caching.
- [Celery](https://docs.celeryq.dev/en/stable/) ➡️ Celery is an open source asynchronous task queue or job queue which is based on distributed message passing.
- [Rabbitmq](https://www.rabbitmq.com/) ➡️ RabbitMQ is a reliable and mature messaging and streaming broker, which is easy to deploy on cloud environments, on-premises, and on your local machine. It is currently used by millions worldwide.

---

## 🚀 Features

- **OTP Authentication**
- **JWT Authentication**
- **Cart**
- **Discount code**
- **Payment gateaway**
- **Filter products**
- **Search products**
- **Comment and Rating(Like)**
- **Categories**

---

## 🗄️ Database

- **SQLite(Development mode)**
- **Postgresql(Production Mode)**

---

## 🧩 installation


1. 💠 Clone Repository

   ```
   $ git clone https://github.com/Abolfazlsi/online-shop.git

   $ cd OnlineShop_API
   ```

2. 💠 Install Virtualenv

   ```
   $ pip install virtualenv

   $ virtualenv venv
   ```

- Windows
  
   ```
   > cd venv/Script/

   > activate

   > cd ../.. (Back to online-shop folder)   
   ```

- Linux

   ```
   $ source venv/bin/activate
   ```

3. 💠 Install Packages

   ```
   $ pip install -r requirements.txt
   ```

4. 💠 Migrate
   ```
   $ python manage.py migrate
   ```

---

## 🪄 Use

1. 💠 create super user (you can enter the admin panel)
    ```
   $ python manage.py createsuperuser
   ```
   - set phone number and password for yourself.

3. 💠 Run Project

   ```
   $ python manage.py runserver
   ```

- you will see this url **`http://127.0.0.1:8000/`** ➡️ Enter this url in a **Browser**.

- you can go to this url **`http://127.0.0.1:8000/admin/`** to enter the admin panel.(enter the phone and password you set in the previous step)

4. 💠 Run Celery
  
   ```
   $ celery -A core worker -l info
   ```
   
   - or
   
   ```
   $ celery -A core worker -l info --pool=solo
   ```
   
   - run celery beat
     
   ```
   $ celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseSchedule
   ```

---

## Socials🤝

- Github: [![github](https://img.icons8.com/?size=40&id=Mhl1TfJLdkh5&format=png&color=000000)](https://github.com/Abolfazlsi)
  
- Linkedin: [![LinkedIn](https://img.icons8.com/?size=40&id=13930&format=png&color=000000)](https://www.linkedin.com/in/abolfazl-shojaei-21101b314/)





  
  




