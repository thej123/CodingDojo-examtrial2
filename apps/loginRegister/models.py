from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

Email_Regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
Name_Regex = re.compile(r'^[a-zA-Z]\w+$')

# Create your models here.

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        # check length of the name fields
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append('Names cannot be fewer than 2 characters')
        # check for only letters in name fields 
        if not re.match(Name_Regex, postData['first_name']) or not re.match(Name_Regex, postData['last_name']):
            errors.append('Names can have only letters')
        # Check if email has been used before
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append('Email has already been registered')
        # check for valid email
        if not re.match(Email_Regex, postData['email']):
            errors.append('Invalid email')
        # check length of password
        if len(postData['password']) < 8:
            errors.append('Password is too small')
        # check if password == password_confirm
        if not (postData['password'] == postData['confirm_password']):
            errors.append('Passwords dont match')
        if not errors:
            # bcrypt the password
            hashing = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(10))
            # add new user to database                                    
            user = User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'], 
                email=postData['email'], 
                password=hashing)
            # return user if added to database
            return user
        # or return the errors that occured
        return errors
    
    def validate_login(self, postData):
        errors = []
        # check if email is in database
        if len(self.filter(email=postData['email'])) > 0:
            # if it is in database then pull out user object
            # the user object will be an element in a list
            # we equal the user to the first element of that list
            # the user will be an object which is a dictionary
            user = self.filter(email=postData['email'])[0]
            # hash the password we got with the encode we had registered for this user - we find the user with the email.
            if not (bcrypt.hashpw(postData['password'].encode(), user.password.encode())):
                # if it password doesnt match then wrong password
                errors.append('Incorrect Password')
        else:
            # if email filter shows nothing then wrong username
            errors.append('Incorrect Email')
        if errors:
            # if errors exist then return errors
            return errors
        # otherwise return the user which is a dictionary
        return user

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    # magic function!
    def __str__(self):
        return self.email