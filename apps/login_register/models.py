from __future__ import unicode_literals
from django.db import models

import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def login(self, post_obj):
        email = post_obj['email']
        pw = post_obj['pw'].encode()

        validation_obj = {
            'errors': []
        }

        try:
            user = User.objects.get(email=email)
        except:
            msg = "Email address doesn't exist. Please register."
            validation_obj['errors'].append(msg)
            return validation_obj
        if bcrypt.hashpw(pw, user.password.encode()) == user.password.encode():
            return {'user': user.first_name + " " + user.last_name}
        else:
            msg = "Invalid password"
            validation_obj['errors'].append(msg)
            return validation_obj

    def register(self, post_obj):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        first_name = post_obj['fname']
        last_name = post_obj['lname']
        email = post_obj['email']
        pw = post_obj['pw']
        confirm_pw = post_obj['confirm_pw']

        validation_obj = {
            'errors': []
        }

        if not first_name or not last_name:
            msg = "You must input a first and last name"
            validation_obj['errors'].append(msg)
        try:
            User.objects.get(email=email)
            msg = "Email already exists"
            validation_obj['errors'].append(msg)
        except:
            pass
        if not EMAIL_REGEX.match(email):
            msg = "Invalid Email"
            validation_obj['errors'].append(msg)
        if len(pw) < 8:
            msg = "Password must be at least 8 characters"
            validation_obj['errors'].append(msg)
        if pw != confirm_pw:
            msg = "Passwords must match"
            validation_obj['errors'].append(msg)

        if validation_obj['errors']:
            return validation_obj
        else:
            return {'user': first_name + " " + last_name}


class User(models.Model):
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=65)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
