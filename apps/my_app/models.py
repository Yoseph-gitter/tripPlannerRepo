from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def validate_userInputs_NoneLoggedInUser(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 :
            errors['first_name'] = "First Name should be greater than 5"
        if len(postData['last_name']) < 2  :
            errors['last_name'] = "Last Name should be greater than 5"
        if not ( self.validateEmail( postData['email'] )) :
            errors['email']  = "Email is not valid , could you correct and submit!"
        if len(postData['password']) < 8 :
            errors['password'] = "Password can not be less than 8 chars"
       
        if len(postData['password']) != len(postData['password_confirmation']) or ( postData['password'] != postData['password_confirmation'] ):
                errors['password_confirmation'] = "Password is not same as passwordConfirmation"

        return errors
    
    def validateEmail(self, email):
        if len(email) > 6:
            if re.match('[\w\.-]+@[\w\.-]+\.\w{2,4}', email) != None:
                return True
        return False
    
    def validate_userInputs_For_LoggedInUsers(self, postData):
        errors = {}
       
        if not ( self.validateEmail( postData['email'] )) :
            errors['email']  = "Email is not valid , could you correct and submit!"
        if len(postData['password']) < 8 :
            errors['password'] = "Password can not be less than 8 chars"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, unique = True)
    password = models.CharField(max_length=255) 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    # associating it to the manager objects
    objects = UserManager()

# Messages Class would go here


class JobManager(models.Manager):
    def validate_userInputs_NoneLoggedInUserForTrip(self, postData):
        errors = {}
        if len(postData['title']) < 3 :
            errors['title'] = "title should be greater than 3"
        if len(postData['authorText']) < 10  :
            errors['authorText'] = "authorText should be greater than 10"
        
        if len(postData['review']) == 0:
            errors['review'] = "review can not be empty"
     
        return errors  

class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="created_jobs" )
    joined_users = models.ManyToManyField(User, related_name="joined_jobs")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = JobManager()


    
