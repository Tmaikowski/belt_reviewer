from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from .models import Author, Review, Book
from ..login_register .models import User

# Create your views here.
def index(request):
    user_obj = User.objects.get(id=request.session['user'])
    book_obj = Book.objects.all().order_by('-review__created_at')[:3]
    context = {
        'user': user_obj,
        'books': book_obj
    }
    return render(request, 'books/index.html', context)

def show(request, id):
    book = Book.objects.get(id=id)
    context = {'book': book}
    return render(request, 'books/show.html', context)

def edit(request, id):
    return render(request, 'books/edit.html')

def new(request):
    authors = Author.objects.all().distinct()
    context = {'authors': authors}
    return render(request, 'books/new.html', context)

def new_review(request):
    book_obj = Book.objects.get(id=request.POST['book_id'])
    review = Review.objects.validate_review(request, book_obj)
    return redirect(reverse('books:index'))

def process_new_book(request):
    if request.method == "POST":
        created_author = Author.objects.validate_author(request)
        if created_author:
            created_book = Book.objects.validate_book(request, created_author)
        else:
            return redirect(reverse('books:new'))
        if created_book:
            created_review = Review.objects.validate_review(request, created_book)
        else:
            return redirect(reverse('books:new'))
        if not created_review:
            return redirect(reverse('books:new'))
    else:
        return redirect(reverse('books:new'))
    return redirect(reverse('books:index'))

def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect(reverse('books:index'))
