"""
This file defines the database models
"""
import datetime
import re
from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def parse_post_content(content):
    """Extract hashtags from post content"""
    tags = re.findall(r'#(\w+)', content)
    return [tag.lower() for tag in tags]

# Define the database tables
db.define_table(
    'post',
    Field('user_email', default=get_user_email),
    Field('content', 'text'),
    Field('created_on', 'datetime', default=get_time),
)

db.define_table(
    'tag',
    Field('name'),
    Field('post_id', 'reference post'),
)
