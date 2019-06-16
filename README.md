# Django Social Network

An application with basic social network functionality made using Django 2.2, with SQLite as database. The demo version can be found [here](https://khansubhan95.pythonanywhere.com).

## Features

- Users can register for an account and login and logout. Only authenticated users are allowed to view posts.
- An email backend uses the SendGrid API , allowing for confirmation of registered user accounts and sending reset password links.
- Users can make posts with or without images
- User can edit or delete posts made by them.
- Users can see who made posts by clicking on the post owners links.


## Using the demo version

Create a user account [here](https://khansubhan95.pythonanywhere.com). Then go to the entered email id, to confirm your account. If you forgot your password click the forgot password link, enter your email and a link to reset password should be sent to your email id.

## Development on your local machine

1. Clone the repo
1. `cd` into the directory `django-social-network`
1. Install virtualenv `pip3 install virtualenv`
1. Create a virtualenv `virtualenv --python=python3.6 env`
1. Activate the virtual env `source env/bin/activate`
1. Install the dependencies `pip install -r requirements.txt`
1. Go to `django-social-network/social_network/social_network` and the appropriate settings into base.py.template. Remove the .template 1.xtensions to convert it into a Python file.
1. Go to `django-social-network/social_network/main` and the appropriate settings into base.py.template. Remove the .template extensions to convert it into a Python file.
1. Go to `django-social-network/social_network` and run `python manage.py runserver`
1. Follow Django documentation to [makemigrations](https://docs.djangoproject.com/en/2.2/ref/django-admin/#makemigrations), [migrate](https://docs.djangoproject.com/en/2.2/ref/django-admin/#migrate), [createsuperuser](https://docs.djangoproject.com/en/2.2/ref/django-admin/#createsuperuser) and [collectstatic](https://docs.djangoproject.com/en/2.2/ref/django-admin/#collectstatic).

### A note on send_mail

I deployed this app on pythonanywhere.com, which does not allow sending SMTP based mail using SendGrid's backend. Therefore I used the SendGrid HTTP based API to send mail. I have provided code to do both. To use SMTP, use the EMAIL based secrets in base.py.template and uncomment the appropriate code in main/views.py . To use HTTP based API, enter the secret in api_key.py.template, the code by default exists in main/views.py . 

### TODO

1. Migrate database from SQLite to PostgreSQL
1. Add a likes system to the posts
1. Add a comment system
