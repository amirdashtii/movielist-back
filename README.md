# movielist

[![LICENSE](https://img.shields.io/badge/LICENSE-GPL----3.0-green)](https://github.com/amirdashtii/movielist-back/blob/master/LICENSE) 
[![Requirements](https://img.shields.io/badge/Requirements-See%20Here-orange)](https://github.com/amirdashtii/movielist-back/blob/master/requirements.txt)

This is a trial project at which you can list your favorite movies watched or not watched and or etc.

<div dir="rtl"> 
این یک پروژه‌ی شخصی است که در آن می‌توانید از فیلم‌های مورد علاقه‌تان، فیلم‌هایی که دیده‌اید، فیلم‌هایی که می‌خواهید ببینید و... لیست  تهیه کنید.
 در این پروژه از تکنولوژی‌های زیر استفاده می‌شود:

- پایتون
- جنگو
- مای اسکوئل

</div>

## How to run
1. Install python3, pip3, virtualenv, MySQL in your system.
2. Clone the project `git clone https://github.com/amirdashtii/movielist-back && cd movielist-back`
3. In the movielist folder, rename the `config.py.sample` to `config.py` and do proper changes.
4. db configs are in config.py. Create the db and grant all access to the specified user with specified password.
5. Create a virtualenv named venv using `virtualenv -p python3 venv`
6. Connect to virtualenv using `source venv/bin/activate`
7. From the project folder, install packages using `pip install -r requirements.txt`
8. Now environment is ready. Run it by `python manage.py makemigrations`
9. Continue with `python manage.py migrate`
10. Lastly `python manage.py runserver`

## Example for creating db and granting access:

> Note: this is just a sample. You have to find your own system's commands.

```
CREATE DATABASE movielist;
USE movielist;
CREATE USER 'movielist'@'localhost' IDENTIFIED BY 'test' PASSWORD NEVER EXPIRE;
GRANT ALL PRIVILEGES ON movielist.* TO 'movielist'@'localhost';
```