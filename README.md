# ComPETdium

Welcome to Competdium, a website geared towards helping prospective pet owners find their perfect four legged friend and helping pets find their forever home.  Competdium employees a number of features in order to streamline the process and to help emphasize the social aspect of pet hunting.  With an in depth search engine and interactive message board users will not only have the tools to find a pet, but the network and support to help raise them.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites

Install Python3 and create an environment for the project. Run `pip install -r requirements.txt` to install the packages below.  

```
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-Login
pip install Flask-Mail
pip install pusher

```
Remember to open `config.py` and add a valid email:
```
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = ""
```

### Installing 
The `flask` command is installed by Flask, not the application; it must be told where to find the application in order to use it. The `FLASK_APP` environment variable is used to specify how to load the application, in this case we'll be using the development environment.  

Unix Bash (Linuz, Mac, etc.):
```
$ export FLASK_APP=flask_app
$ export FLASK_ENV=development
$ flask run
```
Windows CMD:
```
> set FLASK_APP=filename.py
> set FLASK_ENV=development
> flask run
```

Windows Powershell
```
 > $env:FLASK_APP="flask_app"
 > $env:FLASK_ENV="development" 
 > flask run
```

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) - The web framework used
* [requirements.txt](https://github.com/liz0123/Competdium/blob/main/requirements.txt) - Dependency Management
* [Pusher](https://pusher.com/) - Used for realTime chat

## Versioning 
Version 1.0. For the versions available, see the [Competdium](https://github.com/liz0123/Competdium). 

## Website
visit [ComPETdium](https://www.competdium.com/about/) for the live website.

## Authors

* **Isabel Valdez** - *Initial work* - [liz0123](https://github.com/liz0123)
