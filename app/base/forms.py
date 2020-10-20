# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, Length

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])
    remember_me = BooleanField('Remember me', id='remember_me_login')

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired(), Length(max=45)])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired(), Length(max=255)])
    sector = SelectField('Sector', id='sector_create', choices=[(x, x) for x in ['Consumer Discretionary', 'Consumer Staples', 'Energy',
                                                                'Financial Services', 'Healthcare', 'Materials & Processing',
                                                                'Producer Durables', 'Technology', 'Utilities']])
