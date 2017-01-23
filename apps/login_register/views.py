from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse

import bcrypt

# Create your views here.
def index(request):
    return render(request, 'login_register/index.html')

def show(request, id):
    user = User.objects.get(id=id)
    context = {'user': user}
    return render(request, 'login_register/show.html', context)

def process_registration(request):
    if request.method == "POST":
        validation_obj = User.objects.register(request.POST)
        if 'errors' in validation_obj:
            for error in validation_obj['errors']:
                messages.add_message(request, messages.ERROR, error)
        elif 'user' in validation_obj:
            request.session['full_name'] = validation_obj['user']
            user_obj = User.objects.create(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                email = request.POST['email'],
                password = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            )
            request.session['user'] = user_obj.id
            print "ID:", request.session['user']
            return redirect('/show')
        else:
            print "Something went terribly wrong"
    return redirect('/')

def process_login(request):
    if request.method == "POST":
        validation_obj = User.objects.login(request.POST)
        if 'errors' in validation_obj:
            for error in validation_obj['errors']:
                messages.add_message(request, messages.ERROR, error)
        elif 'user' in validation_obj:
            request.session['full_name'] = validation_obj['user']
            request.session['user'] = User.objects.get(email=request.POST['email']).id
            print request.session['user']
            print "*"*50
            # return redirect('/show')
            return redirect(reverse('login_register:show', args=(request.session['user'],)))
        else:
            messages.add_message(request, messages.ERROR, "Something went horribly wrong")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect(reverse("login_register:index"))
