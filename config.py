# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    # FOR LOCAL DEV:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

    SQLALCHEMY_DATABASE_URI = 'postgres://tohjforetehqru:53b9d8d58eacf483f1f4c0cb1e520d926b104cba589f7631641c82894e19c6d8@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d6t7cg26h5blbn'

    # MySQL database URI
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:HeavenBlessesHardwork@localhost/stockdb'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):

    basedir    = os.path.abspath(os.path.dirname(__file__))
    
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

##    # PostgreSQL database
##    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
##        config( 'DB_ENGINE'   , default='postgresql'    ),
##        config( 'DB_USERNAME' , default='appseed'       ),
##        config( 'DB_PASS'     , default='pass'          ),
##        config( 'DB_HOST'     , default='localhost'     ),
##        config( 'DB_PORT'     , default=5432            ),
##        config( 'DB_NAME'     , default='appseed-flask' )
##    )
    
class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
