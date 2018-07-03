import bcrypt
import falcon
import jwt
import os
import smtplib
import time
import uuid
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
from playhouse.shortcuts import model_to_dict

from lib.models import User

confirm_serializer = URLSafeTimedSerializer(str(uuid.uuid4()))
reset_serializer = URLSafeTimedSerializer(str(uuid.uuid4()))

def authenticate(email, password):
    try:
        user = User.get(User.email == email)

        if user.confirmed_at is None:
            raise Exception('The user has not been confirmed.')

        if not bcrypt.checkpw(password.encode(), user.hash):
            raise Exception('The user could not be authenticated.')
            
        claims = {
            'user_id': user.id,
            'iss': time.time()
        }
    
        return jwt.encode(claims, 'secret', algorithm='HS256')
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_401)

def confirm_user(token):
    try:
        user_id = confirm_serializer.loads(token, max_age=3600)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_400)
        
    user = User[user_id]
    
    if user.confirmed_at is not None:
        raise falcon.HTTPError(falcon.HTTP_409)
    
    user.confirmed_at = time.time()
    user.save()

def create_user(email, password):
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        user = User.create(email=email, hash=hash)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_409)
        
    return user

def get_user(user_id):
    user = User[user_id]
    return model_to_dict(user, recurse=False, exclude=[User.hash])

def reset_password(token, password):
    try:
        user_id, reset_key = reset_serializer.loads(token, max_age=3600)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_400)
    
    user = User[user_id]
    
    if reset_key != user.reset_key:
        raise falcon.HTTPError(falcon.HTTP_409)
    
    user.hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user.reset_key = uuid.uuid4()
    user.save()

def send_confirm_email(email):
    user = User.get(User.email == email)
    token = confirm_serializer.dumps(user.id)
    
    message = MIMEText(token, 'plain')
    message['Subject'] = 'Confirm your email address'
    
    send_message(email, message)

def send_message(email, message):
    user = os.environ.get('MAIL_USER')
    password = os.environ.get('MAIL_PASSWORD')
    server = os.environ.get('MAIL_SERVER')
    
    message['From'] = user
    
    mail_server = smtplib.SMTP(server, 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.login(user, password)
    mail_server.sendmail(user, email, message.as_string())
    mail_server.quit()

def send_reset_email(email):
    user = User.get(User.email == email)
    token = reset_serializer.dumps((user.id, str(user.reset_key)))
    
    message = MIMEText(token, 'plain')
    message['Subject'] = 'Reset your password'
    
    send_message(email, message)