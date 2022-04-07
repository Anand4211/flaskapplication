from os import environ
import os
import flask_app


class Config(object):
    DEBUG = True
    TESTING = False
    DB_NAME = environ.get("DB_NAME")
    DB_USERNAME = environ.get("DB_USERNAME")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_PORT = environ.get("DB_PORT")
    DB_HOST = environ.get("DB_HOST")

    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    DEVELOPMENT = True
    DB_NAME = environ.get("DB_NAME")
    DB_USERNAME = environ.get("DB_USERNAME")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_PORT = environ.get("DB_PORT")
    DB_HOST = environ.get("DB_HOST")
    SESSION_COOKIE_SECURE = False
