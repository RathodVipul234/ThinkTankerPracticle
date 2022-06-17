# ThinkTanker Practicle

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/RathodVipul234/ThinkTankerPracticle.git
$ cd ThinkTankerPracticle
```

Create a virtual environment:

```sh
$ python3 -m venv venv
```

Activeate virtual environment:
```sh
(venv)$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirnments.txt
```

Create Super User and add Hobbies to your admin panel for user selection hobbies:
```sh
(venv)$ python3 manage.py createsuperuser
```

# Hobbies Example
Volunteering and community involvement,
Writing,
Blogging,
Podcasting,
Marketing,
Learning languages,
Photography,
Travel

Run project with Bellow command
```sh
(venv)$ python3 manage.py runserver
```

# Important Notes
I Havn't added Email and password for sending mail. I just used my mailtrap acctount for this.
you can check newaly genrated password to console as well I just printed out there.

I you want to test real time email sending then just add your gmail credential to settings.py and test it.


# THANK YOU!
