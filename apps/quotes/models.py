from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
# from datetime import date



class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['Name']) < 3:
            errors['Name'] = "Name  must be at least 3 characters"

        if len(postData['Alias']) < 1:
            errors['Alias'] = "Alias  must be at least 1 characters"

        if not my_re.match(postData['email']):
            errors['email'] = " enter a valid email id"

        if postData['password'] != postData['confirm_password']:
            errors['password'] = "passwords must match"

        return errors
        # min_age = 24
        # max_date = date.today()
        # try:
        #     max_date = max_date.replace(year=max_date.year - min_age)
        # except ValueError: # 29th of february and not a leap year
        #     assert max_date.month == 2 and max_date.day == 29
        #     max_date = max_date.replace(year=max_date.year - min_age, month=2, day=28)
        # people = People.objects.filter(birth_date__lte=max_date)

    def validateLogin(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        hash2 = postData['password'].encode()
       
        if not my_re.match(postData['email']):
            errors['email'] = "Enter a valid email id"
        else :
            # try:
            try :
                user = User.objects.get(email = postData['email'])
                print "user  ", user
                if (user):
                    if bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                       
                        print "logged in"
                    else :
                            errors['password'] = "password do not match"
                       
            except :
            # User.DoesNotExist:
           
                errors['emailnotexist']="email doesn't exist"
                print "user not found"
               
        print errors
        return errors

class QuoteManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "author name must be at least 3 characters"

        if len(postData['info']) < 20:
            errors['info'] = "Quote must be at least 10 characters"

        return errors

class User(models.Model):
    Name = models.CharField(max_length = 255)
    Alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.Name, self.password, self.email)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.Name, self.password, self.email)



class Quote(models.Model):
    author = models.CharField(max_length = 255)
    info = models.CharField(max_length = 255)
    uploader = models.ForeignKey(User, related_name='quotes')
    authors = models.ManyToManyField(User, related_name='favourites')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

    def __repr__(self):
        return "User: \n{}\n{}\n{}\n".format(self.id, self.author, self.info)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n".format(self.id, self.author, self.info)