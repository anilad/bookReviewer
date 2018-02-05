from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^0-9]+$')
PASSWORD_REGEX = re.compile(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=-_.]).*$")

class UserManager(models.Manager):
    def valCreate(self, postData):
        errors = []
        bday = datetime.strptime(postData['birthdate'], '%Y-%m-%d')
        numResults = User.objects.filter(email=postData['email'])
        if len(numResults) > 0:
            errors.append("Unable to register")
            return (False, errors)
        if len(postData['fName'])<1 and len(postData['lName'])<1 and len (postData['email'])<1 and len(postData['birthdate'])<1 and len(postData['pwd'])<1:
            errors.append("Please fill out the form to register")
            return (False, errors)
        if len(postData['fName'])<2:
            errors.append("First name is required")
        elif not NAME_REGEX.match(postData['fName']):
            errors.append("Invalid first name")
        if len(postData['lName'])<2:
            errors.append("Last name is required")
        elif not NAME_REGEX.match(postData['lName']):
            errors.append("Invalid last name")
        if postData['email'] == "":
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email")
        if postData['birthdate'] == "":
            errors.append("Birthdate is required")
        else:
            today=datetime.today()
            if (today-bday).days/365<18:
                errors.append("Unable to register: User must be 18 years or older")
        if postData['pwd'] == "":
            errors.append("Password is required")
        elif not PASSWORD_REGEX.match(postData['pwd']):
            errors.append("Invalid password")
        elif len(postData['pwd'])>15:
            errors.append("Password is too long")
        if postData['pwd'] != postData['confirm']:
            errors.append("Password does not match password confirmation")
        if len(errors) == 0:
            hashed = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['fName'], last_name = postData['lName'], email = postData['email'],birthday = bday, password = hashed)
            return (True, user)
        else:
            return (False, errors)

    def valLogin(self,postData):
        errors=[]
        if postData['email'] == "" and postData['pwd'] == "":
            errors.append("Please fill out the form to login")
            return (False, errors)
        if postData['email'] == "":
            errors.append("Email is required")
        elif postData['pwd'] == "":
            errors.append("Password is required")
        if not User.objects.filter(email = postData['email']):
            errors.append("Incorrect email")
        else:
            password = User.objects.filter(email = postData['email'])[0].password
            if not bcrypt.hashpw(postData['pwd'].encode(), password.encode()):
                errors.append("Incorrect password")
        if len(errors)!=0:
            return (False, errors)
        else:
            user = self.get(email = postData['email'])
            return (True, user)

    def valUserUpdate(self, postData, id):
        errors = []
        if len(postData['fName'])<1 and len(postData['lName'])<1 and len (postData['email'])<1:
            errors.append("Please fill out the form to update user information")
            return (False, errors)
        if postData['fName'] == "":
            errors.append("First name is required")
        elif not NAME_REGEX.match(postData['fName']):
            errors.append("Invalid first name") 
        if postData['lName'] == "":
            errors.append("Last name is required")
        elif not NAME_REGEX.match(postData['lName']):
            errors.append("Invalid last name")
        if postData['email'] == "":
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email")
        if len(errors) != 0:
            return (False, errors)
        else:
            user = User.objects.get(id=id)
            user.first_name=postData['fName']
            user.last_name=postData['lName']
            user.email=postData['email']
            user.save()
            return (True, user)
    
    def userDelete(self, id):
        ratings = User.objects.user_ratings.all()
        if ratings:
            Rating.objects.filter(rater__id__contains="id").delete()
        User.objects.get(id=id).delete()
        return (True)
    
    def valBook(self, postData, id):
        errors = []
        if postData['title'] == "" and postData['author'] == None and postData['add_author'] == "" and postData['review'] == "" and postData['rating'] == None:
            errors.append("Please fill out the form to add and review a book")
            return (False, errors)
        if postData['title'] == "":
            errors.append("Title is required")
        if postData['author'] == None and postData['add_author'] == "":
            errors.append("Author is required")
        if Author.objects.filter(name = postData['add_author']):
            errors.append("Author already exists")
        if postData['review'] == "":
            errors.append("Review is required")
        if postData['rating'] == None:
            errors.append("Rating is required")
        if len(errors) != 0:
            return (False, errors)
        else:
            author = None
            if postData['add_author'] == "":
                author = Author.objects.get(name=postData['author'])
            else:
                author = Author.objects.create(name=postData['add_author'])
            book = Book.objects.create(title = postData['title'], writer = author)
            # Error at line below
            user = User.objects.get(id=id)
            rating = Rating.objects.create(rate = postData['rating'], review = postData['review'], rater = user, rated_book = book)
            return (True, rating)
    
    def valReview(self, postData, id, book_id):
        errors=[]
        if postData['review']=="":
            errors.append("Review is required")
        if postData['rating']==None:
            errors.append("Rating is required")
        if len(errors)!=0:
            return (False, errors)
        else:
            user = User.objects.get(id=id)
            book = Book.objects.get(id=book_id)
            rating = Rating.objects.create(rate=postData['rating'], review=postData['review'], rater=user, rated_book = book)
            return (True, rating)

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    birthday=models.DateField(null=True, blank=True)
    password=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Author(models.Model):
    name=models.CharField(max_length= 255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Book(models.Model):
    title=models.CharField(max_length=100)
    writer=models.ForeignKey(Author, related_name="written_books")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Rating(models.Model):
    rate=models.IntegerField()
    review=models.CharField(max_length=255)
    rater=models.ForeignKey(User, related_name="user_ratings")
    rated_book=models.ForeignKey(Book, related_name="book_ratings")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

