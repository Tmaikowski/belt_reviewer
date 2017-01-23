from __future__ import unicode_literals

from django.db import models
from ..login_register .models import User
from django.contrib import messages

# Create your models here.
class AuthorManager(models.Manager):
    def validate_author(self, request):
        existing = request.POST['existing_author']
        new_author = request.POST['new_author']
        errors = {
            'errors': []
        }
        if existing == "None" and new_author:
            #Create new author
            author_obj = Author.objects.create(
                name=request.POST['new_author']
            )
            #returns author object
            return author_obj
        elif not new_author and existing != "None":
            #Get id of existing author and return
            author_obj = Author.objects.get(id=request.POST['existing_author'])
            return author_obj
        elif new_author and existing != "None":
            msg = "Please only select a new or existing author"
            errors['errors'].append(msg)
        elif not new_author and existing == "None":
            msg = "Please enter a new or existing author"
            errors['errors'].append(msg)
        else:
            msg = "Something weird happened"
            errors['errors'].append(msg)
        if errors['errors']:
            for msg in errors['errors']:
                messages.error(request, msg)
            return False
        else:
            return True


    def create_author(self, request):
        print "*"*50
        print "IN THE CREATE AUTHOR FUNCTION"

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

class ReviewManager(models.Manager):
    def validate_review(self, request, book_obj=None):
        content = request.POST['review_content']
        rating = request.POST['rating']
        errors = {
            'errors': []
        }
        if len(content) < 3:
            msg = "Review content must contain at least 3 characters"
            errors['errors'].append(msg)
        if not rating:
            msg = "Please enter a rating"
            errors['errors'].append(msg)
        elif int(rating) < 1 or int(rating) > 5:
            msg = "Please enter a rating from 1 to 5"
            errors['errors'].append(msg)
        if errors['errors']:
            for msg in errors['errors']:
                messages.error(request, msg)
            return False
        else:
            print "IN THE ELSE FOR REVIEW"
            user_obj = User.objects.get(id=request.session['user'])
            review_obj = Review.objects.create(
                content = content,
                rating = rating,
                user = user_obj,
                book = book_obj
            )
            print review_obj
            return review_obj

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User)
    book = models.ForeignKey('Book')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

class BookManager(models.Manager):
    def validate_book(self, request, author_obj=None):
        title = request.POST['title']
        errors = {
            'errors': []
        }
        if not title:
            msg = "Please provide a book title"
            errors['errors'].append(msg)
            print "*"*50
            print msg
        elif len(title) < 3:
            msg = "Title must be at least 3 characters"
            errors['errors'].append(msg)
            print "*"*50
            print msg
        if errors['errors']:
            for msg in errors['errors']:
                messages.error(request, msg)
            return False
        else:
            book_obj = Book.objects.create(
                title = title,
                author = author_obj
            )
            return book_obj

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
