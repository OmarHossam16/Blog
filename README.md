# Blog

### Technologies used :

* Python
* Flask
* MySQL
* SQLAlchemy
* HTML
* CSS
* Bootstrap

## Required pip packages:

* bcrypt
* Flask
* Flask-Bcrypt
* Flask-Login
* Flask-Mail
* Flask-SQLAlchemy
* Flask-WTF

## Or Simply run this command where requirements.txt file is located:

```

$ pip install -r requirements.txt

```
## If you don't have mysql installed just run this command 

```

$ apt-get update
$ apt-get install mysql-server

```

## To Configure the database just run this in mysql:

```SQL

CREATE DATABASE blog;

use blog;

CREATE TABLE user(
user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
username VARCHAR(20) NOT NULL UNIQUE,
email VARCHAR(120) NOT NULL UNIQUE,
image BLOB,
password VARCHAR(60) NOT NULL,
posts_id INT
);

CREATE TABLE post(
user_id INT,
post_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
title VARCHAR(100) NOT NULL,
date_posted DATETIME DEFAULT NOW() NOT NULL,
content LONGTEXT NOT NULL,
FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE SET NULL
);

ALTER TABLE user ADD FOREIGN KEY(posts_id) 
REFERENCES post(user_id) ON DELETE SET NULL;

```

